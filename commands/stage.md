---
description: "[2025-01-20] [Stage 2] Component-based prompt development using micro-iterations"
argument-hint: [stage] [command_name]
---

### 1. Task context
You are applying ADR002's micro-iteration methodology: add minimal components per specific failure, not rigid stage jumps.

**Micro-Iteration Principle:**
- Test → Specific failure → Add minimal component to fix that failure
- Stage labels (1.1, 1.2, 1.3) are valid and expected
- When components match Stage N definition, call it Stage N (emergent, not target)

### 2. Tone context
Write prompts that are clear, systematic, and follow ADR004 standards. Use proper Anthropic template components for the requested stage.

### 7. Immediate task description or request
Generate/update $2 command to Stage $1 following anthropic-prompt-template.md and ADR002 micro-iteration approach.

**Formatting Requirements:**
Always format the description field as "[YYYY-MM-DD] [Stage X] Command purpose" using the current date to enable version tracking.

### 8. Thinking step by step (MANDATORY)
You MUST use the sequential_thinking tool with exactly 2 thoughts before generating the staged prompt:

**First Thought:** Identify specific failure (if iterating)
- What specific failure occurred in testing?
- What minimal component fixes this specific failure?
- Does this component addition match a stage definition?

**Second Thought:** Plan minimal transformation
- What's the smallest change that fixes the failure?
- Which Anthropic component addresses this specific issue?
- Keep existing working components unchanged

Only after completing both thoughts, proceed to generate the staged prompt.

<prompt_template>
@~/.claude/templates/anthropic-prompt-template.md
</prompt_template>

**Symbol Reference Guide:**
- `@` - Includes file contents when command runs (provides additional context)
- `~` - Cross-system home directory path (works on both local and remote systems)

**IMPORTANT:** Never add @ references unless explicitly instructed by the user. 
These references are design decisions that require human judgment about what 
context is appropriate for each command.

**Available Paths (for human reference):**
- `@~/.claude/templates/` - Complete document templates
- `@~/.claude/patterns/` - Reusable behavioral patterns
- `~/.claude/commands/` - Command definitions

When user provides @ references in their command design, include them exactly as specified.

**Apply Anthropic's 4 Best Practices:**

1. **Be explicit with your instructions** - Provide clear, specific details about desired output
   - ❌ Bad: "Create an analytics dashboard"
   - ✅ Good: "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."

2. **Add context to improve performance** - Explain motivation behind instructions
   - ❌ Bad: "Never use ellipses"
   - ✅ Good: "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."

3. **Be vigilant with examples** - Ensure examples align with desired behaviors

4. **Respect system boundaries** - Clearly separate AI verification from human testing

Use the Anthropic template components appropriate for the requested stage per ADR002 mapping.

**Save this command as:** `~/.claude/commands/$2.md` (requires .md extension for Claude Code recognition)