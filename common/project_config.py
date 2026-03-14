
from SCANSTOCK.settings import BASE_DIR  # from django.conf import settings
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import toml as tomllib  # Python <3.11
from dotenv import load_dotenv
import os

def get_priority_config(path=None, key=None, default=None, data_type=None):
    """
    Priority:
    1. Environment Variable
    2. pyproject.toml
    3. default

    Example:
    get_priority_config(path="tool.configs", key="login_auth_needed", data_type=bool)
    """
    try:
        load_dotenv() # Load environment variables from .env file if it exists
        if key:
            env_val = os.environ.get(key)
            if env_val is not None:
                if data_type:
                    if data_type == bool:
                        return env_val.lower() in ["true", "1", "yes", "True", "TRUE"]
                    # elif data_type == int:
                    #     return int(env_val)
                    # elif data_type == float:
                    #     return float(env_val)
                    # elif data_type == str:
                    #     return str(env_val)
                    # else:
                    #     return env_val
                    return data_type(env_val)

                return env_val
        with open(BASE_DIR / "pyproject.toml", "r", encoding="utf-8") as f:
                CONFIG = tomllib.loads(f.read())
        if path:
            for division in path.split("."):
                CONFIG = CONFIG.get(division, {})
        return CONFIG.get(key, default)
    except Exception as e:
        print(e)
        return default