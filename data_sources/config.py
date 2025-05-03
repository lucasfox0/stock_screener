"""
Configuration file for scraper settings and environment variables.
Edit FMP API key and FMP base URL here.
"""

import os
from dotenv import load_dotenv
load_dotenv()

FMP_KEY = os.getenv("FMP_KEY", "")
BASE_URL = "https://financialmodelingprep.com/api"