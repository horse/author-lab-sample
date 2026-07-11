# Freeze Template Repository and Bootstrap New Projects Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to complete this plan and verify every repository change before merge.

**Goal:** Preserve `author-lab-sample` as a long-lived canonical sample, document the owner-only GitHub protections and backup procedure, and provide a complete prompt for starting each real Author Lab project in a separate repository.

**Architecture:** The sample remains `reference-sample` and contains no real author data. Repository-internal documentation explains governance and transition rules; each real project starts from a GitHub template-generated repository, switches to `active-author-lab`, and develops independently. GitHub settings that cannot be changed through the connected tool are recorded as explicit owner actions rather than being falsely marked complete.

**Tech Stack:** GitHub repository settings, GitHub Actions, Markdown, existing Author Lab validation suite.

## Global constraints

- Do not add real source-author materials or real persona content to `author-lab-sample`.
- Do not archive the canonical template repository while it is intended for repeated template use.
- Do not create parallel architecture versions or duplicate directory systems.
- Do not claim Template, Ruleset, tag, release, or mirror backup actions were executed when the connected GitHub tool cannot perform them.
- Keep `main` as the only normal working branch after this documentation PR is merged.
- All new Markdown files retain the reference-sample marker.

---

### Task 1: Document canonical template governance

**Files:**
- Create: `documentation/template-repository-governance-and-backup.md`
- Modify: `README.md`
- Modify: `documentation/README.md`

- [ ] Explain the permanent identity of `author-lab-sample` as a canonical reference template.
- [ ] Specify GitHub Template repository, protected `main`, immutable snapshot tag, and external mirror backup.
- [ ] Separate actions already represented in Git from owner-only GitHub settings.
- [ ] Explain why real projects must never be developed in the sample repository.

### Task 2: Add the complete new-project bootstrap prompt

**Files:**
- Create: `documentation/new-author-lab-project-bootstrap-prompt.md`

- [ ] Provide fill-in project metadata fields.
- [ ] Require the new conversation to inspect the sample repository as normative architecture only.
- [ ] Require a separate new repository created with `Use this template`.
- [ ] Require conversion from `reference-sample` to `active-author-lab` without retaining fake sample records.
- [ ] Require external storage and rights registration before source ingestion.
- [ ] Require branch/PR workflow, full CI, verification, and a durable agent handoff memo.
- [ ] Prevent changes to the sample repository and prevent model output from becoming source evidence.

### Task 3: Record owner-only GitHub operations

**Files:**
- Create: `.github/OWNER-TEMPLATE-LOCK-CHECKLIST.md`

- [ ] Record exact UI steps for enabling Template repository.
- [ ] Record exact Ruleset targets and protections for `main` and the snapshot tag.
- [ ] Record the intended snapshot tag name and the commit-selection rule.
- [ ] Record mirror backup commands and what Git mirror backup does not include.
- [ ] Leave checkboxes unchecked until the repository owner performs and verifies each UI action.

### Task 4: Record the governance milestone and verify

**Files:**
- Modify: `CHANGELOG.md`

- [ ] Record the sample-freeze and project-bootstrap documentation milestone.
- [ ] Run the complete repository validation workflow through GitHub Actions.
- [ ] Review changed files and merge only after a fresh green PR-head workflow.
- [ ] Delete the documentation branch after merge.
