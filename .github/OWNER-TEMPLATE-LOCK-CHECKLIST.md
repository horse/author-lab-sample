# Owner Template Lock Checklist

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本文只记录必须由 repository owner 在 GitHub UI 或有网络访问的受信任电脑执行的操作。未勾选项目视为未完成；任何 agent 不得根据目标文档推断设置已经生效。

Repository:

```text
horse/author-lab-sample
```

## 1. Enable Template repository

GitHub UI：

```text
Repository
→ Settings
→ General
→ Template repository
```

- [ ] 已启用 `Template repository`。
- [ ] 仓库首页显示 `Use this template`。
- [ ] 使用测试账号或 owner 验证可以创建新 repository。
- [ ] 测试创建时未选择 `Include all branches`。

Verification date:

```text
not verified
```

## 2. Protect `main` with a branch ruleset

GitHub UI：

```text
Repository
→ Settings
→ Rules
→ Rulesets
→ New branch ruleset
```

Target：

```text
main
```

Required protections：

- [ ] Ruleset status = Active。
- [ ] Restrict deletions。
- [ ] Block force pushes。
- [ ] Require a pull request before merging。
- [ ] Require status checks to pass。
- [ ] Required check includes `Validate Author Lab Repository`。
- [ ] Require conversation resolution before merging。
- [ ] Require linear history。
- [ ] Direct pushes by normal collaborators are blocked。
- [ ] Bypass list is empty or contains only the documented emergency owner。
- [ ] Administrator bypass is not used for routine changes。

Ruleset name：

```text
canonical-sample-main-protection
```

Verification date:

```text
not verified
```

## 3. Merge policy

GitHub UI：

```text
Repository
→ Settings
→ General
→ Pull Requests
```

- [ ] Squash merging is enabled。
- [ ] Merge commits are disabled unless explicitly required。
- [ ] Rebase merging is disabled unless explicitly required。
- [ ] Automatically delete head branches is enabled。
- [ ] Auto-merge policy has been reviewed。

Verification date:

```text
not verified
```

## 4. Create the immutable sample snapshot tag

Create only after the template-governance PR is merged and `main` is verified.

Intended tag：

```text
sample-v1.0.0
```

Tag target：

```text
The final main commit that contains:
- template repository governance documentation;
- new-project bootstrap prompt;
- owner template lock checklist;
- successful repository CI.
```

CLI example：

```bash
git fetch origin main
git checkout main
git pull --ff-only origin main
git tag -a sample-v1.0.0 -m "Canonical Author Lab sample: pre-real-run complete"
git push origin sample-v1.0.0
```

- [ ] `sample-v1.0.0` has been created as an annotated tag。
- [ ] Tag points to the intended final main commit。
- [ ] Tag message identifies the canonical sample freeze。
- [ ] Tag is visible on GitHub。

Tag commit SHA：

```text
not created
```

Verification date:

```text
not verified
```

## 5. Protect the snapshot tag

Create a tag ruleset targeting：

```text
sample-v1.0.0
```

- [ ] Restrict tag creation after the initial owner-created tag。
- [ ] Restrict tag updates。
- [ ] Restrict tag deletion。
- [ ] Block force updates。
- [ ] Bypass list is empty or contains only the emergency owner。

Ruleset name：

```text
canonical-sample-tag-protection
```

Verification date:

```text
not verified
```

## 6. Create an external Git mirror backup

Run on a trusted computer with GitHub network access：

```bash
git clone --mirror https://github.com/horse/author-lab-sample.git
mv author-lab-sample.git author-lab-sample-mirror-YYYY-MM-DD.git
tar -czf author-lab-sample-mirror-YYYY-MM-DD.tar.gz \
  author-lab-sample-mirror-YYYY-MM-DD.git
shasum -a 256 author-lab-sample-mirror-YYYY-MM-DD.tar.gz \
  > author-lab-sample-mirror-YYYY-MM-DD.tar.gz.sha256
```

- [ ] Mirror clone completed without errors。
- [ ] Archive SHA-256 was generated。
- [ ] Archive was copied to an encrypted local or external drive。
- [ ] Archive was copied to an independent cloud/object-storage location。
- [ ] One restore or `git fsck --full` verification was performed。

Backup filename：

```text
not created
```

Backup SHA-256：

```text
not created
```

Backup locations：

```text
not recorded
```

Verification date：

```text
not verified
```

## 7. Record GitHub platform settings separately

Git mirror does not preserve every GitHub platform setting.

- [ ] Saved Template repository status。
- [ ] Saved branch ruleset configuration or screenshots。
- [ ] Saved tag ruleset configuration or screenshots。
- [ ] Saved required status check names。
- [ ] Saved repository visibility and default branch。
- [ ] Saved merge policy。
- [ ] Reviewed collaborator permissions。
- [ ] Reviewed GitHub App and Actions permissions。
- [ ] Confirmed no repository secrets were copied into documentation or backup notes。

Verification date：

```text
not verified
```

## 8. Final owner sign-off

- [ ] Canonical sample remains `reference-sample`。
- [ ] Repository contains no real source-author or derived-author data。
- [ ] `Use this template` works。
- [ ] `main` is protected。
- [ ] `sample-v1.0.0` exists and is protected。
- [ ] External mirror backup exists in two locations。
- [ ] New real projects will be created in separate repositories。

Owner：

```text
not signed
```

Sign-off date：

```text
not signed
```
