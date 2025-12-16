#!/bin/bash
# monitor_session.sh - Extract and display last N messages from a conversation
# Usage: monitor_session.sh <conversation_path> [num_messages]
#
# AI-driven monitoring pattern:
#   while true; do sleep 30 && ./monitor_session.sh <path>; done

set -e

CONVERSATION_PATH="$1"
NUM_MESSAGES="${2:-5}"
SCRIPT_DIR="$(dirname "$0")"

if [ -z "$CONVERSATION_PATH" ]; then
    echo "Usage: monitor_session.sh <conversation_path> [num_messages]"
    echo "  conversation_path: Path to .jsonl conversation file"
    echo "  num_messages: Number of messages to display (default: 5)"
    exit 1
fi

if [ ! -f "$CONVERSATION_PATH" ]; then
    echo "Error: File not found: $CONVERSATION_PATH"
    exit 1
fi

# Extract conversation and capture output to parse the saved path
EXTRACT_OUTPUT=$(uv run python "$SCRIPT_DIR/extract_conversation.py" --minimal "$CONVERSATION_PATH" 2>&1)
echo "$EXTRACT_OUTPUT"

# Parse the actual output path from extraction script
EXTRACTED_FILE=$(echo "$EXTRACT_OUTPUT" | grep "Saved to:" | sed 's/.*Saved to: //')

if [ -z "$EXTRACTED_FILE" ] || [ ! -f "$EXTRACTED_FILE" ]; then
    echo "Error: Extraction failed - output file not found"
    exit 1
fi

# Display last N messages formatted
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Last $NUM_MESSAGES messages from: $(basename "$CONVERSATION_PATH")"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

jq -s ".[-$NUM_MESSAGES:]" "$EXTRACTED_FILE" | jq -r '.[] |
    "[\(.role | ascii_upcase)]: \(.text[0:500] // .command_marker.name // "...")\n"'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
