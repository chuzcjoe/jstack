# J Stack

基于 [P Stack](https://github.com/cursor/plugins/tree/main/pstack) 改造的精简工程技能。目前只包含 **J Mode**，其中只有一个 **Bug Fix** 工作流。

## 使用

将 `skills/j-mode` 复制到目标项目的技能目录。例如，从本仓库根目录执行以下命令，把 `/path/to/your-project` 替换成目标项目的路径。

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R skills/j-mode /path/to/your-project/.agents/skills/
```

J Mode 自带工程规则和 Bug Fix 流程，可以独立使用。以支持 `/j-mode` 调用的 Agent 为例：

```text
/j-mode 修复这个 bug：删除最后一条记录后，列表仍然显示旧数据。
预期删除后显示空状态。请先复现，再定位根因、修复并验证。
```

## Bug Fix 流程

1. 在问题发生的界面或运行环境中复现，记录预期与实际行为。
2. 提出假设，通过运行证据排除候选原因，确认根因。
3. 做证据支持的最小修复。有低成本回归测试路径时，先看测试失败，再修复。
4. 在同一环境重跑原始复现，运行相关检查并审查最终改动。
5. 说明问题、根因、修复、验证结果和仍未确认的部分。

流程不要求额外安装 P Stack、配置指定模型或使用子代理。提交代码、开 PR 等交付动作按用户实际要求执行。

## 文件结构

```text
skills/
  j-mode/
    SKILL.md                 # J Mode 入口与工程规则
    playbooks/
      bug-fix.md             # 当前唯一的 playbook
LICENSE
README.md
```

修改 J 的 Bug Fix 流程时，编辑 [`skills/j-mode/playbooks/bug-fix.md`](skills/j-mode/playbooks/bug-fix.md)。修改工程规则时，编辑 [`skills/j-mode/SKILL.md`](skills/j-mode/SKILL.md)。

## 来源与许可

依据 P Stack `0.15.29` 的工程规则与 [Bug Fix playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md) 改写，参考日期为 2026-10-21。

遵循 [MIT License](LICENSE)，保留上游版权声明。
