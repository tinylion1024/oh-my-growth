# 案例结构化规范

## 概述

为了便于Agent检索和引用，所有案例需要遵循统一的结构化格式。

## 标准格式

每个案例文件应包含：

```markdown
---
id: case-id
name: 案例名称
region: china|overseas|global
industry: [行业标签]
stage: [阶段标签]
problem_types: [问题类型标签]
tactics: [玩法标签]
timeframe: 时间范围
key_metrics:
  metric_name: 数值
summary: 一句话摘要
replicable_points: [可复制点列表]
warnings: [注意事项列表]
---

# 案例标题

## 完整背景

[公司/产品介绍、行业背景、发展阶段]

## 核心挑战

[面临的主要增长问题]

## 增长策略

[具体采用的策略和方法]

### 策略一：[名称]
[详细描述]

### 策略二：[名称]
[详细描述]

## 关键数据

| 指标 | 数值 | 说明 |
|------|------|------|
| 用户数 | X亿 | 时间点 |
| 增长率 | X% | 时间段 |
| 其他 | ... | ... |

## 核心洞察

[深层规律总结]

## 可复制点

1. [点一]：[详细说明]
2. [点二]：[详细说明]
3. [点三]：[详细说明]

## 常见误区

- [误区一]：[说明]
- [误区二]：[说明]

## 关键成功因素

1. [因素一]
2. [因素二]

## 后续演进

[发展方向和未来规划]

## 相关案例

- [[相关案例1]]
- [[相关案例2]]
```

## 标签规范

### 行业标签

```yaml
industry_tags:
  - ecommerce        # 电商
  - saas             # SaaS工具
  - content          # 内容平台
  - social           # 社交
  - fintech          # 金融科技
  - education        # 教育
  - ai               # AI产品
  - marketplace      # 双边市场
  - entertainment    # 娱乐
  - healthcare       # 医疗健康
  - travel           # 旅游出行
  - food             # 餐饮
  - fashion          # 时尚
  - d2c              # DTC品牌
```

### 阶段标签

```yaml
stage_tags:
  - "0-1"            # 冷启动
  - "1-10"           # 增长期
  - "10-100"         # 规模化
```

### 问题类型标签

```yaml
problem_tags:
  - acquisition      # 获客
  - activation       # 激活
  - retention        # 留存
  - monetization     # 变现
  - referral         # 裂变
  - resurrection     # 召回
```

### 玩法标签

```yaml
tactic_tags:
  - viral_referral   # 病毒裂变
  - plg              # 产品驱动
  - content          # 内容增长
  - community        # 社区增长
  - gamification     # 游戏化
  - seo              # SEO
  - paid_ads         # 付费广告
  - brand            # 品牌营销
  - partnership      # 合作伙伴
  - influencer       # KOL营销
```

## 批量改造脚本

```bash
#!/bin/bash
# scripts/structure-cases.sh

# 为所有案例添加结构化头部
for file in knowledge/cases/**/*.md; do
  # 跳过已有front matter的文件
  if ! grep -q "^---" "$file"; then
    # 提取标题
    title=$(head -1 "$file" | sed 's/^# //')
    
    # 创建front matter
    cat > /tmp/frontmatter.yaml << EOF
---
id: $(basename "$file" .md)
name: $title
region: unknown
industry: []
stage: []
problem_types: []
tactics: []
summary: 待补充
replicable_points: []
warnings: []
---
EOF
    
    # 合并文件
    cat /tmp/frontmatter.yaml "$file" > /tmp/newfile.md
    mv /tmp/newfile.md "$file"
  fi
done

echo "案例结构化完成"
```

## 验证工具

```python
# scripts/validate-case-structure.py

import yaml
import sys
from pathlib import Path

def validate_case(file_path):
    """验证案例结构"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # 检查front matter
    if not content.startswith('---'):
        return False, "缺少YAML front matter"
    
    # 解析front matter
    try:
        parts = content.split('---', 2)
        front_matter = yaml.safe_load(parts[1])
    except:
        return False, "YAML格式错误"
    
    # 检查必需字段
    required_fields = ['id', 'name', 'region', 'industry', 'stage', 'problem_types']
    for field in required_fields:
        if field not in front_matter:
            return False, f"缺少必需字段: {field}"
    
    return True, "验证通过"

if __name__ == "__main__":
    cases_dir = Path("knowledge/cases")
    errors = []
    
    for case_file in cases_dir.glob("**/*.md"):
        valid, msg = validate_case(case_file)
        if not valid:
            errors.append(f"{case_file}: {msg}")
    
    if errors:
        print("验证失败:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("所有案例验证通过")
```
