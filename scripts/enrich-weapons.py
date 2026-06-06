#!/usr/bin/env python3
"""Regenerate all weapon docs with richer explanations, key points, and indexes."""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT_DIR = Path(__file__).resolve().parent.parent
WEAPONS_ROOT = ROOT_DIR / "knowledge" / "weapons"
CASES_INDEX_PATH = ROOT_DIR / "knowledge" / "indexes" / "cases-index.json"
WEAPONS_INDEX_PATH = ROOT_DIR / "knowledge" / "indexes" / "weapons-index.json"


@dataclass(frozen=True)
class CategoryConfig:
    directory: str
    category_id: str
    category_name: str
    stage_hint: str
    primary_goal: str
    mechanism: str
    overview: str
    theory_files: Tuple[str, ...]
    fallback_case_ids: Tuple[str, ...]
    priority_when: Tuple[str, ...]
    avoid_when: Tuple[str, ...]


CATEGORY_CONFIGS: Dict[str, CategoryConfig] = {
    "01-cold-start": CategoryConfig(
        directory="01-cold-start",
        category_id="cold-start",
        category_name="冷启动增长",
        stage_hint="0→1，优先获取前100到1000个高质量种子用户",
        primary_goal="验证需求、找到首条可复制获客路径",
        mechanism="用高接触、低规模、强反馈的动作快速缩短“产品假设 → 用户反馈 → 迭代”的循环",
        overview="01-overview.md",
        theory_files=("01-growth-hacking.md", "02-plg.md"),
        fallback_case_ids=("dropbox", "airbnb-host", "notion"),
        priority_when=(
            "产品还在 0→1 阶段，最重要的是拿到高质量前100用户。",
            "团队预算有限，但创始人或核心成员愿意亲自下场。",
            "你需要的不是规模化流量，而是真实反馈与明确的产品方向。",
        ),
        avoid_when=(
            "产品已进入规模化投放阶段，此时单点人工动作边际收益会迅速下降。",
            "团队无法持续跟进反馈闭环，导致获客后没人服务或迭代。",
            "目标是短期大规模放量，而不是验证 PMF。",
        ),
    ),
    "02-viral-referral": CategoryConfig(
        directory="02-viral-referral",
        category_id="viral-referral",
        category_name="病毒裂变",
        stage_hint="适合有明确产品价值感知和分享动机的阶段",
        primary_goal="让现有用户带来新的有效用户",
        mechanism="把用户的传播行为和用户自身收益绑定，让分享变成一种低摩擦、可感知、有回报的动作",
        overview="01-overview.md",
        theory_files=("07-viral-growth.md", "03-network-effects.md", "09-gamification.md"),
        fallback_case_ids=("dropbox", "pinduoduo-group-buy", "wechat-redpacket"),
        priority_when=(
            "产品已经有基础留存或价值时刻，用户愿意主动推荐。",
            "核心目标是降低 CAC，而不是继续堆买量预算。",
            "分享链路可以被精确追踪，且奖励成本可控。",
        ),
        avoid_when=(
            "产品核心价值还没被用户感知，强推裂变会放大差口碑。",
            "奖励设计严重亏损，新增用户质量又无法回收成本。",
            "分享动作复杂、路径中断多，导致传播意愿和转化一起下滑。",
        ),
    ),
    "03-content-growth": CategoryConfig(
        directory="03-content-growth",
        category_id="content-growth",
        category_name="内容增长",
        stage_hint="0→10 更常见，适合做可复利的长期获客",
        primary_goal="通过内容持续获取高意向自然流量",
        mechanism="围绕用户真实问题沉淀内容资产，让单次产出在搜索、社媒和分发渠道中持续复用",
        overview="01-overview.md",
        theory_files=("04-content-growth.md", "01-growth-hacking.md"),
        fallback_case_ids=("hubspot", "xiaohongshu", "tiktok"),
        priority_when=(
            "你的用户会主动搜索问题、方案、教程、对比和模板。",
            "团队愿意接受内容增长前期慢、后期复利的节奏。",
            "产品适合用知识、案例、工具或方法论建立信任。",
        ),
        avoid_when=(
            "业务窗口极短，只接受几天内立刻见效的动作。",
            "团队没有持续产出和迭代内容的能力。",
            "内容和产品价值脱节，只能带来泛流量而非有效线索。",
        ),
    ),
    "04-community": CategoryConfig(
        directory="04-community",
        category_id="community",
        category_name="社区增长",
        stage_hint="1→10 更常见，适合沉淀用户关系与身份认同",
        primary_goal="建立用户之间的互动网络和长期粘性",
        mechanism="把用户和用户之间的连接、共创与身份认同做成增长飞轮，而不只是单向运营触达",
        overview="01-overview.md",
        theory_files=("05-community-growth.md", "03-network-effects.md"),
        fallback_case_ids=("bilibili", "slack", "notion"),
        priority_when=(
            "用户之间的交流本身就会提升产品价值。",
            "你想要的不只是单次转化，而是持续活跃和自传播。",
            "团队能长期运营规则、活动、内容与核心成员关系。",
        ),
        avoid_when=(
            "用户之间几乎没有可交流的共同主题，社区会很快失活。",
            "团队只想做短期促销，没有意愿维护秩序和内容质量。",
            "产品本身没有基础价值，只想靠社区掩盖留存问题。",
        ),
    ),
    "05-plg": CategoryConfig(
        directory="05-plg",
        category_id="plg",
        category_name="产品驱动增长",
        stage_hint="适合 SaaS、工具、协作产品，也适合做规模化转化优化",
        primary_goal="让产品体验本身承担获客、激活、留存和传播的一部分职责",
        mechanism="用低摩擦体验、自然传播触点和清晰的价值时刻，把增长动作嵌进产品本身",
        overview="01-overview.md",
        theory_files=("02-plg.md", "01-growth-hacking.md"),
        fallback_case_ids=("notion", "slack", "zoom"),
        priority_when=(
            "用户可以在很短时间内体验到核心价值。",
            "产品本身有天然的协作、分享或升级路径。",
            "你想减少对销售或投放的强依赖。",
        ),
        avoid_when=(
            "产品价值必须依赖长交付、重实施或强人工服务才能体现。",
            "团队无法做埋点、实验和产品迭代，PLG 会停留在口号层。",
            "用户体验本身还不稳定，过早放大流量只会放大流失。",
        ),
    ),
    "06-retention": CategoryConfig(
        directory="06-retention",
        category_id="retention",
        category_name="留存增长",
        stage_hint="1→10 更常见，适合把已有用户留得更久、用得更深",
        primary_goal="提高复访、复用、续费和长期价值",
        mechanism="围绕关键行为、习惯形成、触达时机和用户成就感，持续把用户拉回产品价值闭环",
        overview="01-overview.md",
        theory_files=("09-gamification.md", "10-flywheel.md", "11-business-models.md"),
        fallback_case_ids=("ant-forest", "duolingo", "bilibili"),
        priority_when=(
            "你已经有一定规模用户，但大量用户用过一次就流失。",
            "业务增长瓶颈在复购、复访、习惯形成或续费。",
            "团队能明确识别关键留存行为和触发节点。",
        ),
        avoid_when=(
            "新用户获取本身就严重不足，先只做留存可能难以感知增量。",
            "产品核心价值不清晰，触达再多也只会增加骚扰感。",
            "团队没有基本的分层和行为数据，容易做成泛化群发。",
        ),
    ),
    "07-monetization": CategoryConfig(
        directory="07-monetization",
        category_id="monetization",
        category_name="变现增长",
        stage_hint="适合已经形成基础使用价值后，优化商业模式和付费路径",
        primary_goal="提升付费转化、ARPU、ARR 或整体收入质量",
        mechanism="把用户对价值的感知、付费时机和价格体系对齐，让收入增长和用户体验尽量同向",
        overview="01-overview.md",
        theory_files=("11-business-models.md", "02-plg.md"),
        fallback_case_ids=("stripe", "notion", "slack"),
        priority_when=(
            "产品已经证明有使用价值，下一步要放大商业价值。",
            "团队需要优化价格体系、升级路径或付费时机。",
            "用户分层明显，不同客群愿意为不同价值买单。",
        ),
        avoid_when=(
            "产品留存和价值时刻还没站稳，过早变现会拉低长期留存。",
            "定价和升级逻辑复杂到用户无法理解。",
            "团队只想短期提收，却没有考虑 LTV、续费和品牌信任。",
        ),
    ),
    "08-paid-ads": CategoryConfig(
        directory="08-paid-ads",
        category_id="paid-ads",
        category_name="付费广告增长",
        stage_hint="10+ 更常见，适合可量化归因和可控回收周期的业务",
        primary_goal="用预算换可控规模，并在回收模型成立后放量",
        mechanism="通过精细化人群、创意、渠道和落地页优化，把投放成本稳定转化为高质量新增",
        overview="01-overview.md",
        theory_files=("08-performance-marketing.md", "01-growth-hacking.md"),
        fallback_case_ids=("shein", "doordash", "jd-furniture-roi252"),
        priority_when=(
            "你已经知道什么用户会转化，并能监控 CAC、回收期和 ROAS。",
            "业务需要更快放大规模，而不是只靠自然流量。",
            "落地页、归因和转化事件定义已经比较清楚。",
        ),
        avoid_when=(
            "产品转化链路不稳定，投放只会放大漏斗缺陷。",
            "团队看不到真实回收，只会看到表面注册量或安装量。",
            "预算有限到无法支撑测试学习周期。",
        ),
    ),
    "09-brand": CategoryConfig(
        directory="09-brand",
        category_id="brand",
        category_name="品牌增长",
        stage_hint="10+ 更常见，适合建立长期认知、溢价和信任",
        primary_goal="提升品牌心智、口碑扩散和长期获客效率",
        mechanism="用一致的品牌叙事、可信的公共表达和情绪记忆，降低用户理解和选择成本",
        overview="01-overview.md",
        theory_files=("06-brand-growth.md", "10-flywheel.md"),
        fallback_case_ids=("glossier", "allbirds", "warby-parker"),
        priority_when=(
            "业务已经有一定规模，需要从功能竞争走向心智竞争。",
            "用户决策受信任、风格、价值观和品牌记忆影响明显。",
            "团队可以持续经营品牌资产，而不是只做一次活动。",
        ),
        avoid_when=(
            "产品基本盘还没稳定，品牌投入会缺少真实承接点。",
            "团队把品牌理解成纯视觉包装，没有叙事和体验支撑。",
            "短期业绩压力极高，无法接受品牌动作的滞后反馈。",
        ),
    ),
    "10-b2b-sales": CategoryConfig(
        directory="10-b2b-sales",
        category_id="b2b-sales",
        category_name="B2B销售增长",
        stage_hint="适合客单价较高、决策链较长、需要销售协作的业务",
        primary_goal="提高线索质量、销售转化和大客户成交效率",
        mechanism="把线索获取、价值证明、销售跟进和客户成功串成闭环，缩短决策周期并提高成单质量",
        overview="01-overview.md",
        theory_files=("11-business-models.md", "04-content-growth.md"),
        fallback_case_ids=("hubspot", "calendly", "stripe"),
        priority_when=(
            "目标客户需要多角色决策、复杂评估或较长采购流程。",
            "客单价较高，值得用销售和内容共同推动转化。",
            "你需要更稳的 SQL、Demo 和成交节奏。",
        ),
        avoid_when=(
            "产品是低客单价自助成交，重销售会拉高成本结构。",
            "没有清晰 ICP 就盲目外联，只会堆低质量线索。",
            "交付与客户成功能力跟不上成交节奏。",
        ),
    ),
}


