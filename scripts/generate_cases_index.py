#!/usr/bin/env python3
"""
自动生成案例索引
从 knowledge/cases/ 目录下的所有案例文件提取元数据，生成完整的索引文件
"""

import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# 证据等级定义
EVIDENCE_TIERS = {
    "A": "元分析、系统综述、官方统计、权威教材",
    "B": "同行评审论文、公开数据集、行业标准、良好文档的基准",
    "C": "结构化专家意见、内部历史数据、仔细收集的现场证据",
    "D": "LLM建议、类比、常识、非正式启发式",
    "E": "博客文章、营销文案、社交媒体、未注明来源的声称"
}

# 行业映射
INDUSTRY_MAP = {
    "支付": "fintech",
    "金融": "fintech",
    "电商": "ecommerce",
    "社交": "social",
    "内容": "content",
    "教育": "education",
    "出行": "transportation",
    "外卖": "on_demand",
    "视频": "video",
    "游戏": "gaming",
    "AI": "ai",
    "SaaS": "saas",
    "协作": "collaboration",
    "存储": "storage",
    "旅游": "travel",
    "住宿": "travel",
    "时尚": "fashion",
    "美妆": "fashion",
    "健身": "health",
    "医疗": "health",
}

# 问题类型映射
PROBLEM_MAP = {
    "获客": "acquisition",
    "增长": "acquisition",
    "冷启动": "acquisition",
    "裂变": "referral",
    "邀请": "referral",
    "留存": "retention",
    "活跃": "activation",
    "变现": "monetization",
    "付费": "monetization",
    "转化": "conversion",
}

def extract_metadata(content: str, filename: str) -> dict:
    """从案例文件提取元数据"""
    metadata = {
        "id": filename,
        "name": "",
        "file": "",
        "region": "unknown",
        "evidence_tier": "C",
        "evidence_sources": [],
        "confidence": 0.75,
        "tags": {
            "industry": [],
            "stage": [],
            "problem": [],
            "tactics": [],
            "business_model": []
        },
        "key_metrics": {},
        "summary": "",
        "replicable_points": []
    }

    lines = content.split('\n')

    # 提取标题
    for line in lines[:10]:
        if line.startswith('# ') and not line.startswith('## '):
            metadata["name"] = line[2:].strip()
            break

    # 提取基本信息表格
    in_table = False
    table_data = {}
    for i, line in enumerate(lines):
        if '| 字段 | 内容 |' in line:
            in_table = True
            continue
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3 and parts[1] and parts[1] != '字段':
                table_data[parts[1]] = parts[2]
        if in_table and not line.startswith('|'):
            break

    # 从表格提取行业
    if "行业" in table_data:
        industry_text = table_data["行业"]
        for cn, en in INDUSTRY_MAP.items():
            if cn in industry_text:
                if en not in metadata["tags"]["industry"]:
                    metadata["tags"]["industry"].append(en)

    # 从表格提取阶段
    if "阶段" in table_data:
        stage_text = table_data["阶段"]
        if "冷启动" in stage_text or "0-1" in stage_text or "初创" in stage_text:
            metadata["tags"]["stage"].append("0-1")
        if "增长" in stage_text or "1-10" in stage_text or "成长" in stage_text:
            metadata["tags"]["stage"].append("1-10")
        if "成熟" in stage_text or "10-100" in stage_text:
            metadata["tags"]["stage"].append("10-100")

    # 从表格提取标签
    if "标签" in table_data:
        tags_text = table_data["标签"]
        # 提取问题类型
        for cn, en in PROBLEM_MAP.items():
            if cn in tags_text and en not in metadata["tags"]["problem"]:
                metadata["tags"]["problem"].append(en)
        # 提取战术
        tactics = [t.strip() for t in tags_text.split(',')]
        metadata["tags"]["tactics"] = tactics[:5]

    # 提取关键数据
    for i, line in enumerate(lines):
        if '| 活跃用户' in line or '| 用户数' in line:
            parts = line.split('|')
            if len(parts) >= 3:
                metadata["key_metrics"]["users"] = parts[2].strip()
        if '| 交易' in line or '| GMV' in line:
            parts = line.split('|')
            if len(parts) >= 3:
                metadata["key_metrics"]["gmv"] = parts[2].strip()
        if '| 估值' in line or '| 市值' in line:
            parts = line.split('|')
            if len(parts) >= 3:
                metadata["key_metrics"]["valuation"] = parts[2].strip()

    # 生成摘要（从完整背景提取）
    for i, line in enumerate(lines):
        if '## 完整背景' in line:
            # 获取下一段
            if i + 2 < len(lines):
                summary_lines = []
                for j in range(i + 2, min(i + 10, len(lines))):
                    if lines[j].startswith('---') or lines[j].startswith('## '):
                        break
                    summary_lines.append(lines[j])
                if summary_lines:
                    metadata["summary"] = ''.join(summary_lines)[:200] + "..."
            break

    # 提取可复制点
    in_replicable = False
    for line in lines:
        if '## 可复制点' in line:
            in_replicable = True
            continue
        if in_replicable:
            if line.startswith('## '):
                break
            if line.startswith('### ') or line.startswith('**'):
                point = line.replace('#', '').replace('*', '').strip()
                if point and len(point) > 2:
                    metadata["replicable_points"].append(point[:50])

    # 限制可复制点数量
    metadata["replicable_points"] = metadata["replicable_points"][:5]

    return metadata

