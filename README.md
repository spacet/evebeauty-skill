# EveBeauty Skill - 伊芙丽格医美客服助手

> 一个兼容多平台的 AI Agent Skill，提供伊芙丽格医疗美容机构的客服查询服务。

## 兼容平台

本 Skill 基于 **SKILL.md 开放标准** 编写，兼容以下平台：

| 平台 | 兼容性 | 安装路径 | 说明 |
|------|--------|----------|------|
| **Claude Code** | ✅ 原生支持 | `~/.claude/skills/evebeauty-skill/` | SKILL.md 标准制定者 |
| **OpenClaw / Qclaw** | ✅ 原生支持 | `~/.agents/skills/evebeauty-skill/` 或 `~/.openclaw/skills/` | SKILL.md 标准采用者 |
| **Qwen Code** | ✅ 原生支持 | `~/.qwen/skills/evebeauty-skill/` | 兼容 SKILL.md 标准 |
| **OpenAI Codex** | ✅ 原生支持 | `~/.codex/skills/evebeauty-skill/` | SKILL.md 标准采用者 |
| **Cursor** | ⚙️ 需适配器 | `.cursor/rules/evebeauty.mdc` | 提供专用适配文件 |

## 功能

- 机构信息查询（地址、电话、营业时间、停车）
- 项目介绍（痘坑修复、清新微波除腋汗腋臭）
- 医生介绍（吴凌燕院长、刘兰兰主任）
- 术后护理注意事项查询

## 数据架构

**数据与 Skill 完全解耦**，所有数据来自外部源：

```
数据源 → scripts/fetch_info.py → Agent 回复
```

| 数据源 | 配置 | 更新方式 |
|--------|------|----------|
| GitHub Raw | `data_source: github` | 修改 JSON 并提交，实时同步 |
| 本地 JSON | `data_source: local` | 替换 `data/info.json` |
| 腾讯文档 | `data_source: tencent_docs` | 表格中直接修改（需 API） |

**核心优势：更新数据无需修改任何 Skill 文件。**

## 快速开始

### 1. 安装

**Claude Code / OpenClaw / Qwen Code / Codex：**
```bash
# 克隆或复制到此平台的标准 Skill 路径
git clone https://github.com/spacet/evebeauty-skill.git ~/.agents/skills/evebeauty-skill
```

**Cursor：**
```bash
# 复制适配文件到项目规则目录
cp adapters/cursor/rules/evebeauty.mdc .cursor/rules/
```

### 2. 使用

安装后，直接询问即可：
- "伊芙丽格在哪？"
- "痘坑修复怎么做的？"
- "吴凌燕医生怎么样？"
- "清新微波术后要注意什么？"

### 3. 验证

```bash
cd evebeauty-skill
python scripts/fetch_info.py --query "地址"
python scripts/fetch_info.py --query "痘坑修复"
python scripts/fetch_info.py --query "吴凌燕"
```

## 目录结构

```
evebeauty-skill/
├── SKILL.md                    ← 通用标准文件（Claude/OpenClaw/Qwen/Codex）
├── skill.json                  ← Qwen Code 专用元数据（可选）
├── README.md                   ← 本文件
├── scripts/
│   └── fetch_info.py           ← 通用查询脚本（Python 标准库）
├── data/
│   ├── config.json             ← 数据源配置
│   └── info.json               ← 示例数据
└── adapters/
    └── cursor/
        └── rules/
            └── evebeauty.mdc   ← Cursor 专用适配文件
```

## 数据格式

`data/info.json` 结构：

```json
{
  "institution": { "address": "...", "phone": "...", "hours": "..." },
  "doctors": [{ "name": "...", "title": "...", "description": "..." }],
  "projects": [{ "name": "...", "description": "..." }],
  "care_instructions": [{ "project": "...", "post_care": "..." }]
}
```

## 自定义扩展

### 添加新字段
1. 在 `data/info.json` 中添加新键值对
2. 脚本自动返回，无需修改代码
3. 如需智能查询，告诉我关键词，我更新映射

### 添加新项目/医生
在对应数组中添加对象即可，如：
```json
{
  "doctors": [...existing, { "name": "新医生", "title": "...", "description": "..." }]
}
```

## License

MIT
