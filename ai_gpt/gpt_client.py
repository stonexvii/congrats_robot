import openai
from aiogram import Bot
import httpx
import config
from .enums import GPTModel
from .gpt_message import GPTMessage


class GPTService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model: GPTModel = GPTModel.GPT_4_TURBO):
        self._gpt_token = config.OPENAI_API_KEY
        self._proxy = config.PROXY
        self._client = self._create_client()
        self._model = model.value

    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._gpt_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
            )
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

    async def transcript_voice(self, file, bot: Bot):
        try:
            with open(file, "rb") as audio_file:
                transcript = await self._client.audio.transcriptions.create(
                    model=GPTModel.WHISPER.value,
                    file=audio_file
                )
                return transcript.text
        except Exception as e:
            await bot.send_message(
                chat_id=config.ADMIN_ID,
                text=str(e),
            )

    # async def generate_image(self, description: str, url: str):
    #     prompt = await FileManager.read('ai_gpt', 'prompts', 'dalle_prompt', desc=description, url=url)
    #     print(prompt)
    #     image_response = await self._client.images.generate(
    #         model=GPTModel.GPT_IMAGE.value,
    #         prompt=prompt,
    #         size="1024x1024",
    #     )
    #     image_url = image_response.data[0].url
    #     resp_img = requests.get(image_url)
    #     final_img = Image.open(BytesIO(resp_img.content))
    #     final_img.save(os.path.join('data', 'final_card.png'))
    #     with open(os.path.join('data', 'final_card.png'), "rb") as photo:
    #         return photo
