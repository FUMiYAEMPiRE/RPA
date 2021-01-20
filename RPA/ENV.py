import os
from dotenv import load_dotenv
from pathlib import Path


def load_env(ENV_NAME:str):
    load_dotenv(verbose=True)
    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    except:
        dotenv_path = os.path.join(Path().resolve(), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(ENV_NAME)