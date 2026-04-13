#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伊芙丽格信息查询脚本
支持多种数据源：GitHub Raw URL / 本地JSON / 腾讯文档API
"""

import json
import argparse
import sys
import os
from pathlib import Path

try:
    import urllib.request
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

# 配置文件路径
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / "data" / "config.json"


def load_config():
    """加载配置"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_FILE}")
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def fetch_from_github_raw(url: str) -> dict:
    """从 GitHub Raw URL 获取数据"""
    if not HAS_URLLIB:
        raise ImportError("urllib 模块不可用")
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'EveBeauty-Skill/1.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_data = response.read().decode('utf-8')
            return json.loads(raw_data)
    except urllib.error.HTTPError as e:
        raise ConnectionError(f"GitHub Raw URL 请求失败: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"无法访问 GitHub Raw URL: {e.reason}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")


def fetch_from_local_json(data_file: str) -> dict:
    """从本地JSON文件读取"""
    data_path = PROJECT_ROOT / "data" / data_file
    if not data_path.exists():
        raise FileNotFoundError(f"数据文件不存在: {data_path}")
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def fetch_from_tencent_docs(config: dict) -> dict:
    """
    从腾讯文档读取数据
    需要腾讯文档开放平台 API 权限
    """
    raise NotImplementedError(
        "腾讯文档API需要额外配置。\n"
        "请切换到 GitHub Raw 或本地JSON模式。"
    )


def query_info(query_type: str, keyword: str = None, config: dict = None):
    """
    查询信息
    
    Args:
        query_type: 查询类型 (institution/doctor/project/care/all)
        keyword: 关键词
        config: 配置字典
    """
    if config is None:
        config = load_config()
    
    data_source = config.get("data_source", "local")
    
    # 根据数据源获取数据
    if data_source == "github":
        github_url = config.get("github_raw_url")
        if not github_url:
            raise ValueError("配置中未设置 github_raw_url")
        data = fetch_from_github_raw(github_url)
    elif data_source == "tencent_docs":
        data = fetch_from_tencent_docs(config)
    else:  # local
        data_file = config.get("data_file", "info.json")
        data = fetch_from_local_json(data_file)
    
    # 根据query_type筛选
    if query_type != "all" and query_type in data:
        result = data[query_type]
    else:
        result = data  # 返回全部
    
    # 如果有keyword，进一步筛选
    if keyword:
        if isinstance(result, list):
            result = [
                item for item in result 
                if keyword.lower() in json.dumps(item, ensure_ascii=False).lower()
            ]
        elif isinstance(result, dict):
            # 对于字典，先查值，如果没匹配则返回原字典（机构信息通常全部返回）
            matched = {
                k: v for k, v in result.items() 
                if keyword.lower() in k.lower() or keyword.lower() in str(v).lower()
            }
            if matched:  # 有匹配才返回，否则保留原结果
                result = matched
    
    return result


def format_output(data, query_type: str) -> str:
    """格式化输出"""
    if isinstance(data, list):
        if not data:
            return "未找到相关信息。"
        parts = []
        for item in data:
            if isinstance(item, dict):
                # 对字典，格式化输出每个键值对
                parts.append("\n".join(f"{k}: {v}" for k, v in item.items() if v))
            else:
                parts.append(str(item))
        return "\n\n---\n\n".join(parts)
    elif isinstance(data, dict):
        # 检查值是否是列表（如 projects/doctors），需要展开
        parts = []
        for k, v in data.items():
            if isinstance(v, list):
                # 列表类型，展开每个项目
                for item in v:
                    if isinstance(item, dict):
                        parts.append(f"{k}:\n" + "\n".join(f"  {ik}: {iv}" for ik, iv in item.items() if iv))
                    else:
                        parts.append(f"{k}: {item}")
            else:
                parts.append(f"{k}: {v}")
        return "\n\n".join(parts)
    return str(data)


def main():
    parser = argparse.ArgumentParser(description="伊芙丽格信息查询")
    parser.add_argument("--query", "-q", type=str, required=True, help="查询类型或关键词")
    parser.add_argument("--type", "-t", type=str, 
                        choices=["institution", "doctor", "project", "care", "all"], 
                        help="查询类型", default=None)
    parser.add_argument("--config", "-c", type=str, help="配置文件路径", default=None)
    
    args = parser.parse_args()
    
    try:
        # 自动判断查询类型
        query_type = args.type
        if not query_type:
            # 根据关键词自动判断
            auto_mapping = {
                "地址": "institution",
                "电话": "institution",
                "营业": "institution",
                "停车": "institution",
                "痘坑": "project",
                "清新微波": "project",
                "除腋": "project",
                "吴凌燕": "doctor",
                "刘兰兰": "doctor",
                "术后": "care",
                "护理": "care"
            }
            for kw, qtype in auto_mapping.items():
                if kw in args.query:
                    query_type = qtype
                    break
            else:
                query_type = "all"
        
        config = None
        if args.config:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        result = query_info(query_type, args.query, config)
        output = format_output(result, query_type)
        print(output)
        
    except Exception as e:
        print(f"查询失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