DEFAULT_METRICS = {
    "cold-start": ("种子用户获取成本", "注册/回复转化率", "高质量反馈数量"),
    "viral-referral": ("邀请发送率", "邀请转化率", "病毒系数或分享带来的有效新增"),
    "content-growth": ("自然流量", "内容转化率", "内容带来的有效线索或注册"),
    "community": ("活跃成员数", "成员互动率", "社区带来的留存/传播贡献"),
    "plg": ("激活率", "关键功能采用率", "自传播或升级转化率"),
    "retention": ("D7/D30 留存", "关键行为完成率", "复访或续费率"),
    "monetization": ("付费转化率", "ARPU/ARPA", "升级率或收入贡献"),
    "paid-ads": ("CPA/CAC", "转化率", "ROAS/回收周期"),
    "brand": ("品牌搜索量", "直接流量/自然提及", "品牌带来的转化提升"),
    "b2b-sales": ("MQL→SQL 转化率", "Demo到成交转化率", "销售周期/平均客单价"),
}


KEY_POINT_LABELS = (
    "关键点",
    "设计要点",
    "优化要点",
    "创意要点",
    "选择标准",
    "策略",
    "策略要点",
    "使用策略",
    "关键",
)

EXECUTION_LABELS = (
    "执行方法",
    "执行流程",
    "执行要点",
    "步骤",
    "准备阶段",
    "内容设计",
    "落地页设计",
    "跟进策略",
    "关键词策略",
    "出价策略",
    "账户结构",
    "优化方向",
    "创意策略",
    "策划流程",
    "升级路径",
    "收入模式",
    "设计方式",
    "合作方式",
    "制作要点",
)

