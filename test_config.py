from config import *

print("BOT TOKEN:", "Loaded" if BOT_TOKEN else "Missing")
print("OPENAI API KEY:", "Loaded" if OPENAI_API_KEY else "Missing")
print("BASE URL:", OPENAI_BASE_URL)
print("MODEL:", MODEL)