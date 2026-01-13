import httpx
import openai
from aiogram import Bot

import config
from .settings import GPTModel
from .messages import GPTMessage


class GPTService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model: GPTModel = GPTModel.GPT_4_TURBO):
        self._gpt_token = config.GPT_KEY
        self._proxy = config.PROXY
        self._client = self._create_client()
        self._model = model.value

    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._gpt_token,
            # http_client=httpx.AsyncClient(
            #     proxy=self._proxy,
            # )
        )
        return gpt_client

    async def request(self, message_list: GPTMessage, bot: Bot) -> str:
        try:
            response = await self._client.chat.completions.create(
                messages=message_list.message_list,
                model=self._model,
            )
            return response.choices[0].message.content
        except Exception as e:
            await bot.send_message(
                chat_id=config.ADMIN_ID,
                text=str(e),
            )

    # async def transcript_voice(self, file, bot: Bot):
    #     try:
    #         with open(file, "rb") as audio_file:
    #             transcript = await self._client.audio.transcriptions.create(
    #                 model=GPTModel.WHISPER.value,
    #                 file=audio_file
    #             )
    #             return transcript.text
    #     except Exception as e:
    #         await bot.send_message(
    #             chat_id=config.ADMIN_ID,
    #             text=str(e),
    #         )