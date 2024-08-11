# from utils.base.config import settings
import asyncio

from utils.base.integration import BaseServiceAPI


class TelegramAPI(BaseServiceAPI):
    def __init__(self):
        # super().__init__(base_api=f"https://api.telegram.org/bot{settings.bot.token}")
        super().__init__(base_api=f"https://api.telegram.org/bot7264557873:AAGtGwY3vDqV__SK5K-jRjoCmx9idKwK-oI")

    async def send_message(self, user_id: int, message: str):
        if not user_id:
            return
        url = "/sendMessage"
        body = {"chat_id": user_id,
                "text": message,
                "parse_mode": "html"}
        response = await self.post(url=url, body=body)
        return response


if __name__ == '__main__':
    async def send():
        message = f'''НОВОЕ СОБЫТИЕ ⭐️

        Акт #1523 успешно подписан    

        Проект "super projecy" успешно завершен ✅

        Проект принял: Лоx Лоx'''
        await TelegramAPI().send_message(user_id=373649910, message=message)

    asyncio.run(send())