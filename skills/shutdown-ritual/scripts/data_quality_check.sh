#!/bin/bash
# Data Quality Check - Find items missing maker/manager label
# Scope: All assignees, to-do/in-progress/review, excludes CLAUDE-CODE-IMPROVEMENTS and sub-issues

echo "=== STEP 1: DATA QUALITY CHECK ==="
echo ""

result=$(gh api graphql -f query='{
  repository(owner: "DaveX2001", name: "deliverable-tracking") {
    issues(first: 100, states: OPEN) {
      nodes {
        number
        title
        assignees(first: 5) { nodes { login } }
        labels(first: 10) { nodes { name } }
        parent { number }
      }
    }
  }
}' --jq '.data.repository.issues.nodes[]
  | select(.parent == null)
  | select(.labels.nodes | map(.name) | any(. == "to-do" or . == "in-progress" or . == "review"))
  | select(.labels.nodes | map(.name) | any(. == "CLAUDE-CODE-IMPROVEMENTS") | not)
  | select((.labels.nodes | map(.name) | any(. == "maker" or . == "manager")) | not)
  | "#\(.number) [\(.labels.nodes | map(.name) | map(select(. == "to-do" or . == "in-progress" or . == "review")) | .[0])] @\(.assignees.nodes | map(.login) | join(",") | if . == "" then "unassigned" else . end): \(.title)"')

if [ -z "$result" ]; then
    echo "✓ All items have maker/manager classification"
else
    echo "Items missing maker/manager label:"
    echo ""
    echo "$result"
fi
