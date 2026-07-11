# Complete Repository File and Directory Guide Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task by task.

**Goal:** Add a canonical Chinese guide explaining the responsibility, authority, readers, inputs, outputs, and lifecycle of every directory and file in `author-lab-sample`, while relating the architecture to lessons learned from `holonpress/author-zhang`.

**Architecture:** Create one comprehensive reference document under `documentation/`, organized first by system concepts and then by exact repository path. Update the documentation index to make the guide discoverable. Preserve standard agent-facing filenames while explaining why descriptive long names are used elsewhere.

**Tech Stack:** Markdown, GitHub repository paths, existing Python validation and GitHub Actions.

## Global Constraints

- Every new or modified file must retain the required sample marker.
- The guide must distinguish source evidence, source-author research, compiled source models, derived-author models, harness rules, runtime configuration, work-item state, evaluations, and approved publications.
- Every tracked path in the current sample scaffold must be addressed either individually or through an explicitly enumerated repeated-structure section.
- The guide must explain what is inherited from `author-zhang`, what is corrected, and what is newly introduced.
- No source-author or derived-author file may be described as authoritative outside its declared layer.

---

### Task 1: Write the canonical repository guide

**Files:**
- Create: `documentation/complete-repository-file-and-directory-reference.md`

- [ ] Explain the relationship to `holonpress/author-zhang`.
- [ ] Explain source-of-truth direction and prohibited feedback loops.
- [ ] Explain root files and every top-level directory.
- [ ] Enumerate every nested directory and file with its intended responsibility.
- [ ] Add operational reading paths for researchers, model curators, writers, reviewers, editors, publishers, and runtime maintainers.

### Task 2: Update the documentation index

**Files:**
- Modify: `documentation/README.md`

- [ ] Add the canonical guide as the first navigation entry.
- [ ] Explain that the guide is the authoritative path-by-path reference.

### Task 3: Verify repository consistency

**Files:**
- Existing validation scripts and tests only.

- [ ] Run repository structure validation.
- [ ] Run JSON and JSONL parsing validation.
- [ ] Run sample-marker validation.
- [ ] Run work-item state validation.
- [ ] Run pytest through GitHub Actions.
