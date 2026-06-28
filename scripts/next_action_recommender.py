#!/usr/bin/env python3
"""
oh-my-growth Next Action Recommender
智能推荐下一步行动
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class NextActionRecommender:
    """基于用户历史推荐下一个命令"""

    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.expanduser("~/.oh-my-growth")
        self.history_file = os.path.join(self.config_dir, "command-history.json")
        self.user_profile_file = os.path.join(self.config_dir, "user-profile.json")

        # 加载用户画像
        self.user_profile = self._load_user_profile()

        # 加载命令历史
        self.history = self._load_history()

        # 推荐规则
        self.recommendation_rules = {
            # (last_command, condition) -> (next_command, reason)
            ("diagnose", "completed"): ("match", "查看相似案例，找到可复制的策略"),
            ("match", "completed"): ("assess", "评估你的方案可行性"),
            ("assess", "positive"): ("design", "制定具体执行方案"),
            ("assess", "negative"): ("diagnose", "重新诊断，寻找其他方向"),
            ("design", "completed"): ("brd", "生成决策文档，申请资源"),
            ("cold-start", "completed"): ("match", "看看其他产品如何冷启动"),
            ("retention", "completed"): ("learn", "系统学习留存策略"),
            ("monetization", "completed"): ("assess", "评估变现方案可行性"),
            ("referral", "completed"): ("design", "设计裂变执行方案"),
        }

        # 命令旅程映射
        self.command_journeys = {
            "新手探索": ["diagnose", "match", "assess"],
            "冷启动路径": ["cold-start", "match", "design"],
            "留存优化路径": ["retention", "diagnose", "design"],
            "变现设计路径": ["monetization", "assess", "design"],
            "裂变规划路径": ["referral", "assess", "design"],
        }

    def _load_user_profile(self) -> Dict:
        """加载用户画像"""
        if os.path.exists(self.user_profile_file):
            with open(self.user_profile_file, 'r') as f:
                return json.load(f)
        return {
            "stage": "unknown",
            "problem": "unknown",
            "industry": "unknown",
            "first_diagnosis_completed": False
        }

    def _load_history(self) -> List[Dict]:
        """加载命令历史"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_history(self):
        """保存命令历史"""
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def record_command(self, command: str, params: Dict = None, result: str = "success"):
        """记录命令执行"""
        entry = {
            "command": command,
            "params": params or {},
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(entry)
        self.save_history()

    def get_last_command(self) -> Optional[Dict]:
        """获取最后一个命令"""
        return self.history[-1] if self.history else None

    def recommend_next(self) -> Dict:
        """推荐下一个命令"""
        last = self.get_last_command()

        # 如果没有历史，推荐新手命令
        if not last:
            return self._recommend_first_command()

        # 基于最后一个命令推荐
        last_cmd = last["command"]
        last_result = last["result"]

        # 查找推荐规则
        rule_key = (last_cmd, last_result)
        if rule_key in self.recommendation_rules:
            next_cmd, reason = self.recommendation_rules[rule_key]
            return {
                "command": next_cmd,
                "reason": reason,
                "confidence": "high",
                "based_on": "last_command"
            }

        # 基于用户画像推荐
        return self._recommend_by_profile()

    def _recommend_first_command(self) -> Dict:
        """推荐第一个命令"""
        stage = self.user_profile.get("stage", "cold-start")
        problem = self.user_profile.get("problem", "acquisition")

        # 映射到推荐命令
        if stage == "cold-start" and problem == "acquisition":
            return {
                "command": "cold-start",
                "reason": "你的产品处于冷启动期，先获取首批用户",
                "confidence": "high",
                "based_on": "user_profile"
            }
        elif problem == "retention":
            return {
                "command": "retention",
                "reason": "聚焦用户留存问题",
                "confidence": "high",
                "based_on": "user_profile"
            }
        elif problem == "monetization":
            return {
                "command": "monetization",
                "reason": "设计变现策略",
                "confidence": "high",
                "based_on": "user_profile"
            }
        else:
            return {
                "command": "diagnose",
                "reason": "先进行整体诊断",
                "confidence": "medium",
                "based_on": "default"
            }

    def _recommend_by_profile(self) -> Dict:
        """基于用户画像推荐"""
        problem = self.user_profile.get("problem", "acquisition")

        # 推荐学习命令
        if len(self.history) >= 5:
            return {
                "command": "learn",
                "reason": "你已经使用了一段时间，系统学习增长方法",
                "confidence": "medium",
                "based_on": "usage_pattern"
            }

        # 默认推荐
        return {
            "command": "diagnose",
            "reason": "继续探索增长策略",
            "confidence": "medium",
            "based_on": "default"
        }

    def get_journey_progress(self) -> Dict:
        """获取用户旅程进度"""
        total_commands = len(self.history)
        unique_commands = len(set(cmd["command"] for cmd in self.history))

        # 判断用户等级
        if total_commands == 0:
            level = "新手"
        elif total_commands < 5:
            level = "探索者"
        elif total_commands < 20:
            level = "专家"
        else:
            level = "大师"

        # 计算旅程完成度
        journey_completion = {}
        for journey_name, commands in self.command_journeys.items():
            completed = sum(1 for cmd in commands if any(h["command"] == cmd for h in self.history))
            completion_rate = completed / len(commands) * 100
            journey_completion[journey_name] = {
                "completed": completed,
                "total": len(commands),
                "rate": completion_rate
            }

        return {
            "level": level,
            "total_commands": total_commands,
            "unique_commands": unique_commands,
            "journey_completion": journey_completion
        }

    def print_recommendation(self):
        """打印推荐"""
        rec = self.recommend_next()
        progress = self.get_journey_progress()

        print("\n" + "="*60)
        print("  🎯 下一步推荐")
        print("="*60)
        print(f"\n  推荐命令: /omg-{rec['command']}")
        print(f"  理由: {rec['reason']}")
        print(f"  置信度: {rec['confidence']}")

        print("\n" + "="*60)
        print("  📊 你的使用进度")
        print("="*60)
        print(f"\n  用户等级: {progress['level']}")
        print(f"  已使用命令: {progress['total_commands']} 次")
        print(f"  解锁命令: {progress['unique_commands']} 种")

        print("\n  旅程完成度:")
        for journey, stats in progress['journey_completion'].items():
            bar = "█" * int(stats['rate'] / 10) + "░" * (10 - int(stats['rate'] / 10))
            print(f"    {journey}: {bar} {stats['rate']:.0f}%")

        print("\n")


def main():
    """主函数"""
    import sys

    recommender = NextActionRecommender()

    # 如果有参数，记录命令
    if len(sys.argv) > 1:
        command = sys.argv[1]
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        result = sys.argv[3] if len(sys.argv) > 3 else "success"

        recommender.record_command(command, params, result)

    # 打印推荐
    recommender.print_recommendation()


if __name__ == "__main__":
    main()
