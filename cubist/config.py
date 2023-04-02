MOST_COMMON_HEADERS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

HEADERS = {
    "User-Agent": MOST_COMMON_HEADERS,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://cubist.dev",
    "Connection": "keep-alive",
    "Referer": "https://cubist.dev/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}

CAPMONSTER_API_KEY = ""  # Enter your CapMonster API key here

if CAPMONSTER_API_KEY == "":
    CAPMONSTER_API_KEY = input("Enter your CapMonster API key >> ")


CUBIST_URL = "https://cubist.dev/early-access"
CUBIST_SITE_KEY = "6LcNOeYjAAAAAI5GuvtPr_C7NwqEJejV_524MJ1y"
