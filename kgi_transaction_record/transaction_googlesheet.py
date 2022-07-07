import numpy as np
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import config


class GoogleSheet:
    def __init__(self):
        # define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            config.path["google_api"], scope
        )
        # authorize the clientsheet
        self.client = gspread.authorize(creds)

    def item_mapping_sheet(self, company_name):
        # get the instance of the Spreadsheet
        sheet = self.client.open_by_key(config.google_sheet["item_mapping"])
        # get the matching sheet in the Spreadsheet
        sheet_instance = sheet.worksheet(company_name)

        records_data = sheet_instance.get_all_records()
        records_df = pd.DataFrame.from_dict(records_data)

        return records_df

    def store_mapping_sheet(self, company_name):
        # get the instance of the Spreadsheet
        sheet = self.client.open_by_key(config.google_sheet["store_mapping"])
        # get the matching sheet in the Spreadsheet
        sheet_instance = sheet.worksheet(company_name)

        records_data = sheet_instance.get_all_records()
        records_df = pd.DataFrame.from_dict(records_data)

        return records_df

    def gmail_mapping_sheet(self):

        # get the instance of the Spreadsheet
        sheet = self.client.open_by_key(config.google_sheet["gmail_mapping"])
        # get the matching sheet in the Spreadsheet
        sheet_instance = sheet.worksheet("gmail_file")

        records_data = sheet_instance.get_all_records()
        records_df = pd.DataFrame.from_dict(records_data)

        return records_df