def get_region_from_path(file_path: str) -> str:
    """从文件路径推断地区"""
    if "/china/" in file_path:
        return "china"
    elif "/overseas/" in file_path:
        return "overseas"
    elif "/vertical/" in file_path:
        return "global"
    return "unknown"

def determine_evidence_tier(metadata: dict) -> str:
    """根据内容判断证据等级"""
    # 如果有公开财报、官方数据，提升等级
    if metadata.get("key_metrics"):
        if any(k in str(metadata.get("key_metrics", {})) for k in ["亿", "公开", "官方"]):
            return "B"
    return "C"

def generate_cases_index():
    """生成完整的案例索引"""
    cases_dir = BASE_DIR / "knowledge" / "cases"
    cases = []

    # 遍历所有地区
    for region in ["china", "overseas", "vertical"]:
        region_dir = cases_dir / region
        if not region_dir.exists():
            continue

        for file_path in region_dir.glob("*.md"):
            if file_path.name == "README.md":
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                filename = file_path.stem
                metadata = extract_metadata(content, filename)

                # 设置文件路径和地区
                metadata["file"] = f"cases/{region}/{file_path.name}"
                metadata["region"] = region

                # 确定证据等级
                metadata["evidence_tier"] = determine_evidence_tier(metadata)

                # 设置证据来源
                if metadata["evidence_tier"] == "B":
                    metadata["evidence_sources"] = ["公开财报", "媒体报道", "行业分析"]
                    metadata["confidence"] = 0.85
                else:
                    metadata["evidence_sources"] = ["媒体报道", "用户访谈", "行业观察"]
                    metadata["confidence"] = 0.75

                cases.append(metadata)
                print(f"✅ 处理: {metadata['name']} ({region})")
            except Exception as e:
                print(f"❌ 错误处理 {file_path}: {e}")

    return cases

def build_indexes(cases: list) -> dict:
    """构建各类索引"""
    index_by_industry = {}
    index_by_problem = {}
    index_by_tactic = {}
    index_by_stage = {}

    for case in cases:
        case_id = case["id"]

        # 按行业索引
        for industry in case["tags"].get("industry", []):
            if industry not in index_by_industry:
                index_by_industry[industry] = []
            index_by_industry[industry].append(case_id)

        # 按问题类型索引
        for problem in case["tags"].get("problem", []):
            if problem not in index_by_problem:
                index_by_problem[problem] = []
            index_by_problem[problem].append(case_id)

        # 按战术索引
        for tactic in case["tags"].get("tactics", []):
            tactic_key = tactic.lower().replace(" ", "_")[:20]
            if tactic_key not in index_by_tactic:
                index_by_tactic[tactic_key] = []
            index_by_tactic[tactic_key].append(case_id)

        # 按阶段索引
        for stage in case["tags"].get("stage", []):
            if stage not in index_by_stage:
                index_by_stage[stage] = []
            index_by_stage[stage].append(case_id)

    return {
        "index_by_industry": index_by_industry,
        "index_by_problem": index_by_problem,
        "index_by_tactic": index_by_tactic,
        "index_by_stage": index_by_stage
    }

def main():
    print("=" * 60)
    print("生成案例索引")
    print("=" * 60)

    # 生成案例列表
    cases = generate_cases_index()

    # 构建索引
    indexes = build_indexes(cases)

    # 构建完整数据结构
    output = {
        "metadata": {
            "version": "1.2.0",
            "last_updated": "2026-05-29",
            "total_cases": len(cases),
            "evidence_tier_definition": EVIDENCE_TIERS
        },
        "cases": cases,
        **indexes
    }

    # 保存索引文件
    output_path = BASE_DIR / "knowledge" / "indexes" / "cases-index.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print(f"完成! 共处理 {len(cases)} 个案例")
    print(f"输出: {output_path}")
    print("=" * 60)

    # 打印统计
    print("\n统计:")
    print(f"  行业分类: {len(indexes['index_by_industry'])} 个")
    print(f"  问题类型: {len(indexes['index_by_problem'])} 个")
    print(f"  战术分类: {len(indexes['index_by_tactic'])} 个")
    print(f"  阶段分类: {len(indexes['index_by_stage'])} 个")

if __name__ == "__main__":
    main()
