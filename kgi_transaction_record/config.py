from pathlib import Path
from threading import local

project_folder = Path(__file__).absolute().parents[1]
config_folder = project_folder.joinpath("config")

gmail_api_path = config_folder.joinpath("credentials.json")
google_api_path = config_folder.joinpath("google_api_key.json")
gmail_token_path = config_folder.joinpath("token.pickle")

path = {
    "google_api": google_api_path,
    "gmail_api": gmail_api_path,
    "gmail_token": gmail_token_path,
}

key = {"kgi_mail": "OWZmMThiYTQy"}

redis = {"host": "redis", "port": 6379}

google_sheet = {
    "KGI": "1MRb_PTKGrB7bhkqs06DkYAH3xPYI9NRoIr_P-SdZf94",
    "client": "1wSqRSU6O9PR77im5fwV4GrYSXJLMJa_Rve-zgMmi1F8",
}

robot = {
    "tsaitung": "https://chat.googleapis.com/v1/spaces/AAAAo-rIW2M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=P3BKjvY6yXN1UQI4Ogmc1k16-7aLQY9XmJTdKcUTmCY%3D",
    "KGI": "https://chat.googleapis.com/v1/spaces/AAAAdB1FK2o/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Z9LTRca093pf9vmTG1HekxrqEvPvnqfSPECOljkoS6A%3D",
}

sheet_data = {
    ######建立dictionary 各店家有對應的biwwekly sheet，內容為店家對應 : 兩個表單名、行名、額外備註店家名、
    "KGI_record": {
        "title": [
            "是否完成核對",
            "日期",
            "代理行",
            "末五碼",
            "交易金額",
            "匯款店家",
            "匯款公司",
            "匯款帳號(附言)",
            "收款虛擬帳號",
            "備註",
        ],
        "fixed_row": "5",
    },
}
