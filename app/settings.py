# type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

SALT: bytes = os.getenv("SALT").encode()
