# EveBeauty Skill 使用说明

## 目录结构

```
evebeauty-skill/
├── skill.json              ← Skill 元数据（几乎不变）
├── SKILL.md                ← Agent 入口指令（几乎不变）
├── README.md               ← 本文件
├── scripts/
│   └── fetch_info.py       ← 数据查询脚本
└── data/
    ├── config.json         ← 当前配置
    ├── config.example.json ← 配置示例
    ├── info.json           ← 本地数据（local模式用）
    └── 腾讯文档模板.md      ← 表格填写模板
```

## 快速开始

### 1. 当前状态（本地 JSON 模式）

数据已预装在 `data/info.json`，可直接使用：

```bash
python scripts/fetch_info.py --query "地址在哪"
python scripts/fetch_info.py --query "痘坑修复"
python scripts/fetch_info.py --query "吴凌燕"
```

### 2. 迁移到 GitHub Raw 模式（推荐）

**优势：** 改数据只需提交 GitHub，Skill 自动同步，无需改 Skill 文件。

**步骤：**

1. **创建 GitHub 仓库**
   - 新建仓库，如 `evebeauty-data`
   - 上传 `data/info.json` 到仓库根目录

2. **获取 Raw URL**
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/evebeauty-data/main/info.json
   ```

3. **修改配置**
   编辑 `data/config.json`：
   ```json
   {
     "data_source": "github",
     "github_raw_url": "https://raw.githubusercontent.com/YOUR_USERNAME/evebeauty-data/main/info.json"
   }
   ```

4. **测试**
   ```bash
   python scripts/fetch_info.py --query "地址"
   ```

**后续更新数据：**
- 在 GitHub 仓库修改 `info.json` 并提交
- Skill 自动拉取最新版本，无需任何改动

### 3. 其他数据源方案

| 方案 | 配置 | 说明 |
|------|------|------|
| 本地 JSON | `"data_source": "local"` | 替换 `info.json` 文件 |
| GitHub Raw | `"data_source": "github"` | 修改 JSON 并提交 |
| 腾讯文档 | `"data_source": "tencent_docs"` | 需 API 权限（待实现） |

## 数据格式

`info.json` 结构：

```json
{
  "institution": {
    "address": "地址",
    "phone": "电话",
    "hours": "营业时间",
    "parking": "停车信息",
    "map_search": "地图搜索关键词"
  },
  "doctors": [
    {
      "name": "医生姓名",
      "title": "职称",
      "description": "详细介绍"
    }
  ],
  "projects": [
    {
      "name": "项目名称",
      "description": "项目介绍"
    }
  ],
  "care_instructions": [
    {
      "project": "项目名称",
      "post_care": "术后注意事项"
    }
  ]
}
```

## 常见问题

### Q: 如何添加新医生/新项目？
A: 在 `info.json` 对应数组中添加对象即可，如：
```json
{
  "doctors": [
    ...existing,
    {
      "name": "新医生",
      "title": "职称",
      "description": "介绍"
    }
  ]
}
```

### Q: 地址/电话变了怎么办？
A: 修改 `institution` 对象中的对应字段，提交后即刻生效（GitHub 模式）。

### Q: 可以加新字段吗？
A: 可以。在 JSON 中添加新字段后，脚本会自动返回。如需智能查询，告诉我字段含义，我更新脚本的关键词映射。

### Q: 腾讯文档 API 什么时候能用？
A: 需要腾讯文档开放平台权限。如需对接，可联系我实现。

## 测试脚本

```bash
# 测试全部查询
python scripts/fetch_info.py --query "测试"

# 测试机构信息
python scripts/fetch_info.py --query "地址" --type institution

# 测试医生信息
python scripts/fetch_info.py --query "吴凌燕"

# 测试项目介绍
python scripts/fetch_info.py --query "痘坑"

# 测试术后护理
python scripts/fetch_info.py --query "术后" --type care
```

## 发布准备

1. 确保 `skill.json` 中信息准确
2. 上传到 GitHub 仓库
3. 用户可通过 Qwen Code 安装使用
