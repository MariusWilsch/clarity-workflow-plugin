# Skill Fix Methodology

Reference for fixing skills using the skill-creator methodology.

## Fix Tool - MANDATORY

**YOU MUST use the `skill-creator` skill for ALL skill changes. No exceptions.**

**Before making any skill edit, announce:** "Using skill-creator to fix {skill-name}"

Direct editing without skill-creator = methodology bypass. Every time. The skill-creator ensures:
- Proper skill structure (SKILL.md, references/, scripts/, assets/)
- Progressive disclosure patterns
- Discovery phase tagging
- Best practices compliance

## Invoke skill-creator

When fixing a skill, invoke:

```
Skill(skill-creator)
```

The skill-creator provides the complete 7-step methodology:
1. Understand the skill with concrete examples
2. Determine discovery phase (requirements-clarity vs implementation-clarity)
3. Plan reusable contents (scripts, references, assets)
4. Initialize (if new) or skip to Step 5 (if existing)
5. Edit the skill
6. Package the skill
7. Iterate based on real usage

## Key Principles (from skill-creator)

- **Concise is key** - Context window is a public good
- **Progressive disclosure** - Metadata → SKILL.md → Resources (3 levels)
- **Degrees of freedom** - Match specificity to task fragility
- **Discovery timing** - Include `(discovery: X)` in description

## Skill Fix Workflow

**YOU MUST follow this sequence. Skipping steps = broken fixes.**

1. **Announce:** "Using skill-creator to fix {skill-name}"
2. **Invoke:** `Skill(skill-creator)`
3. **Follow skill-creator's 7-step process**
4. **Test:** Verify fix in new conversation
5. **Iterate:** Repeat until working

**Remember:** Direct Edit tool on skill files = methodology bypass. Always use skill-creator.
