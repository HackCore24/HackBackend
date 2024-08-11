from utils.base.config import settings
from utils.base.integration import BaseServiceAPI


class TelegramAPI(BaseServiceAPI):
    def __init__(self):
        super().__init__(base_api=f"https://api.telegram.org/bot{settings.bot.token}")

    async def send_message(self, user_id: int, message: str, project_id: str):
        if not user_id:
            return
        url = "/sendMessage"
        body = {"chat_id": user_id,
                "text": message,
                "parse_mode": "html",
                "reply_markup": {
                    "inline_keyboard": [[
                        {
                            "text": "Посмотреть ⚙️",
                            "url": f"https://24core.ru/project/{project_id}"
                        }
                    ]]
                }
                }
        response = await self.post(url=url, body=body)
        return response

