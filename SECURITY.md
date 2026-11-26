# Security policy

Report vulnerabilities in any ERP-02 repository **privately**. Never open a public issue, pull request, discussion or comment that describes a vulnerability, and never include real credentials, tokens, personal data or production data in a report.

## How to report

Use GitHub private vulnerability reporting: open the affected repository's **Security** tab and choose **Report a vulnerability**. If that button is not available for the repository, report through this repository instead: <https://github.com/ERP-02/.github/security/advisories/new>. Only the maintainers can see the report.

## What to include

Copy this template into the report:

```text
Affected repository and version (commit SHA or tag):
Component (e.g. identity-service login, erp procurement API):
Vulnerability type (e.g. authorization bypass, injection, tenant isolation):
Impact (what an attacker can read, change or deny, and who can exploit it):
Steps to reproduce (against a local stack; redact secrets):
Expected vs observed behaviour:
Suggested fix or mitigation (optional):
Whether the issue is already public or exploited (yes / no / unknown):
```

## What happens next

- The maintainers acknowledge the report within 5 working days, assess severity and keep the discussion in the private advisory.
- Fixes are developed in a private fork or advisory branch, then released with a published advisory crediting the reporter unless they prefer otherwise.
- Please do not disclose the issue publicly until the advisory is published.

## Scope

In scope: code and configuration in the ERP-02 repositories (ERP, Identity, infrastructure templates, integration and reporting services, shared libraries, developer tools). Out of scope: tests against deployed production tenants, denial-of-service testing, social engineering and third-party services. Test only against your own local stack.
