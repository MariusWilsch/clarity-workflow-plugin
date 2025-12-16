# Command/Prompt Fix Methodology

Reference for fixing prompts using the prompt engineering methodology.

## Prompt Types

This methodology covers ALL engineered prompts:

| Prompt Type | Description | Example |
|-------------|-------------|---------|
| **Slash Command** | Interactive, user-invoked via `/command` | /requirements-clarity |
| **Agent Prompt** | Autonomous, paired with code (prompt.md + index.ts) | board-digest/prompt.md |
| **Prompt Template** | Reusable prompt pattern | system prompts, instruction sets |

**Core methodology applies to all:** Anthropic template structure, iterative refinement via /stage, persuasion principles.

## Fix Tool - MANDATORY

**YOU MUST use `/stage` for ALL prompt changes. No exceptions.**

```bash
/stage {stage_number} {prompt_name}
```

**Before making any prompt edit, announce:** "Using /stage to fix {prompt_name}"

Direct editing without /stage = methodology bypass. Every time. The /stage command ensures:
- Proper Anthropic template structure
- Stage-appropriate components
- Frontmatter date versioning

## Methodology Summary

### ADR 001: Universal Prompt Engineering Principles

**10 Principles (apply progressively):**

| Principle | Core Concept |
|-----------|--------------|
| Context Before Content | Define role/task before data |
| Structure Reduces Entropy | XML tags, clear sections |
| Order Reflects Logic | Easy → Hard sequence |
| Reinforce Constraints | Repeat critical rules at boundaries |
| Separate Static/Dynamic | System = unchanging, User = variable |
| Examples > Instructions | Few-shot beats elaborate rules |
| Prevent Hallucination | Explicitly forbid invention |
| Visible Reasoning | Show work in dev, hide in prod |
| Iterative Refinement | Test → Fail → Example → Repeat |
| Explicit Output Spec | Define format, not just content |

### ADR 002: Iterative Development Methodology

**Stage Progression:**

| Stage | Time | Focus | Components |
|-------|------|-------|------------|
| Stage 1 | 1 min | MVP | Component 7 only |
| Stage 2 | 5 min | Working prototype | Components 1, 2, 7 |
| Stage 3 | 15 min | Background + rules | Components 1-5, 7 |
| Stage 4 | 30-60 min | Production | All components |

**Micro-Iteration Principle:**
- NOT: "Stage 1 failed → Add all Stage 2 components"
- YES: "Specific failure X → Add minimal Component Y to fix X"
- Stage labels are EMERGENT, not targets

### ADR 004: Slash Command Framework

**Frontmatter Format:**
```yaml
---
description: "[YYYY-MM-DD] [Stage X] Command purpose"
argument-hint: [optional argument hints]
---
```

**Anthropic Template Components:**

| # | Component | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|---|-----------|---------|---------|---------|---------|
| 1 | Task Context | ❌ | ✅ | ✅ | ✅ |
| 2 | Tone Context | ❌ | ✅ | ✅ | ✅ |
| 3 | Background Data | ❌ | ❌ | ✅ | ✅ |
| 4 | Detailed Rules | ❌ | ❌ | ✅ | ✅ |
| 5 | Examples | ❌ | ❌ | ⚠️ | ✅ |
| 6 | Conversation History | ❌ | ❌ | ⚠️ | ✅ |
| 7 | Immediate Task | ✅ | ✅ | ✅ | ✅ |
| 8 | Thinking Process | ❌ | ⚠️ | ✅ | ⚠️ |
| 9 | Output Formatting | ❌ | ❌ | ⚠️ | ✅ |
| 10 | Prefilled Response | ❌ | ❌ | ❌ | ⚠️ |

## Prompt Fix Workflow

**YOU MUST follow this sequence. Skipping steps = broken fixes.**

1. **Announce:** "Using /stage to fix {prompt_name}"
2. **Identify current stage** - Check frontmatter description (e.g., `[Stage 2]`) or infer from structure
3. **Identify failure** - What specific behavior is wrong?
4. **Invoke /stage** - `/stage {current_or_next_stage} {prompt_name}`
5. **Apply micro-iteration** - Add minimal component to fix specific failure
6. **Test** - Verify fix in new conversation (Session C)
7. **Iterate** - Repeat until working

## Template Location

Anthropic prompt template: `~/.claude/templates/anthropic-prompt-template.md`

## Common Fixes

**All fixes go through /stage. No direct editing.**

| Failure | Likely Fix | /stage Action |
|---------|------------|---------------|
| Wrong role/context | Add/update Component 1 (Task Context) | `/stage {current} {cmd}` |
| Wrong tone | Add/update Component 2 (Tone Context) | `/stage {current} {cmd}` |
| Missing domain knowledge | Add Component 3 (Background Data) | `/stage 3 {cmd}` (upgrade) |
| Skips steps | Add Component 4 (Detailed Rules) | `/stage 3 {cmd}` (upgrade) |
| Inconsistent output | Add examples (Component 5) | `/stage 3 {cmd}` (upgrade) |
| Wrong output format | Add Component 9 (Output Formatting) | `/stage 4 {cmd}` (upgrade) |

**Remember:** Direct Edit tool on prompt files = methodology bypass. Always use /stage.
