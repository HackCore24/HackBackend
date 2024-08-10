from utils.base.config import settings
from utils.base.integration import BaseServiceAPI


class TelegramAPI(BaseServiceAPI):
    def __init__(self):
        super().__init__(base_api=f"https://api.telegram.org/bot{settings.bot.token}")
        self.product_check = {'Накрутка ПФ 7 дней': (4, 5000.00), "Сделаю сам": (16, 15000.00),
                              "Подписка": (28, 200000.00), "Сделайте за меня + дизайн": (24, 45000.00),
                              "Сделайте за меня": (20, 30000.00), "Оптимальный функционал продвижения": (12, 80000.00),
                              "Накрутка ПФ 1 год": (8, 50000.00)}

    async def send_message(self, user_id: int, message: str):
        if not user_id:
            return
        url = "/sendMessage"
        body = {"chat_id": user_id,
                "text": message,
                "parse_mode": "MarkdownV2"}
        response = await self.post(url=url, body=body)
        return response
