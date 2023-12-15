from dotenv import load_dotenv
import os

# 加載 .env 檔案中的環境變量
load_dotenv()

# 獲取 FinMind API 金鑰
FINMIND_API_KEY = os.getenv("FINMIND_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")