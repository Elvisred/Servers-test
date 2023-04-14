import os


class BaseTest:
    UI_URL = "https://portal.servers.com/"
    baseurl = os.environ.get("UI_URL", UI_URL)
