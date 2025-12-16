# External Tool Config Methodology

Reference for configuring external tools (GTR, uv, docker, etc.) that support Claude Code workflows.

## Key Difference

External tools don't need persuasion principles - they're configured, not instructed. The deliverable is **hippocampus documentation**, not Claude Code artifacts.

## Checklist

Follow this sequence for external tool configuration:

### 1. Investigate

Understand the tool before configuring:
- How does it work?
- What config options exist?
- Where is config stored?

Use Task agent to explore tool capabilities.

### 2. Baseline Test

Observe current behavior before changes:
- What happens now without configuration?
- Document the "before" state

### 3. Design Configuration

Work with user to determine:
- What behavior do we want?
- What tradeoffs are acceptable?
- Edge cases to handle?

### 4. Apply Configuration

Implement the configuration. Common patterns:
- Global config files (`~/.gitconfig`, `~/.config/`)
- Environment variables
- Project-level overrides

### 5. Verify Behavior

Test that configuration works:
- Create test scenario
- Compare against baseline
- Check edge cases

### 6. Document in Hippocampus

Use hippocampus skill to create documentation:
- What was configured
- How to verify/modify
- Design decisions made

Link to `[[claude-code-architecture]]` if tool enables Claude Code workflows.

## No PRE-COMMIT PAUSE Needed

Unlike Claude Code artifacts, external tools don't need session verification. The tool either works or doesn't - observable immediately.

## Example: GTR Hooks

See hippocampus: `global/gtr-global-hooks-configuration.md`
