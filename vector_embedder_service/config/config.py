import os
from dotenv import load_dotenv

__ENV_FILES = {
    "dev": ".env.dev",
    "prod": ".env.prod",
}


def load_env_vars(env: str) -> None:
    if env not in __ENV_FILES:
        raise ValueError("no env matched")

    env_file_path = os.path.join(os.getcwd(), __ENV_FILES[env])
    load_dotenv(env_file_path)