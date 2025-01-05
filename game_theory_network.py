import matplotlib.pyplot as plt
import numpy as np
import random

class NetworkSecurityGame:
    def __init__(self):
        """初始化网络安全博弈"""
        self.payoff_matrix = {
            ('防御', '不攻击'): (3, 3),  # 双方和平，系统正常运行
            ('防御', '攻击'): (-2, 1),  # 防御成功，攻击方小收益
            ('不防御', '攻击'): (-8, 8),  # 攻击成功，造成重大损失
            ('不防御', '不攻击'): (4, 4)  # 无防御无攻击，系统运行效率最高
        }

        self.history = []
        self.scores = {'防守方': 0, '攻击方': 0}

    def play_round(self, strategy_a, strategy_b):
        """进行一轮博弈"""
        decision_a = strategy_a(self.history)
        decision_b = strategy_b(self.history)

        # 通过决策得到对应的收益
        payoff_a, payoff_b = self.payoff_matrix[(decision_a, decision_b)]

        # 更新得分
        self.scores['防守方'] += payoff_a
        self.scores['攻击方'] += payoff_b

        # 记录这一轮的历史数据
        self.history.append({
            'round': len(self.history) + 1,
            'decisions': (decision_a, decision_b),
            'payoffs': (payoff_a, payoff_b)
        })

    def run_game(self, strategy_a, strategy_b, rounds):
        """运行多轮博弈"""
        for _ in range(rounds):
            self.play_round(strategy_a, strategy_b)

    def plot_results(self):
        """可视化博弈结果"""
        rounds = len(self.history)

        # 提取每一轮的收益数据
        payoffs_a = [h['payoffs'][0] for h in self.history]  # 防守方的收益
        payoffs_b = [h['payoffs'][1] for h in self.history]  # 攻击方的收益
        cumulative_a = np.cumsum(payoffs_a)  # 防守方的累计收益
        cumulative_b = np.cumsum(payoffs_b)  # 攻击方的累计收益

        # 创建图表
        plt.figure(figsize=(12, 5))

        # 使用黑体
        plt.rcParams['font.family'] = 'SimHei'

        # 绘制单轮收益
        plt.subplot(121)
        plt.plot(range(1, rounds + 1), payoffs_a, 'b-', label='防守方')
        plt.plot(range(1, rounds + 1), payoffs_b, 'r-', label='攻击方')
        plt.title('单轮收益')  # 图表标题
        plt.xlabel('回合')  # X轴标签
        plt.ylabel('收益')  # Y轴标签
        plt.legend()  # 图例
        plt.grid(True)  # 显示网格

        # 绘制累计收益
        plt.subplot(122)
        plt.plot(range(1, rounds + 1), cumulative_a, 'b-', label='防守方')
        plt.plot(range(1, rounds + 1), cumulative_b, 'r-', label='攻击方')
        plt.title('累计收益')  # 图表标题
        plt.xlabel('回合')  # X轴标签
        plt.ylabel('累计收益')  # Y轴标签
        plt.legend()  # 图例
        plt.grid(True)  # 显示网格
        plt.tight_layout()  # 调整布局
        plt.show()  # 显示图表

class PassiveDefender:
    def __init__(self, defense_prob=0.5):
        self.defense_prob = defense_prob

    def make_decision(self, history):
        return '防御' if random.random() < self.defense_prob else '不防御'

class RandomAttacker:
    """随机选择攻击或防守的攻击方"""
    def make_decision(self, history):
        """随机选择攻击或防守"""
        return random.choice(['攻击', '不攻击'])

class EnhancedTitForTat:
    """改进的以牙还牙策略"""

    def __init__(self, is_defender=True, memory_size=3):
        self.is_defender = is_defender
        self.memory_size = memory_size
        self.role = '防守方' if is_defender else '攻击方'
        self.opponent_history = []

    def analyze_pattern(self, history):
        """分析对手行为模式"""
        if not history:
            return None

        recent_moves = [h['decisions'][0 if not self.is_defender else 1]
                        for h in history[-self.memory_size:]]

        # 计算对手的攻击/防御倾向
        aggressive_count = sum(1 for move in recent_moves
                               if (self.is_defender and move == '攻击') or
                               (not self.is_defender and move == '防御'))
        aggressive_rate = aggressive_count / len(recent_moves)

        return aggressive_rate

    def make_decision(self, history):
        """基于历史记录做出决策"""
        if not history:
            # 首轮采取友好策略
            return '防御' if self.is_defender else '不攻击'

        # 分析对手模式
        aggressive_rate = self.analyze_pattern(history)

        # 获取对手上一轮的选择
        opponent_last_move = history[-1]['decisions'][0 if not self.is_defender else 1]

        # 基于对手上一轮行为和整体模式做出决策
        if self.is_defender:
            if opponent_last_move == '攻击' or aggressive_rate > 0.7:
                return '防御'  # 对方攻击性强时保持防御
            else:
                # 对方友好时有小概率降低防御以提高效率
                return '不防御' if random.random() < 0.2 else '防御'
        else:
            if opponent_last_move == '不防御' or aggressive_rate < 0.3:
                return '攻击'  # 对方防御松懈时进行攻击
            else:
                # 对方防御严密时暂时和平
                return '不攻击' if random.random() < 0.8 else '攻击'

def main():
    num_iterations = 5
    rounds = 100

    EnhancedTitForTat_total_defender_score = 0
    PassiveDefender_total_attacker_score = 0
    total_attacker_score_1 = 0
    total_attacker_score_2 = 0

    defender_strategies_1 = EnhancedTitForTat(is_defender=True)
    defender_strategies_2 = PassiveDefender()
    attacker_strategies = RandomAttacker()

    print(f"\n对战: {defender_strategies_1.__class__.__name__} vs {attacker_strategies.__class__.__name__}")
    for i in range(num_iterations):

        game = NetworkSecurityGame()
        game.run_game(lambda h: defender_strategies_1.make_decision(h), lambda h: attacker_strategies.make_decision(h), rounds=rounds)

        EnhancedTitForTat_total_defender_score += game.scores['防守方']
        total_attacker_score_1 += game.scores['攻击方']

        # 打印每次迭代的结果
        print(f"\n第 {i + 1} 次迭代结果:")
        print(f"防守方得分: {game.scores['防守方']}")
        print(f"攻击方得分: {game.scores['攻击方']}")
        game.plot_results()

    print(f"\n对战: {defender_strategies_2.__class__.__name__} vs {attacker_strategies.__class__.__name__}")
    for i in range(num_iterations):
        game = NetworkSecurityGame()
        game.run_game(lambda h: defender_strategies_2.make_decision(h), lambda h: attacker_strategies.make_decision(h), rounds=rounds)

        PassiveDefender_total_attacker_score += game.scores['防守方']
        total_attacker_score_2 += game.scores['攻击方']

        # 打印每次迭代的结果
        print(f"\n第 {i + 1} 次迭代结果:")
        print(f"防守方得分: {game.scores['防守方']}")
        print(f"攻击方得分: {game.scores['攻击方']}")
        game.plot_results()

    # 打印总体统计
    print("\n=== 总体统计 ===")
    print(f"防守方（采取以牙还牙策略防御）平均得分: {EnhancedTitForTat_total_defender_score / num_iterations:.2f}")
    print(f"攻击方平均得分: {total_attacker_score_1 / num_iterations:.2f}")
    print(f"防守方（采取传统被动防御策略防御）平均得分: {PassiveDefender_total_attacker_score / num_iterations:.2f}")
    print(f"攻击方平均得分: {total_attacker_score_2 / num_iterations:.2f}")

if __name__ == "__main__":
    main()