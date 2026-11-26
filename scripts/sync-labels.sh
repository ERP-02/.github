#!/bin/sh
# Print (default) or apply the labels.yml taxonomy to one repository. Creates missing labels and updates colour and
# description of existing ones; never deletes a label. Usage: scripts/sync-labels.sh OWNER/REPO [--apply]
set -eu
repo=${1:?usage: sync-labels.sh OWNER/REPO [--apply]}
apply=${2:-}
file=$(dirname "$0")/../labels.yml
ruby -ryaml -e 'YAML.load_file(ARGV[0])["labels"].each { |l| puts [l["name"], l["color"], l["description"]].join("\t") }' "$file" |
while IFS="$(printf '\t')" read -r name color description; do
  if [ "$apply" = "--apply" ]; then
    gh label create "$name" --repo "$repo" --color "$color" --description "$description" --force >/dev/null
    echo "applied $name"
  else
    echo "would apply $name ($color): $description"
  fi
done
[ "$apply" = "--apply" ] || echo "dry run: pass --apply to change $repo"
