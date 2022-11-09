class GameStats():
    """追踪游戏的统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏运行期间可能辩护的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
