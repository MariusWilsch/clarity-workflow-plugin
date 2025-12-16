#!/bin/bash
# Maker Selection - Display maker items grouped by status
# Scope: MariusWilsch only, maker items, excludes CLAUDE-CODE-IMPROVEMENTS and sub-issues

echo "=== STEP 2: MAKER SELECTION (MariusWilsch only) ==="
echo ""

data=$(gh api graphql -f query='{
  repository(owner: "DaveX2001", name: "deliverable-tracking") {
    issues(first: 100, states: OPEN, filterBy: {assignee: "MariusWilsch"}, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        title
        labels(first: 10) { nodes { name } }
        parent { number }
      }
    }
  }
}')

# REVIEW
review=$(echo "$data" | jq -r '[.data.repository.issues.nodes[]
  | select(.parent == null)
  | select(.labels.nodes | map(.name) | any(. == "review"))
  | select(.labels.nodes | map(.name) | any(. == "maker"))
  | select(.labels.nodes | map(.name) | any(. == "CLAUDE-CODE-IMPROVEMENTS") | not)
  | "#\(.number): \(.title)"]')
review_count=$(echo "$review" | jq 'length')
echo "=== REVIEW ($review_count) ==="
echo "$review" | jq -r 'if length == 0 then "(empty)" else .[] end'

echo ""

# IN-PROGRESS
inprog=$(echo "$data" | jq -r '[.data.repository.issues.nodes[]
  | select(.parent == null)
  | select(.labels.nodes | map(.name) | any(. == "in-progress"))
  | select(.labels.nodes | map(.name) | any(. == "maker"))
  | select(.labels.nodes | map(.name) | any(. == "CLAUDE-CODE-IMPROVEMENTS") | not)
  | "#\(.number): \(.title)"]')
inprog_count=$(echo "$inprog" | jq 'length')
echo "=== IN-PROGRESS ($inprog_count) ==="
echo "$inprog" | jq -r 'if length == 0 then "(empty)" else .[] end'

echo ""

# TO-DO
todo=$(echo "$data" | jq -r '[.data.repository.issues.nodes[]
  | select(.parent == null)
  | select(.labels.nodes | map(.name) | any(. == "to-do"))
  | select(.labels.nodes | map(.name) | any(. == "maker"))
  | select(.labels.nodes | map(.name) | any(. == "CLAUDE-CODE-IMPROVEMENTS") | not)
  | "#\(.number): \(.title)"]')
todo_count=$(echo "$todo" | jq 'length')
echo "=== TO-DO ($todo_count) — select max 3 for book ==="
echo "$todo" | jq -r 'if length == 0 then "(empty)" else .[] end'
