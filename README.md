# EveBeauty Skill - 伊芙丽格医美客服助手

> 一个兼容多平台的 AI Agent Skill，提供伊芙丽格医疗美容机构的客服查询服务。
> 数据以 Markdown 文件管理，新增服务/医生只需新建文件，无需修改 Skill 代码。

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

- 机构信息查询（地址、电话、营业时间、停车、机构介绍）
- 服务项目查询（痘坑修复、清新微波除腋汗腋臭等，每个服务独立文件）
- 医生介绍（吴凌燕院长、刘兰兰主任）
- 预约面诊流程
- 术后护理注意事项

## 数据架构

**数据与 Skill 完全解耦**，所有数据为 `references/` 目录下的 Markdown 文件：

```
references/
├── institution.md              ← 机构信息
├── appointment.md              ← 预约面诊
├── doctors/
│   ├── wu-lingyan.md           ← 吴凌燕院长
│   └── liu-lanlan.md           ← 刘兰兰主任
└── services/
    ├── doukeng-xiufu.md        ← 痘坑修复
    ├── qingxin-weibo.md        ← 清新微波
    └── ...                     ← 每个服务一个文件
```

**核心优势：**
- ✅ Markdown 格式，自然语言编写，无需 JSON 格式
- ✅ 每个服务/医生独立文件，编辑互不干扰
- ✅ 支持任意复杂结构（标题、列表、表格）
- ✅ Agent 天然能读，LLM 最熟悉的格式
- ✅ 新增 = 新建文件，零代码改动

## 快速开始

### 1. 安装

**Claude Code / OpenClaw / Qwen Code / Codex：**
```bash
git clone https://github.com/spacet/evebeauty-skill.git ~/.agents/skills/evebeauty-skill
```

**Cursor：**
```bash
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
python scripts/fetch_info.py --list    # 列出所有服务
```

## 添加新服务

1. 在 `references/services/` 下新建 `.md` 文件，如 `remaji.md`
2. 用 Markdown 格式写入服务信息（简介、适应症、禁忌、疗程、术后护理等）
3. 提交即可，脚本自动发现

**示例文件：**
```markdown
# 热玛吉

## 简介
...

## 适应症
- ...

## 禁忌
- ...

## 疗程
...

## 术后护理
...
```

## 自定义扩展

- **添加新医生**：在 `references/doctors/` 下新建文件
- **添加新服务**：在 `references/services/` 下新建文件
- **修改内容**：直接编辑对应 Markdown 文件

**更新数据无需修改任何 Skill 代码。**

## License

MIT
