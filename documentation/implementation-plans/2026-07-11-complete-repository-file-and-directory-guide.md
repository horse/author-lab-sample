# Complete Repository File and Directory Guide Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task by task.

**Goal:** Add a canonical Chinese operations guide explaining the responsibility, authority, readers, inputs, outputs, and lifecycle of every directory and file in `author-lab-sample`.

**Architecture:** Treat the current `author-lab-sample` directory architecture as the normative design. Create one comprehensive reference document under `documentation/`, organized first by the repository's own data flow and then by exact path. Update the documentation index so agents and human maintainers can find the guide before modifying the repository.

**Tech Stack:** Markdown, GitHub repository paths, existing Python validation and GitHub Actions.

## Global Constraints

- Every new or modified file must retain the required sample marker.
- The guide must distinguish source evidence, source-author research, compiled source models, derived-author models, harness rules, runtime configuration, work-item state, evaluations, and approved publications.
- Every tracked path in the current sample scaffold must be addressed either individually or through an explicitly enumerated repeated-structure section.
- `holonpress/author-zhang` may be mentioned only as background for understanding the kind of writing system being generalized; it is not the normative structure and must not control the new guide.
- The guide must explain the work that should be performed inside the new architecture, including who reads and writes each layer, what may flow downstream, and what must never flow upstream.
- No source-author or derived-author file may be described as authoritative outside its declared layer.

---

### Task 1: Write the canonical repository operations guide

**Files:**
- Create: `documentation/complete-repository-file-and-directory-reference.md`

- [x] Explain the repository's own one-way data flow and authority hierarchy.
- [x] Explain root files and every top-level directory.
- [x] Enumerate every nested directory and file with its intended responsibility.
- [x] For each layer, state who reads it, who may write it, its upstream inputs, downstream outputs, and prohibited uses.
- [x] Add operational reading paths for source curators, researchers, source-model curators, derived-author designers, writers, factual reviewers, style reviewers, editors, publishers, runtime maintainers, and repository maintainers.
- [x] Explain how a new source author, a new derived author, a new work item, and a new publication should be added.

### Task 2: Update the documentation index

**Files:**
- Modify: `documentation/README.md`

- [x] Add the canonical guide as the first navigation entry.
- [x] Explain that the guide is the authoritative path-by-path and workflow reference.

### Task 3: Verify repository consistency

**Files:**
- Existing validation scripts and tests only.

- [x] Run repository structure validation.
- [x] Run JSON and JSONL parsing validation.
- [x] Run sample-marker validation.
- [x] Run work-item state validation.
- [x] Run pytest through GitHub Actions.

## Verification result

GitHub Actions workflow `Validate Author Lab Repository`, run 4, completed successfully with every validation and pytest step passing.
