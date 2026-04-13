---
name: evebeauty-skill
description: 伊芙丽格医疗美容客服助手。查询机构信息、项目介绍、医生信息、术后护理等。数据来自外部源，实时更新无需修改Skill。
version: 0.1.0
alwaysApply: false
keywords:
  - 伊芙丽格
  - evebeauty
  - 医美
  - 美容
  - 痘坑修复
  - 清新微波
  - miraDry
  - 皮肤科
  - 北京医美
---

# 伊芙丽格医疗美容 · 客服助手 Skill

## 用途
当用户询问伊芙丽格医美机构的**地址、项目、医生、术后护理**等信息时，使用本 Skill 回复。

## 数据源
**所有数据来自外部，Skill 本身不包含业务数据。**

查询方式：
```bash
python scripts/fetch_info.py --query "用户问题"
```

### 数据类型自动识别
脚本会根据关键词自动判断查询类型：
- `地址/电话/营业/停车` → 机构信息
- `痘坑/清新微波/除腋/项目名` → 项目介绍  
- `吴凌燕/刘兰兰/医生名` → 医生介绍
- `术后/护理/注意事项` → 术后护理

### 手动指定类型（可选）
```bash
python scripts/fetch_info.py --query "关键词" --type doctor
```

## 回复规则

1. **必须先运行脚本**获取最新数据，不可凭记忆回复
2. **照实回复**，不可添加/删改话术
3. **找不到信息时**，回复"暂未收录该信息，请联系客服确认"
4. **脚本报错时**，回复"系统查询异常，请拨打客服热线咨询"

## 数据源配置

当前支持三种模式（修改 `data/config.json` 切换）：

### 模式 1：GitHub Raw URL（推荐）
- 数据存在 GitHub 仓库的 JSON 文件
- 脚本通过 HTTP GET 实时拉取最新版本
- 修改 JSON 提交后即刻生效

### 模式 2：本地 JSON
- 数据在 `data/info.json`
- 替换文件即可更新

### 模式 3：腾讯文档（待实现API）
- 需要腾讯文档开放平台 API 权限
- 配置 AppID/AppSecret 后可用

## 更新数据
**无需修改 Skill 文件！**
- GitHub 模式：在仓库修改 JSON 并提交
- 本地模式：替换 `data/info.json` 文件
- 腾讯文档模式：直接在表格中修改

## 示例

用户问：地址在哪？
→ 运行：`python scripts/fetch_info.py --query "地址"`
→ 读取返回结果并回复

用户问：痘坑修复怎么做的？
→ 运行：`python scripts/fetch_info.py --query "痘坑修复"`
→ 读取返回结果并回复