METRIC_LABELS = ("关键指标",)
CASE_LABELS = ("案例",)
USE_LABELS = ("适用场景", "使用场景", "适用产品")

THEORY_LABELS = {
    "01-growth-hacking.md": "增长黑客派",
    "02-plg.md": "PLG",
    "03-network-effects.md": "网络效应",
    "04-content-growth.md": "内容增长",
    "05-community-growth.md": "社区增长",
    "06-brand-growth.md": "品牌驱动",
    "07-viral-growth.md": "病毒传播",
    "08-performance-marketing.md": "付费广告",
    "09-gamification.md": "游戏化",
    "10-flywheel.md": "增长飞轮",
    "11-business-models.md": "商业模型",
    "12-growthhackers.md": "GrowthHackers",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_front_matter(path: Path) -> Dict[str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}

    payload: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        payload[key.strip()] = value.strip()
    return payload


def parse_overview_sections(path: Path) -> Dict[int, Dict[str, object]]:
    content = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^###\s+(\d+)\.\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(content))
    result: Dict[int, Dict[str, object]] = {}

    for index, match in enumerate(matches):
        weapon_id = int(match.group(1))
        name = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        block = content[start:end].strip()
        fenced = re.search(r"```(?:\w+)?\n(.*?)\n```", block, re.DOTALL)
        if fenced:
            block = fenced.group(1).strip()
        intro, fields = parse_labeled_block(block)
        result[weapon_id] = {
            "name": name,
            "intro": intro,
            "fields": fields,
        }
    return result


def parse_labeled_block(block: str) -> Tuple[List[str], List[Tuple[str, List[str]]]]:
    intro: List[str] = []
    fields: List[Tuple[str, List[str]]] = []
    current_label: Optional[str] = None
    current_lines: List[str] = []

    def flush():
        nonlocal current_label, current_lines
        if current_label:
            while current_lines and not current_lines[-1].strip():
                current_lines.pop()
            fields.append((current_label, current_lines[:]))
        current_label = None
        current_lines = []

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped == "```":
            continue
        if not stripped:
            if current_label and current_lines and current_lines[-1] != "":
                current_lines.append("")
            elif not current_label and intro and intro[-1] != "":
                intro.append("")
            continue

        standalone_label = re.match(r"^([^：:]{1,24})[：:]$", stripped)
        inline_label = re.match(r"^([^：:]{1,24})[：:]\s*(.+)$", stripped)

        if standalone_label:
            flush()
            current_label = standalone_label.group(1).strip()
            continue
        if inline_label and not stripped.startswith("-"):
            flush()
            current_label = inline_label.group(1).strip()
            current_lines = [inline_label.group(2).strip()]
            continue

        if current_label:
            current_lines.append(stripped)
        else:
            intro.append(stripped)

    flush()
    return intro, fields


def strip_bullet_prefix(text: str) -> str:
    return re.sub(r"^[-*]\s+|^\d+[.)]\s*", "", text).strip()


def markdown_link(label: str, relative_target: str) -> str:
    return f"[{label}](<{relative_target}>)"


def relative_doc_link(from_file: Path, target: Path) -> str:
    import os

    return Path(os.path.relpath(target, start=from_file.parent)).as_posix()


def build_case_lookup(case_payload: Dict) -> Dict[str, Dict]:
    return {case["id"]: case for case in case_payload.get("cases", [])}


def find_case_by_name(case_payload: Dict, raw_name: str) -> Optional[Dict]:
    normalized = raw_name.strip().lower()
    normalized = re.sub(r"[：:（(].*$", "", normalized).strip()
    for case in case_payload.get("cases", []):
        case_name = case["name"].lower()
        case_id = case["id"].lower()
        if normalized and (normalized in case_name or normalized in case_id):
            return case
    return None


def case_summary(case: Dict) -> str:
    tactics = "、".join(case.get("tags", {}).get("tactics", [])[:2])
    stage = " / ".join(case.get("tags", {}).get("stage", [])[:1])
    industry = "、".join(case.get("tags", {}).get("industry", [])[:1])
    details = []
    if tactics:
        details.append(tactics)
    if industry:
        details.append(industry)
    if stage:
        details.append(stage)
    if details:
        return " · ".join(details)
    return f"{case.get('region', 'unknown')} · {case.get('evidence_tier', 'N/A')}级证据"


def find_case_matches(
    case_payload: Dict,
    category_config: CategoryConfig,
    fields: List[Tuple[str, List[str]]],
    fallback_lookup: Dict[str, Dict],
) -> List[Dict]:
    matches: List[Dict] = []
    seen = set()
    for label, lines in fields:
        if label not in CASE_LABELS:
            continue
        for line in lines:
            candidate = find_case_by_name(case_payload, strip_bullet_prefix(line))
            if candidate and candidate["id"] not in seen:
                matches.append(candidate)
                seen.add(candidate["id"])
    for fallback_id in category_config.fallback_case_ids:
        candidate = fallback_lookup.get(fallback_id)
        if candidate and candidate["id"] not in seen:
            matches.append(candidate)
            seen.add(candidate["id"])
        if len(matches) >= 3:
            break
    return matches[:3]


def first_non_empty(fields: List[Tuple[str, List[str]]], wanted_labels: Tuple[str, ...]) -> List[str]:
    for label, lines in fields:
        if label in wanted_labels and any(line.strip() for line in lines):
            return [line for line in lines if line.strip()]
    return []


def collect_candidate_points(fields: List[Tuple[str, List[str]]], labels: Tuple[str, ...]) -> List[str]:
    points: List[str] = []
    for label, lines in fields:
        if label not in labels:
            continue
        for line in lines:
            cleaned = strip_bullet_prefix(line)
            if cleaned:
                points.append(cleaned)
    return points


def unique_keep_order(items: List[str], limit: int) -> List[str]:
    result: List[str] = []
    seen = set()
    for item in items:
        key = item.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(key)
        if len(result) >= limit:
            break
    return result


def build_key_points(
    name: str,
    category_config: CategoryConfig,
    fields: List[Tuple[str, List[str]]],
) -> List[str]:
    candidates = []
    tactic_line = first_non_empty(fields, ("战术",))
    if tactic_line:
        candidates.append(f"{name} 的核心不是“多做一个动作”，而是 {tactic_line[0]}。")

    candidates.extend(collect_candidate_points(fields, KEY_POINT_LABELS))
    candidates.extend(collect_candidate_points(fields, EXECUTION_LABELS))
    if len(candidates) < 4:
        candidates.extend(collect_candidate_points(fields, METRIC_LABELS))
    candidates.append(f"判断是否值得持续投入，要回到 {category_config.primary_goal} 这个目标，而不是只看表面热度。")
    candidates.append(f"这类玩法最有效的前提，是团队能持续执行并围绕 {category_config.mechanism} 做复盘。")
    candidates.extend(
        [
            "先把最小可执行闭环跑通，再决定是否值得做产品化和规模化投入。",
            "优先关注真正反映业务价值的指标，而不是只看表面曝光或互动。",
            "先找出这类玩法成立的前提条件，再判断是否值得大规模复制。",
        ]
    )
    return unique_keep_order(candidates, 5)


def build_execution_steps(fields: List[Tuple[str, List[str]]], category_config: CategoryConfig) -> List[str]:
    steps = collect_candidate_points(fields, EXECUTION_LABELS)
    if steps:
        return unique_keep_order(steps, 5)
    return [
        f"先确认这次动作要解决的核心问题是否真的是“{category_config.primary_goal}”。",
        "把触发场景、执行动作和用户回流路径设计成一条最短闭环。",
        "先用小范围实验验证，再决定是否加预算、加人力或做产品化投入。",
    ]


def build_metric_lines(fields: List[Tuple[str, List[str]]], category_config: CategoryConfig) -> List[str]:
    metrics = collect_candidate_points(fields, METRIC_LABELS)
    if metrics:
        return unique_keep_order(metrics, 6)
    return list(DEFAULT_METRICS[category_config.category_id])


def build_use_context(fields: List[Tuple[str, List[str]]], category_config: CategoryConfig) -> List[str]:
    contexts = collect_candidate_points(fields, USE_LABELS)
    if contexts:
        return unique_keep_order(contexts, 4)
    return []


def build_core_explanation(
    name: str,
    description: str,
    category_config: CategoryConfig,
    intro_lines: List[str],
    fields: List[Tuple[str, List[str]]],
) -> List[str]:
    paragraphs = [
        f"{name} 是“{category_config.category_name}”模块中的典型玩法，通常用来 {category_config.primary_goal}。"
        f"它的价值不在于单个动作本身，而在于 {category_config.mechanism}。",
        f"如果只把它理解成“{description}”，很容易停留在表层执行；真正要做的是把触发时机、用户动机、执行摩擦和回收指标设计成一条闭环。",
    ]
    if intro_lines:
        paragraphs.append(" ".join(intro_lines))
    tactic_line = first_non_empty(fields, ("战术",))
    if tactic_line:
        paragraphs.append(f"在这个玩法里，最重要的策略定位是：{tactic_line[0]}。")
    return paragraphs


def format_lines(lines: List[str]) -> List[str]:
    formatted: List[str] = []
    for line in lines:
        if not line:
            if formatted and formatted[-1] != "":
                formatted.append("")
            continue
        if re.match(r"^[-*]\s+", line) or re.match(r"^\d+[.)]\s+", line):
            formatted.append(line)
        else:
            formatted.append(line)
    while formatted and not formatted[-1].strip():
        formatted.pop()
    return formatted


def render_field_sections(fields: List[Tuple[str, List[str]]]) -> List[str]:
    rendered: List[str] = []
    for label, lines in fields:
        if not lines:
            continue
        rendered.append(f"### {label}")
        rendered.extend(format_lines(lines))
        rendered.append("")
    if rendered and not rendered[-1]:
        rendered.pop()
    return rendered


def build_theory_links(category_config: CategoryConfig, weapon_path: Path) -> List[str]:
    links = []
    for theory_file in category_config.theory_files:
        theory_path = WEAPONS_ROOT / "11-referencs" / theory_file
        label = THEORY_LABELS.get(theory_file, theory_path.stem)
        links.append(f"- {markdown_link(label, relative_doc_link(weapon_path, theory_path))}")
    return links


def build_related_weapon_links(weapon_records: List[Dict], current_index: int, weapon_path: Path, overview_path: Path) -> List[str]:
    links: List[str] = []
    current = weapon_records[current_index]
    if current_index > 0:
        prev_record = weapon_records[current_index - 1]
        links.append(
            f"- 上一玩法：{markdown_link(prev_record['name'], relative_doc_link(weapon_path, ROOT_DIR / 'knowledge' / prev_record['file']))}"
        )
    if current_index + 1 < len(weapon_records):
        next_record = weapon_records[current_index + 1]
        links.append(
            f"- 下一玩法：{markdown_link(next_record['name'], relative_doc_link(weapon_path, ROOT_DIR / 'knowledge' / next_record['file']))}"
        )
    links.append(f"- 模块总览：{markdown_link('返回本模块', relative_doc_link(weapon_path, overview_path))}")
    links.append(f"- 武器库导航：{markdown_link('返回武器库首页', relative_doc_link(weapon_path, WEAPONS_ROOT / 'index.md'))}")
    return links


def render_weapon_doc(
    weapon: Dict,
    category_config: CategoryConfig,
    overview_entry: Dict[str, object],
    case_matches: List[Dict],
    category_weapons: List[Dict],
) -> str:
    weapon_path = ROOT_DIR / "knowledge" / weapon["file"]
    overview_path = WEAPONS_ROOT / category_config.directory / category_config.overview
    current_index = next(index for index, item in enumerate(category_weapons) if item["id"] == weapon["id"])
    intro_lines = overview_entry.get("intro", [])
    fields = overview_entry.get("fields", [])

    key_points = build_key_points(weapon["name"], category_config, fields)
    execution_steps = build_execution_steps(fields, category_config)
    metrics = build_metric_lines(fields, category_config)
    contexts = build_use_context(fields, category_config)
    core_paragraphs = build_core_explanation(
        weapon["name"],
        weapon.get("description", ""),
        category_config,
        intro_lines,
        fields,
    )

    lines = [
        "---",
        f"id: {weapon['id']}",
        f"name: {weapon['name']}",
        f"category: {category_config.category_name}",
        f"category_id: {category_config.category_id}",
        f"description: {weapon.get('description', '')}",
        "---",
        "",
        f"# {weapon['id']}. {weapon['name']}",
        "",
        f"> {weapon.get('description', '')}",
        "",
        "## 玩法定位",
        "",
        f"- 所属模块：{markdown_link(category_config.category_name, relative_doc_link(weapon_path, overview_path))}",
        f"- 适用阶段：{category_config.stage_hint}",
        f"- 核心目标：{category_config.primary_goal}",
        f"- 难度 / 影响 / 证据：{weapon.get('effort', 'N/A')} / {weapon.get('impact', 'N/A')} / {weapon.get('evidence_tier', 'N/A')}级",
        "",
        "## 核心讲解",
        "",
    ]

    for paragraph in core_paragraphs:
        lines.append(paragraph)
        lines.append("")

    lines.extend(
        [
            "## 关键要点",
            "",
        ]
    )
    for point in key_points:
        lines.append(f"- {point}")
    lines.extend(["", "## 深入讲解", ""])
    lines.extend(render_field_sections(fields))

    lines.extend(["", "## 执行要点", ""])
    for index, step in enumerate(execution_steps, 1):
        lines.append(f"{index}. {step}")

    lines.extend(["", "## 适用判断", "", "### 优先使用", ""])
    for item in unique_keep_order(list(contexts) + list(category_config.priority_when), 4):
        lines.append(f"- {item}")
    lines.extend(["", "### 暂不优先", ""])
    for item in category_config.avoid_when:
        lines.append(f"- {item}")

    lines.extend(["", "## 关键指标", ""])
    for metric in metrics:
        lines.append(f"- {metric}")

    lines.extend(["", "## 案例索引", ""])
    for case in case_matches:
        case_path = ROOT_DIR / "knowledge" / case["file"]
        lines.append(
            f"- {markdown_link(case['name'], relative_doc_link(weapon_path, case_path))}：{case_summary(case)}"
        )

    lines.extend(["", "## 相关索引", "", "### 理论", ""])
    lines.extend(build_theory_links(category_config, weapon_path))
    lines.extend(["", "### 关联玩法", ""])
    lines.extend(build_related_weapon_links(category_weapons, current_index, weapon_path, overview_path))

    lines.extend(["", "### 继续查阅", ""])
    lines.append(
        f"- 案例库入口：{markdown_link('查看全部增长案例', relative_doc_link(weapon_path, ROOT_DIR / 'knowledge' / 'cases' / 'README.md'))}"
    )
    lines.append(
        f"- 武器库入口：{markdown_link('查看全部增长玩法', relative_doc_link(weapon_path, WEAPONS_ROOT / 'index.md'))}"
    )
    lines.append("")
    return "\n".join(lines)


def build_weapon_records() -> Tuple[List[Dict], Dict[int, Dict]]:
    payload = load_json(WEAPONS_INDEX_PATH)
    by_id = {int(item["id"]): item for item in payload.get("weapons", [])}
    records: List[Dict] = []
    for path in sorted(WEAPONS_ROOT.glob("**/weapons/*.md")):
        front_matter = parse_front_matter(path)
        weapon_id = int(front_matter["id"])
        category_dir = path.parent.parent.name
        config = CATEGORY_CONFIGS[category_dir]
        index_item = by_id.get(weapon_id, {})
        record = {
            "id": weapon_id,
            "name": front_matter.get("name", index_item.get("name", path.stem)),
            "description": front_matter.get("description", index_item.get("description", "")),
            "effort": index_item.get("effort", "N/A"),
            "impact": index_item.get("impact", "N/A"),
            "evidence_tier": index_item.get("evidence_tier", "N/A"),
            "category_id": config.category_id,
            "category_name": config.category_name,
            "file": path.relative_to(ROOT_DIR / "knowledge").as_posix(),
        }
        records.append(record)
    return records, by_id


def main():
    case_payload = load_json(CASES_INDEX_PATH)
    weapon_records, _ = build_weapon_records()
    case_lookup = build_case_lookup(case_payload)

    overview_cache = {
        directory: parse_overview_sections(WEAPONS_ROOT / directory / config.overview)
        for directory, config in CATEGORY_CONFIGS.items()
    }

    by_category: Dict[str, List[Dict]] = {}
    for weapon in weapon_records:
        by_category.setdefault(weapon["category_id"], []).append(weapon)

    for category_weapons in by_category.values():
        category_weapons.sort(key=lambda item: item["id"])

    for weapon in weapon_records:
        path = ROOT_DIR / "knowledge" / weapon["file"]
        category_dir = path.parent.parent.name
        config = CATEGORY_CONFIGS[category_dir]
        overview_entry = overview_cache[category_dir].get(weapon["id"])
        if not overview_entry:
            raise ValueError(f"Missing overview entry for weapon {weapon['id']} in {category_dir}")
        case_matches = find_case_matches(case_payload, config, overview_entry["fields"], case_lookup)
        content = render_weapon_doc(
            weapon=weapon,
            category_config=config,
            overview_entry=overview_entry,
            case_matches=case_matches,
            category_weapons=by_category[config.category_id],
        )
        path.write_text(content + "\n", encoding="utf-8")

    print(f"Enriched {len(weapon_records)} weapon docs")


if __name__ == "__main__":
    main()
