from dotenv import load_dotenv
from decouple import config

print(config('GEMINI_KEY'))