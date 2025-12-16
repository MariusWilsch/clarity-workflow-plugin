#!/usr/bin/env python3
"""
Extract essential fields from Claude conversation JSONL files.
Reduces token count by ~6x while preserving analysis value.

COMMAND MARKER COLLAPSING:
Command markers appear as two consecutive messages:
1. Marker: Contains <command-message> and <command-name> tags
2. Template: The expanded command prompt (same timestamp)

These are collapsed into a single message with command_marker field.

TOOL RESULT HANDLING:
Different tool result types are handled as follows:
- null: Marked as {"tools": "executed"} (truly empty execution)
- string: Preserved as {"tool_output": "..."}
- list: Text items joined as {"tool_output": "..."}
- dict: Preserved as {"tool_output": "{...}"} (compact JSON)

Key: Dict outputs (TodoWrite, ExitPlanMode, etc.) are preserved,
not discarded. Storage uses compact JSON - pretty-printing happens
at display time in the labeling tool.

TOOL EXECUTION MARKER COLLAPSING:
Consecutive empty tool markers ({"tools": "executed"}) are collapsed
into a single message with tools_collapsed count to reduce noise.
"""

import json
import sys
import re
import argparse
import hashlib
from pathlib import Path

def get_message_id(extracted):
    """Generate stable hash from message content.

    Creates unique identifier from message content that survives
    re-extraction even if extraction logic changes.
    """
    content = json.dumps({
        'role': extracted.get('role'),
        'text': extracted.get('text', ''),
        'tool_output': extracted.get('tool_output', ''),
        'command_marker': extracted.get('command_marker', {})
    }, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()[:12]

def is_command_marker(text):
    """Check if message text contains command marker tags."""
    return '<command-message>' in text and '<command-name>' in text

def parse_command_info(text):
    """Extract command name and args from marker text.

    Returns: (command_name, args) or None if not a command marker
    """
    cmd_match = re.search(r'<command-name>(.*?)</command-name>', text)
    if not cmd_match:
        return None

    command_name = cmd_match.group(1)

    # Extract args if present
    args_match = re.search(r'<command-args>(.*?)</command-args>', text, re.DOTALL)
    args = args_match.group(1).strip() if args_match else ''

    return (command_name, args)

def should_include_minimal(extracted):
    """Filter for minimal extraction: keep only conversational content.

    Keeps:
    - Messages with 'text' field (user/assistant dialogue)
    - Messages with 'command_marker' field (collapsed commands)

    Removes:
    - Messages with 'tool_output' field (tool execution results)
    - Messages with only 'tools' or 'tools_collapsed' fields (tool markers)
    """
    # Remove tool execution results
    if 'tool_output' in extracted:
        return False

    # Remove tool markers
    if 'tools' in extracted or 'tools_collapsed' in extracted:
        return False

    # Keep conversational content or collapsed commands
    if 'text' in extracted or 'command_marker' in extracted:
        return True

    return False

def extract_essentials(jsonl_path, minimal=False):
    """Extract only essential fields from conversation JSONL."""

    output_lines = []
    pending_marker = None  # Track command marker waiting for template
    tool_marker_buffer = []  # Track consecutive tool execution markers

    with open(jsonl_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                obj = json.loads(line)

                # Skip summary lines
                if obj.get('type') == 'summary':
                    continue

                # Extract essential fields
                extracted = {}

                # Get message content if exists
                if 'message' in obj and obj['message']:
                    msg = obj['message']

                    # Role (user/assistant)
                    extracted['role'] = msg.get('role', 'unknown')

                    # Extract text from content (string or array format)
                    if 'content' in msg and msg['content']:
                        content = msg['content']

                        # Handle both string (v1.0.109) and array (v1.0.111+) formats
                        if isinstance(content, str):
                            # Old format: direct string
                            extracted['text'] = content
                        elif isinstance(content, list):
                            # New format: array of content objects
                            texts = []
                            for item in content:
                                if isinstance(item, dict) and 'text' in item:
                                    texts.append(item['text'])
                            if texts:
                                extracted['text'] = '\n'.join(texts)

                # Timestamp
                if 'timestamp' in obj:
                    extracted['timestamp'] = obj['timestamp']

                # Tool results (full content)
                if 'toolUseResult' in obj:
                    tool_result = obj['toolUseResult']
                    if tool_result is None:
                        # Truly empty tool execution
                        extracted['tools'] = 'executed'
                    elif isinstance(tool_result, str):
                        extracted['tool_output'] = tool_result
                    elif isinstance(tool_result, list):
                        # Extract text from tool result objects
                        tool_texts = []
                        for item in tool_result:
                            if isinstance(item, dict) and 'text' in item:
                                tool_texts.append(item['text'])
                        if tool_texts:
                            extracted['tool_output'] = '\n'.join(tool_texts)
                        else:
                            # Empty list treated as empty execution
                            extracted['tools'] = 'executed'
                    elif isinstance(tool_result, dict):
                        # Structured output - pretty-print for readability
                        extracted['tool_output'] = json.dumps(tool_result, indent=2)
                    else:
                        # Unknown type - treat as empty execution
                        extracted['tools'] = 'executed'

                # Add stable message ID (computed after all content extracted)
                extracted['_id'] = get_message_id(extracted)

                # Handle tool execution marker collapsing
                if extracted.get('tools') == 'executed':
                    # Add to buffer for consecutive tool markers
                    tool_marker_buffer.append(extracted)
                    continue  # Don't output yet, accumulate consecutive markers

                # Flush tool marker buffer if we hit a non-tool message
                if tool_marker_buffer:
                    if len(tool_marker_buffer) == 1:
                        # Single tool marker - output as-is
                        if not minimal or should_include_minimal(tool_marker_buffer[0]):
                            output_lines.append(tool_marker_buffer[0])
                    else:
                        # Multiple consecutive markers - collapse
                        collapsed = tool_marker_buffer[0].copy()
                        collapsed['tools_collapsed'] = len(tool_marker_buffer)
                        del collapsed['tools']  # Replace 'tools' with 'tools_collapsed'
                        if not minimal or should_include_minimal(collapsed):
                            output_lines.append(collapsed)
                    tool_marker_buffer = []

                # Handle command marker collapsing
                if 'text' in extracted and is_command_marker(extracted['text']):
                    # This is a command marker - save it and wait for next message (template)
                    cmd_info = parse_command_info(extracted['text'])
                    if cmd_info:
                        pending_marker = {
                            'extracted': extracted,
                            'command_name': cmd_info[0],
                            'command_args': cmd_info[1],
                            'timestamp': extracted.get('timestamp')
                        }
                        continue  # Don't output yet, wait for template

                # Check if this is the expanded template following a command marker
                if pending_marker and 'text' in extracted:
                    # Next message after marker is always the template (sequence-based)
                    # Timestamps may differ due to export timing, but sequence is guaranteed
                    collapsed = pending_marker['extracted'].copy()
                    collapsed['command_marker'] = {
                        'name': pending_marker['command_name'],
                        'args': pending_marker['command_args'],
                        'template': extracted['text']
                    }
                    # Remove the raw text field (it's now in command_marker)
                    del collapsed['text']
                    if not minimal or should_include_minimal(collapsed):
                        output_lines.append(collapsed)
                    pending_marker = None
                    continue

                # Only output if we have meaningful content
                # Note: 'tools' excluded here - tool markers handled by buffer flush only
                if 'text' in extracted or 'tool_output' in extracted:
                    if not minimal or should_include_minimal(extracted):
                        output_lines.append(extracted)

            except json.JSONDecodeError:
                print(f"Warning: Skipping invalid JSON at line {line_num}")
                continue

    # Flush any remaining tool markers at end of file
    if tool_marker_buffer:
        if len(tool_marker_buffer) == 1:
            if not minimal or should_include_minimal(tool_marker_buffer[0]):
                output_lines.append(tool_marker_buffer[0])
        else:
            collapsed = tool_marker_buffer[0].copy()
            collapsed['tools_collapsed'] = len(tool_marker_buffer)
            del collapsed['tools']
            if not minimal or should_include_minimal(collapsed):
                output_lines.append(collapsed)

    return output_lines

def main():
    parser = argparse.ArgumentParser(
        description='Extract essential fields from Claude conversation JSONL files.'
    )
    parser.add_argument('input_path', type=str,
                       help='Path to input conversation JSONL file')
    parser.add_argument('--minimal', action='store_true',
                       help='Extract only user/assistant text (exclude tool execution results)')

    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    # Create output directory
    output_dir = Path.cwd() / 'conversation_data'
    output_dir.mkdir(exist_ok=True)

    # Generate output filename
    suffix = "_minimal" if args.minimal else ""
    output_file = output_dir / f"filtered{suffix}_{input_path.name}"

    print(f"📂 Processing: {input_path.name}")
    print(f"📊 File size: {input_path.stat().st_size / 1024 / 1024:.2f} MB")
    if args.minimal:
        print(f"🎯 Mode: Minimal (conversation only)")

    # Extract essentials
    extracted = extract_essentials(input_path, minimal=args.minimal)

    # Write filtered JSONL
    with open(output_file, 'w') as f:
        for item in extracted:
            f.write(json.dumps(item) + '\n')

    print(f"✅ Extracted: {len(extracted)} messages")
    print(f"💾 Saved to: {output_file}")
    print(f"📉 New size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"🎯 Reduction: {(1 - output_file.stat().st_size / input_path.stat().st_size) * 100:.1f}%")

if __name__ == "__main__":
    main()