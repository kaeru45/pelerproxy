"""
PelerProxy Bot — Configuration
Loads settings from environment variables or config.toml.
"""
import os
import tomllib
from pathlib import Path

# ==================== PATHS ====================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ACCOUNTS_FILE = BASE_DIR / "webshare_accounts.json"
PROXIES_FILE = BASE_DIR / "proxies.txt"
DB_PATH = DATA_DIR / "pelerproxy.db"
CONFIG_FILE = BASE_DIR / "config.toml"

# ==================== LOAD CONFIG ====================

_cfg: dict = {}
if CONFIG_FILE.exists():
    _cfg = tomllib.loads(CONFIG_FILE.read_text(encoding="utf-8"))

def _get(section: str, key: str, env_var: str, default=""):
    return os.getenv(env_var) or _cfg.get(section, {}).get(key, default)

# ==================== BOT ====================

BOT_TOKEN = os.getenv("BOT_TOKEN") or _cfg.get("bot", {}).get("token", "")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set via environment variable or config.toml")

# ==================== ADMIN ====================

_admin_env = os.getenv("ADMIN_IDS", "")
if _admin_env:
    ADMIN_IDS: list[int] = [int(x.strip()) for x in _admin_env.split(",") if x.strip()]
else:
    ADMIN_IDS: list[int] = _cfg.get("admin", {}).get("ids", [])

# ==================== CAPTCHA PROVIDERS ====================

CAPTCHA_DEFAULT_PROVIDER = _get("captcha", "default_provider", "CAPTCHA_DEFAULT_PROVIDER", "2captcha")

CAPTCHA_PROVIDERS = {
    "azcaptcha": {
        "name": "AZCaptcha",
        "api_url": "https://azcaptcha.com/in.php",
        "result_url": "https://azcaptcha.com/res.php",
        "api_key": os.getenv("CAPTCHA_AZCAPTCHA_KEY") or _cfg.get("captcha", {}).get("azcaptcha", {}).get("api_key", ""),
    },
    "2captcha": {
        "name": "2Captcha",
        "api_url": "https://2captcha.com/in.php",
        "result_url": "https://2captcha.com/res.php",
        "api_key": os.getenv("CAPTCHA_2CAPTCHA_KEY") or _cfg.get("captcha", {}).get("2captcha", {}).get("api_key", ""),
    },
}

# ==================== WEBSHARE ====================

FIXED_PASSWORD = _get("webshare", "fixed_password", "WEBSHARE_FIXED_PASSWORD", "Pasardigital#26")
WEBSHARE_RECAPTCHA_SITEKEY = _get("webshare", "recaptcha_sitekey", "WEBSHARE_RECAPTCHA_SITEKEY", "6LeHZ6UUAAAAAKat_YS--O2tj_by3gv3r_l03j9d")
WEBSHARE_REGISTER_URL = _get("webshare", "register_url", "WEBSHARE_REGISTER_URL", "https://proxy.webshare.io/register")
API_BASE = _get("webshare", "api_base", "WEBSHARE_API_BASE", "https://proxy.webshare.io/api/v2")

# ==================== PROXY SETTINGS ====================

PROXY_MODE_DEFAULT = bool(_get("proxy", "mode_default", "PROXY_MODE_DEFAULT", True))
PROXY_CHECK_TIMEOUT = int(_get("proxy", "check_timeout", "PROXY_CHECK_TIMEOUT", 15))
PROXY_CHECK_URL = _get("proxy", "check_url", "PROXY_CHECK_URL", "http://httpbin.org/ip")
PROXY_MAX_RETRIES = int(_get("proxy", "max_retries", "PROXY_MAX_RETRIES", 5))

# ==================== LIMITS ====================

MAX_REGISTRATIONS_PER_DAY = int(_get("limits", "max_registrations_per_day", "MAX_REGISTRATIONS_PER_DAY", 1))
MAX_PROXIES_PER_FETCH = int(_get("limits", "max_proxies_per_fetch", "MAX_PROXIES_PER_FETCH", 10))
MAX_ACCOUNTS_KEPT = int(_get("limits", "max_accounts_kept", "MAX_ACCOUNTS_KEPT", 20))
