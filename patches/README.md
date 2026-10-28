# Codex 0.165.0 ephemeral subagent patch

`codex-0.165.0-ephemeral-subagents.patch` targets OpenAI Codex tag `rust-v0.165.0`, commit `360319d8dee62d87e2d59fc0c21805d79519cfed`. It is a local compatibility patch, not an official OpenAI release. The original Codex source and patch context are covered by [Apache 2.0](LICENSE-APACHE-2.0).

The patch uses the live parent's existing annotated checkpoint when a full-history subagent is forked from an ephemeral parent. The parent stays ephemeral. For a live ephemeral parent, `SubagentStop` passes a null parent transcript rather than logging a failed lookup for a file that cannot exist. Normal persisted parents still use the existing storage path and preserve genuine errors. Hooks must handle the documented nullable transcript path.

Verification on 2026-10-28, Windows: `codex-core` compiled; the added ephemeral-parent regression test passed; a locally built CLI spawned the `gs_qa_tester` role with full parent context, read its role document, and ran the user's existing trusted SubagentStart and SubagentStop hooks with null parent transcript and no lookup warning. A persisted-session regression retained a non-null transcript and also completed. The full Codex test suite and other operating systems were not tested.

This patch does not automatically update the Codex app or install a binary. Apply it only to the pinned source revision, build and test it for the target environment, and keep the official installation available. Packaged CLI builds also require the matching official companion executables and resources. Updates to Codex may supersede or invalidate this patch.
