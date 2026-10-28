---
name: game-studio
description: Use the Codex Game Studios workflows and specialist roles for game development. Apply when the user asks for game-studio, CCGS, a studio role, or a workflow such as team-ui, team-qa, qa-plan, ux-review, design-system, or regression-suite.
---

# Game Studio

Use the installed Codex Game Studios snapshot under `../../game-studios/codex-game-studios/` as a catalog. The snapshot is reference material; the current user's project is the work target.

1. Run `python <this-skill-directory>/scripts/catalog.py list`, `workflow <name>`, or `role <name>` to locate the source. Read relevant sources and supporting references only.
2. Adapt source workflows to the actual project. Follow applicable user and project instructions and preserve project baselines. Paths in source documents are examples; map them to the real project.
3. Translate Claude-specific tools, commands, and model choices to available Codex capabilities. Do not assume Claude hooks are enabled. Do not impose blanket approval for work already authorized by the user.
4. Use `gs_*` specialist agents only when delegation is authorized and supported. Otherwise apply the relevant role locally. For an unpatched ephemeral Codex 0.165.0 session, if a spawn fails with `no rollout found`, retry once with `fork_turns="none"` and include all necessary context in the message. This does not give hooks a parent transcript; do not claim that it does.
5. Report actual work and distinguish automatic checks, observed input, and unverified cases.

Claude hooks are kept as reference only and are not registered by the global installer.
