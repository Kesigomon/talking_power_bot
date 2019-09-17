import asyncio

class Power_counter:
    __slots__ = ('loop', 'power', 'count', 'limit', 'rank', 'bot_count',
                 'conlevel')
    cooldown = (30, 20, 15, 10, 5)
    power_list = (50, 25, 15, 5, 1, 0)

    def __init__(self, loop: asyncio.AbstractEventLoop, **kwargs):
        """
        Level_counter
        発言力カウンターです。
        exp:経験値
        count:発言回数（Botコマンド以外）
        bot_count：botのコマンド（と思われる）の使用回数
        """
        self.loop = loop
        self.limit = None
        self.power = kwargs.get('power', 0)
        self.count = kwargs.get('count', 0)
        self.rank = kwargs.get('rank', 0)
        self.bot_count = kwargs.get('bot_count', 0)
        self.conlevel = 0

    def increase_conlevel(self):
        self.loop.create_task(self._increase_conlevel())

    async def _increase_conlevel(self):
        if self.limit is None:
            self.limit = asyncio.Event(loop=self.loop)
        else:
            self.limit.set()
        self.conlevel = min(self.conlevel + 1, len(self.cooldown))
        while self.conlevel:
            try:
                await asyncio.wait_for(self.limit.wait(), timeout=self.cooldown[self.conlevel - 1])
            except asyncio.TimeoutError:
                self.conlevel -= 1
            else:
                self.limit.clear()
                break
        else:
            self.limit = None

    def increase_power(self):
        self.power += self.power_list[self.conlevel]

    def increase_value(self):
        self.increase_power()
        self.increase_conlevel()
