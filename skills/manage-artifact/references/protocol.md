# Protocol Fix Methodology

Reference for fixing protocols (CLAUDE.md behavioral patterns) using direct editing.

## Fix Tool - MANDATORY

**YOU MUST study `~/.claude/CLAUDE.md` before making protocol changes. No exceptions.**

**Before making any protocol edit, announce:** "Studying CLAUDE.md structure for protocol fix"

Protocol fixes have no dedicated tool (unlike /stage for commands or skill-creator for skills). This reference file IS your guardrail. Direct editing without understanding CLAUDE.md structure = broken behavioral patterns. Every time.

## What Protocols ARE (ADR-008)

**Protocols are NOT workflows.** This distinction is critical.

| Pattern | Definition | Key Phrase |
|---------|------------|------------|
| **Workflow** | Sequential HOW-TO instructions | "Do this, then this, then this" |
| **Protocol** | Behavioral WHEN/WHY patterns | "When X happens, apply principle Y" |

**The Trust Test:**
> "Can I trust it to figure out the steps?"
> - YES → Protocol (behavioral guidance)
> - NO → Workflow (step-by-step instructions)

**Critical insight:** Protocols define WHEN/WHY, expecting agents to determine HOW. Attempting to "workflowize" a protocol removes its adaptive power.

**Reference:** [ADR-008: Distinguish Workflows, Protocols, and Agents](https://mariuswilsch.github.io/public-wilsch-ai-pages/global/distinguish-workflows-protocols-agents-ai-systems)

## CLAUDE.md Structure (Authoritative Template)

**YOU MUST reference `~/.claude/CLAUDE.md` as THE pattern to follow.**

The user's CLAUDE.md contains these core sections:

| Section | Purpose |
|---------|---------|
| **Team Integration** | Identity, role, principles, expectations |
| **Task Lifecycle** | Phase definitions, boundaries, confidence gates |
| **Authority Model** | Investigation vs execution authority by phase |
| **Authoritative Sources** | Where truth lives (codebase, git, user, docs, hippocampus) |
| **Confidence Philosophy** | Binary ✗/✓ gating, disambiguation before action |
| **JIT Knowledge Retrieval** | On-demand truth discovery, ephemeral sessions |
| **Communication Standards** | Status updates, task completion format |

**Protocol Principle:** Each section answers WHEN/WHY, not HOW. The agent determines HOW based on the behavioral pattern.

## Protocol Fix Workflow

**YOU MUST follow this sequence. Skipping steps = broken behavioral patterns.**

1. **Announce:** "Studying CLAUDE.md structure for protocol fix"
2. **Read:** Study `~/.claude/CLAUDE.md` to understand current structure
3. **Identify failure:** What behavioral pattern is wrong or missing?
4. **Locate section:** Which CLAUDE.md section owns this behavior?
5. **Apply WHEN/WHY framing:** Write the fix as a behavioral pattern, not a workflow
6. **Test:** Verify fix across multiple scenarios (protocols need diverse verification)
7. **Iterate:** Repeat until behavioral pattern works consistently

## Common Protocol Fixes

| Failure | Likely Cause | Fix Approach |
|---------|--------------|--------------|
| Wrong authority used | Unclear phase boundaries | Clarify Authority Model section |
| Skipped confidence gate | Weak ✗/✓ enforcement | Strengthen Confidence Philosophy language |
| Used stale context | JIT retrieval not triggered | Add specific retrieval triggers to Authoritative Sources |
| Wrong communication format | Missing or unclear standard | Add/clarify Communication Standards section |
| Inconsistent phase behavior | Task Lifecycle ambiguity | Define clearer phase boundaries with WHEN conditions |

## Protocol Verification (Different from Commands/Skills)

**Protocols require diverse scenario testing.**

Unlike commands (single invocation test) or skills (workflow completion test), protocols define behavioral patterns across many situations. A single test is insufficient.

**Verification approach:**
1. Test the specific scenario that failed
2. Test 2-3 related scenarios to ensure pattern generalization
3. Test an edge case to ensure no over-correction

**Why:** Protocols are WHEN/WHY patterns. A fix that works for one scenario but breaks others is worse than no fix.

## Remember

Direct Edit tool on CLAUDE.md without studying structure = methodology bypass. Always study CLAUDE.md first. Protocols are behavioral patterns (WHEN/WHY), not workflows (HOW). Test across multiple scenarios.
