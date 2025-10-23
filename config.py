import os

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
OPENAI_API_KEY = os.getenv('OPENAI_TOKEN')
PROXY = os.getenv('PROXY')
