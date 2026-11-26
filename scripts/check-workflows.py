#!/usr/bin/env python3
"""ERP-02 GitHub Actions workflow policy check (ERP-02/.github#27).

Usage: check-workflows.py FILE_OR_DIRECTORY...

Rules (`yaml` reports an unparseable file; a finding prints as "<file>: <rule>: <detail>" and makes the exit status 1):
  pinned-action        every remote `uses:` (action or reusable workflow) is pinned to a full 40-hex commit SHA
  permissions          the workflow declares top-level `permissions`, never `write-all`; each `write` scope carries an
                       inline `# reason` comment on its line
  no-pull-request-target  the workflow is never triggered by `pull_request_target`
  checkout-credentials `actions/checkout` steps set `persist-credentials: false`
  no-secret-in-run     `run:` scripts never expand `${{ secrets.* }}` directly (pass secrets through `env:`)
  no-secret-echo       `run:` scripts never echo/print a secret-backed environment variable and never enable `set -x`
                       while one is in scope
  no-untrusted-expression  `run:` scripts never expand attacker-controlled event fields (titles, bodies, branch names...)
  destructive-opt-in   steps with destructive commands run only on `workflow_dispatch` and behind an `if:` on an input
Requires PyYAML (preinstalled on GitHub-hosted Ubuntu runners).
"""
import os
import re
import sys

import yaml

SHA = re.compile(r"@[0-9a-f]{40}$")
SECRET_EXPR = re.compile(r"\$\{\{[^}]*\bsecrets\.")
UNTRUSTED = re.compile(
    r"\$\{\{[^}]*github\.(?:event\.(?:issue\.(?:title|body)|pull_request\.(?:title|body|head\.ref|head\.label)|comment\.body"
    r"|review\.body|review_comment\.body|head_commit\.(?:message|author\.(?:name|email))|commits|pages|discussion\.(?:title|body))"
    r"|head_ref)")
DESTRUCTIVE = re.compile(
    r"\b(?:rm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+/(?:\s|$)|docker\s+(?:system|volume|image)\s+prune|docker\s+volume\s+rm|dropdb|DROP\s+DATABASE"
    r"|git\s+push\s+(?:.*\s)?(?:--force|-f)\b|gh\s+(?:release|repo)\s+delete|terraform\s+destroy|kubectl\s+delete)", re.IGNORECASE)
PRINT = r"(?:echo|printf|cat\s+<<<)"


class Loader(yaml.SafeLoader):
    """Keeps `on` as a string key instead of YAML 1.1 boolean True."""


Loader.yaml_implicit_resolvers = {k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:bool"]
                                  for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def triggers(doc):
    on = doc.get("on", {})
    if isinstance(on, str):
        return {on}
    if isinstance(on, list):
        return set(on)
    return set(on or {})


def check(path):
    text = open(path, encoding="utf-8").read()
    findings = []
    try:
        doc = yaml.load(text, Loader=Loader) or {}
    except yaml.YAMLError as error:
        return [f"{path}: yaml: {str(error).splitlines()[0]}"]

    def add(rule, detail):
        findings.append(f"{path}: {rule}: {detail}")

    on = triggers(doc)
    if "pull_request_target" in on:
        add("no-pull-request-target", "pull_request_target runs fork code with secrets; use pull_request")

    if "permissions" not in doc:
        add("permissions", "declare top-level permissions (e.g. contents: read)")
    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.split("#", 1)
        if re.search(r"\bpermissions\s*:\s*write-all\b", stripped[0]):
            add("permissions", f"line {line_no}: write-all is never allowed")
        elif re.search(r"^\s*[a-z-]+\s*:\s*write\s*$", stripped[0]) and (len(stripped) < 2 or not stripped[1].strip()):
            add("permissions", f"line {line_no}: write scope without an inline '# reason' comment")

    workflow_env = doc.get("env") or {}
    jobs = doc.get("jobs") or {}
    for job_id, job in jobs.items():
        job = job or {}
        uses = job.get("uses")
        if uses and not uses.startswith("./") and not SHA.search(uses):
            add("pinned-action", f"job {job_id}: {uses} is not pinned to a commit SHA")
        job_env = {**workflow_env, **(job.get("env") or {})}
        for index, step in enumerate(job.get("steps") or []):
            step = step or {}
            where = f"job {job_id} step {step.get('name') or step.get('id') or index + 1}"
            step_uses = step.get("uses")
            if step_uses and not step_uses.startswith(("./", "docker://")) and not SHA.search(step_uses):
                add("pinned-action", f"{where}: {step_uses} is not pinned to a commit SHA")
            if step_uses and step_uses.split("@")[0] == "actions/checkout":
                if str((step.get("with") or {}).get("persist-credentials", "")).lower() != "false":
                    add("checkout-credentials", f"{where}: set persist-credentials: false")
            run = step.get("run")
            if not isinstance(run, str):
                continue
            if SECRET_EXPR.search(run):
                add("no-secret-in-run", f"{where}: pass secrets through env, not ${{{{ secrets.* }}}} in the script")
            env = {**job_env, **(step.get("env") or {})}
            secret_vars = [k for k, v in env.items() if isinstance(v, str) and SECRET_EXPR.search(v)]
            for name in secret_vars:
                if re.search(PRINT + r"[^\n]*\$\{?" + re.escape(name) + r"\b", run):
                    add("no-secret-echo", f"{where}: prints secret-backed variable {name}")
            if secret_vars and re.search(r"^\s*set\s+-[a-zA-Z]*x", run, re.MULTILINE):
                add("no-secret-echo", f"{where}: set -x would trace secret-backed variables")
            if UNTRUSTED.search(run):
                add("no-untrusted-expression", f"{where}: pass untrusted event fields through env and quote them")
            if DESTRUCTIVE.search(run):
                guarded = "inputs." in str(step.get("if", "")) or "inputs." in str(job.get("if", ""))
                if on != {"workflow_dispatch"} or not guarded:
                    add("destructive-opt-in", f"{where}: destructive command needs workflow_dispatch only and an if: on an input")
    return findings


def files(args):
    for arg in args:
        if os.path.isdir(arg):
            for name in sorted(os.listdir(arg)):
                if name.endswith((".yml", ".yaml")):
                    yield os.path.join(arg, name)
        else:
            yield arg


def main(argv):
    if not argv:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    findings = []
    checked = 0
    for path in files(argv):
        checked += 1
        findings.extend(check(path))
    for finding in findings:
        print(finding)
    print(f"{'FAIL' if findings else 'PASS'}: {checked} workflow(s), {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
