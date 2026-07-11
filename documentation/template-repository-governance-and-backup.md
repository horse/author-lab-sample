# Canonical Template Repository Governance and Backup

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

`horse/author-lab-sample` 的长期身份是 Author Lab 的 canonical reference template。它不是任何真实作者项目，也不承担真实 corpus、真实研究、真实派生作者、真实运行结果或生产出版物。

## 一、长期不变量

本仓库必须长期保持：

```text
repository_mode = reference-sample
real source-author content = absent
real derived-author content = absent
real runtime results = absent
real evaluation results = absent
production publications = absent
```

允许发生的变化只有：

- 修复安全问题；
- 修复 GitHub、Python、JSON Schema 或 Actions 平台变化；
- 修复已经证实的合同缺陷；
- 补充对样板使用方式的说明；
- 经过独立 review 的必要架构改进。

不允许：

- 在 sample 仓库中启动真实作者研究；
- 把 sample 直接改成某个真实作者仓库；
- 为一个具体作者修改共享目录结构；
- 把真实受限材料、私密资料、held-out pack 或 secrets 放进 sample；
- 因为某个真实项目需要特殊规则而静默改变所有项目的 canonical template。

## 二、正确的新项目关系

```text
author-lab-sample
  = canonical reference template

Use this template
  → author-<project-slug>-lab
  → repository_mode = active-author-lab
  → independent Git history
  → independent source evidence, research, personas, runs and publications
```

每个真实作者项目都必须拥有独立仓库。真实项目可以引用 sample 的架构和文档，但不能把工作结果写回 sample。

推荐命名：

```text
author-<source-author-slug>-lab
<project-name>-author-lab
```

一个项目包含多个 source authors 时，使用项目名而不是单一作者名。

## 三、为什么使用 GitHub Template，而不是普通 clone

推荐流程：

1. 在 GitHub 中打开 `horse/author-lab-sample`；
2. 点击 `Use this template`；
3. 选择 `Create a new repository`；
4. 不选择 `Include all branches`；
5. 创建新的空历史项目仓库；
6. clone 新仓库，而不是 clone sample 后修改 remote。

Template-generated repository 的优点：

- 不继承 sample 的施工历史；
- 不会误把真实项目 commit 推回 sample；
- 新仓库从完整、干净的当前文件树开始；
- 每个项目独立配置权限、secrets、private storage 和 CI；
- sample 的未来修复不会静默进入真实项目。

Template repository 不是 package dependency。真实项目不会自动得到 sample 的后续改动。确有必要同步修复时，必须经过显式审查和迁移，而不是自动 merge。

## 四、`main` 的保护策略

Sample 的 `main` 应由 GitHub Ruleset 保护：

- Restrict deletions；
- Block force pushes；
- Require a pull request before merging；
- Require status checks to pass；
- 必须通过 `Validate Author Lab Repository`；
- Require conversation resolution；
- Require linear history；
- 禁止普通直接 push；
- bypass list 留空，或只保留一个明确的 emergency owner；
- 不允许管理员在日常变更中跳过检查。

正常改动流程：

```text
short-lived branch
→ focused PR
→ independent review
→ fresh green merge-ref CI
→ squash merge
→ verify main tree
→ delete branch
```

## 五、冻结快照

在本治理 PR 合并并通过验证后，应建立一个不可变标签：

```text
sample-v1.0.0
```

该标签表示：

```text
Author Lab canonical sample
pre-real-run execution contracts complete
reference-sample content only
```

标签必须指向治理文档已经进入 `main` 后的最终 commit，而不是此前的 `2b22e261bb9ad35b1de7bceabe9df7f7bf5ec7f8`。创建后应用 tag ruleset：

- restrict creation to owner；
- restrict update；
- restrict deletion；
- block force update；
- bypass list 为空或仅保留 emergency owner。

`main` 可以在必要时修复；`sample-v1.0.0` 永远代表这一冻结基准。

## 六、备份策略

至少保存两类备份。

### 1. 完整 Git mirror

在有 GitHub 网络访问的受信任电脑执行：

```bash
git clone --mirror https://github.com/horse/author-lab-sample.git
mv author-lab-sample.git author-lab-sample-mirror-YYYY-MM-DD.git
tar -czf author-lab-sample-mirror-YYYY-MM-DD.tar.gz \
  author-lab-sample-mirror-YYYY-MM-DD.git
shasum -a 256 author-lab-sample-mirror-YYYY-MM-DD.tar.gz \
  > author-lab-sample-mirror-YYYY-MM-DD.tar.gz.sha256
```

保存到两个独立位置，例如：

```text
encrypted local/external drive
independent cloud or object storage
```

Mirror 包含 Git objects、commits、branches 和 tags。它不完整保存 GitHub Issues、PR discussions、Actions logs、repository settings、rulesets 或 secrets。

### 2. GitHub 平台设置记录

保存：

- Template repository 是否启用；
- Ruleset 配置截图或导出；
- required status check 名称；
- repository visibility；
- default branch；
- merge policy；
- collaborator 权限；
- tag protection；
- GitHub App / Actions permissions。

这些设置不能仅靠 Git mirror 恢复。

## 七、Archive 的使用边界

不要 archive 当前 canonical template。Archive 表示仓库停止维护并进入只读状态，不适合频繁使用 `Use this template` 的长期样板。

需要真正只读档案时，可以额外建立：

```text
author-lab-sample-archive-YYYY-MM-DD
```

然后 archive 该副本；canonical `author-lab-sample` 继续保持受保护、可维护、可作为模板。

## 八、从 sample 创建真实项目后的第一批变化

新仓库必须完成以下转换：

1. 修改 project ID 与仓库说明；
2. 将 `repository_mode` 切换为 `active-author-lab`；
3. 更新 placeholder register；
4. 删除或替换 Sample source author、Sample B、Sample C 和 sample experiment；
5. 不保留 fake sample record；
6. 建立真实 source-author ID；
7. 建立 rights、storage、checksum 与 ingestion register；
8. 使用仓库外 URI 保存受限 primary source；
9. 在真实材料进入后再开展 research claims；
10. 只有 accepted claims 才能进入 approved source model；
11. 创建独立 Derived Author B/C；
12. 在分支和 PR 中完成转换；
13. 运行完整 CI；
14. 写入项目级 handoff memo，记录当前状态和下一步。

## 九、治理状态的真实性

仓库内可以记录目标设置，但只有 GitHub 实际 repository settings 才能证明它们已经启用。

因此：

- `.github/OWNER-TEMPLATE-LOCK-CHECKLIST.md` 中未勾选的项目视为未执行；
- 任何 agent 不得因为文档描述了 Ruleset 就声称 Ruleset 已启用；
- 任何 agent 不得因为文档写了 `sample-v1.0.0` 就声称 tag 已创建；
- 任何 agent 不得因为写了 backup command 就声称 mirror 已完成。

完成 owner-only 操作后，应更新 checklist，并保留可核验的日期、commit、tag 和备份 checksum。
