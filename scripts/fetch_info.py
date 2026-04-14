#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伊芙丽格信息查询脚本
从 references/ 目录读取 Markdown 文件返回
"""

import argparse
import os
import sys
from pathlib import Path

# 路径
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
REFS_DIR = PROJECT_ROOT / "references"


def read_markdown(path: str) -> str:
    """读取 Markdown 文件"""
    file_path = Path(path)
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def discover_services() -> list:
    """自动发现 services/ 目录下所有服务文件"""
    services_dir = REFS_DIR / "services"
    if not services_dir.exists():
        return []
    return [
        f.stem for f in services_dir.glob("*.md")
    ]


def discover_doctors() -> list:
    """自动发现 doctors/ 目录下所有医生文件"""
    doctors_dir = REFS_DIR / "doctors"
    if not doctors_dir.exists():
        return []
    return [
        f.stem for f in doctors_dir.glob("*.md")
    ]


def build_keyword_index() -> dict:
    """
    构建关键词索引
    返回: {关键词: 文件相对路径}
    """
    index = {}

    # 固定映射（兜底）
    defaults = {
        "地址": "institution.md",
        "电话": "institution.md",
        "营业": "institution.md",
        "停车": "institution.md",
        "介绍": "institution.md",
        "简介": "institution.md",
        "怎么样": "institution.md",
        "正规": "institution.md",
        "伊芙丽格": "institution.md",
        "evebeauty": "institution.md",
        "燕莎": "institution.md",
        "亮马桥": "institution.md",
        "预约": "appointment.md",
        "面诊": "appointment.md",
        "术后": "services/",  # 特殊：搜索所有服务
        "护理": "services/",
        "注意事项": "services/",
        "恢复": "services/",
        "疗程": "services/",
    }
    index.update(defaults)

    # 动态提取医生名
    for stem in discover_doctors():
        # 文件名转中文显示名（简单映射）
        name_map = {
            "wu-lingyan": "吴凌燕",
            "liu-lanlan": "刘兰兰",
        }
        display_name = name_map.get(stem, stem)
        index[display_name] = f"doctors/{stem}.md"
        index[stem] = f"doctors/{stem}.md"

    # 动态提取服务名和文件名
    services = discover_services()
    service_name_map = {
        "doukeng-xiufu": ("痘坑修复", "痘坑"),
        "qingxin-weibo": ("清新微波除腋汗腋臭", "清新微波", "除腋臭", "腋汗", "miraDry"),
    }
    for stem in services:
        file_path = f"services/{stem}.md"
        # 读取文件第一行提取服务名
        full_path = REFS_DIR / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip().lstrip("# ").strip()
                if first_line:
                    index[first_line] = file_path
        # 添加别名
        if stem in service_name_map:
            for alias in service_name_map[stem]:
                index[alias] = file_path
        index[stem] = file_path

    return index


def find_matching_files(query: str) -> list:
    """
    根据查询字符串匹配相关文件
    返回: [(文件相对路径, 匹配度), ...]
    """
    index = build_keyword_index()
    matches = []
    query_lower = query.lower()

    # 精确匹配
    for keyword, path in index.items():
        if keyword.lower() in query_lower:
            if path.endswith("/"):
                # 目录型：返回目录下所有文件
                dir_path = REFS_DIR / path.rstrip("/")
                if dir_path.exists():
                    for f in dir_path.glob("*.md"):
                        matches.append((f.relative_to(REFS_DIR), 1))
            else:
                matches.append((path, 2))  # 精确匹配权重高

    # 去重
    seen = set()
    unique = []
    for path, score in sorted(matches, key=lambda x: -x[1]):
        if path not in seen:
            seen.add(path)
            unique.append((path, score))

    return unique


def query_info(query: str) -> str:
    """
    查询信息，返回格式化结果
    """
    matches = find_matching_files(query)

    if not matches:
        # 无匹配，返回全部内容
        return _get_all_content()

    parts = []
    for path, _score in matches:
        full_path = REFS_DIR / path
        content = read_markdown(full_path)
        if content:
            parts.append(content)

    if not parts:
        return "暂未收录该信息，请联系客服确认。"

    return "\n\n---\n\n".join(parts)


def _get_all_content() -> str:
    """获取全部内容"""
    parts = []
    # 机构信息
    inst = read_markdown(REFS_DIR / "institution.md")
    if inst:
        parts.append(inst)
    # 医生
    doctors_dir = REFS_DIR / "doctors"
    if doctors_dir.exists():
        for f in sorted(doctors_dir.glob("*.md")):
            parts.append(read_markdown(f))
    # 服务
    services_dir = REFS_DIR / "services"
    if services_dir.exists():
        for f in sorted(services_dir.glob("*.md")):
            parts.append(read_markdown(f))
    # 预约
    appt = read_markdown(REFS_DIR / "appointment.md")
    if appt:
        parts.append(appt)
    return "\n\n---\n\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="伊芙丽格信息查询")
    parser.add_argument("--query", "-q", type=str, help="查询关键词")
    parser.add_argument("--list", action="store_true", help="列出所有可用服务")

    args = parser.parse_args()

    if args.list:
        print("=== 机构信息 ===")
        print("institution.md")
        print("\n=== 医生介绍 ===")
        for d in discover_doctors():
            print(f"doctors/{d}.md")
        print("\n=== 服务项目 ===")
        for s in discover_services():
            print(f"services/{s}.md")
        print("\n=== 其他 ===")
        print("appointment.md")
        return

    if not args.query:
        parser.error("必须指定 --query 或 --list")

    try:
        result = query_info(args.query)
        print(result)
    except Exception as e:
        print(f"查询失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
