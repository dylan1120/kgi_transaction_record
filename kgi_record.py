#!/usr/bin/env python
# coding: utf-8

# Gmail_File
import numpy as np
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import config
import os
import base64
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from gmailsetting import GmailSetting
from redistime import RedisTime
import zipfile
from robot import robot_kgi
import datetime
import time
# googlesheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(config.path["google_api"], scope)
# authorize the clientsheet 
client = gspread.authorize(creds)
KGI_spreadsheet = client.open_by_key(config.google_sheet["KGI"])
client_spreadsheet = client.open_by_key(config.google_sheet["client"])
accountant = client_spreadsheet.worksheet("原始檔")
accountant_df = pd.DataFrame(accountant.get_all_values()[1::], columns=accountant.get_all_values()[1 - 1])


def record_csvtodf(input_file):
    read_file = pd.read_csv(input_file, index_col=None, header=None, encoding='big5', dtype=str)
    count = read_file.shape[0]
    payee = []
    remitter = []
    amount = []
    bank = []
    date = []
    header = ["payee", "amount", "bank_remitter", "remitter", "date"]
    for i, row_all in read_file.iterrows():
        row = row_all[0].split()
        if len(row) == 6:
            date_string = row[0][16:24]
            date_string = datetime.datetime.strptime(date_string, "%Y%m%d")
            date_string = datetime.datetime.strftime(date_string, "%Y/ %m/ %d")
            date.append(date_string)
            payee.append(row[2])
            amount.append(float(row[3][1:16]))
            bank.append(row[3][16:19] + row[3][23::])
            if row[4][0] == "0":
                remitter.append(row[4][2::])
            else:
                remitter.append(row[4][:])
        else:
            date_string = row[0][16:24]
            date_string = datetime.datetime.strptime(date_string, "%Y%m%d")
            date_string = datetime.datetime.strftime(date_string, "%Y/ %m/ %d")
            date.append(date_string)
            payee.append(row[2])
            amount.append(float(row[3][1:16]))
            bank.append(row[3][16:19] + row[3][23:29])
            if len(row[3]) > 29:
                if row[3][29] == "0":
                    remitter.append(row[3][31::])
                else:
                    remitter.append(row[3][29::])
            else:
                remitter.append("")

    record = pd.DataFrame((payee, amount, bank, remitter, date), index=header).T
    return record


# 建立紀錄表單，若已存在則避免覆蓋
def record_sheet_create(record):
    sheet_title = record["date"][0][:8] + "交易紀錄_test"
    fixed_row = 5
    try:
        KGI_spreadsheet.add_worksheet(sheet_title, 500, 20, index=None)
        sheet = KGI_spreadsheet.worksheet(sheet_title)
        sheet.insert_row(config.sheet_data["KGI_record"]["title"], fixed_row)
    except:
        sheet = KGI_spreadsheet.worksheet(sheet_title)

    sheet.batch_update([
        {'range': 'A1', 'values': [[record["date"][0][:8] + " 交易紀錄"]]},
        {'range': 'A2', 'values': [["當月交易紀錄總筆數"]]},
        {'range': 'A3', 'values': [["未完成對帳總筆數"]]}
    ])

    # 更改dataframe格式
    # 調整freeze範圍
    sheet.freeze(rows=fixed_row, cols=1)

    # 更改顏色之函式
    def set_color(sheet, area, R, G, B):
        sheet.format(str(area), {
            "backgroundColor": {
                "red": int(R) / 255,
                "green": int(G) / 255,
                "blue": int(B) / 255
            }})

    # 更改標題顏色
    set_color(sheet, "A5:Z5", 255, 255, 0)
    return sheet


# 進行記錄
def record_update(record, accountant_df, sheet):
    header_record = ["check", "date", "bank_remitter", "five", "amount", "store_remitter", "company_remitter",
                     "remitter", "payee", "notes"]
    values = None
    for i, row in record.iterrows():
        value = []
        for col in header_record:
            try:
                value.append(row[col])
            except:
                if col == "five":
                    try:
                        float(row["remitter"][0])
                        value.append(row["remitter"][-5:])
                    except:
                        value.append(row["remitter"])
                elif col == "company_remitter":
                    if row["payee"] in accountant_df["virtual_bank_account"].tolist():
                        company_index = accountant_df["virtual_bank_account"].tolist().index(row["payee"])
                        company = accountant_df["company_name"][company_index]
                        value.append(company)
                    else:
                        value.append("")
                elif col == "store_remitter":
                    if row["payee"] in accountant_df["virtual_bank_account"].tolist():
                        company_index = accountant_df["virtual_bank_account"].tolist().index(row["payee"])
                        company = accountant_df["store_name"][company_index]
                        value.append(company)
                    else:
                        value.append("")
                elif col == "message":
                    value.append("")
                elif col == "notes":
                    value.append("")
                else:
                    value.append("")
        if values == None:
            values = [value]
        else:
            values = values + [value]
    sheet.append_rows(values, value_input_option='RAW', insert_data_option=None, table_range=None)


# connect to the Gmail API
service = build('gmail', 'v1', credentials=GmailSetting().token_check())
# request a list of all the messages 
result = service.users().messages().list(maxResults=300, userId='me').execute()
user_id = "me"

for i in range(len(result["messages"])):
    msg_id = result["messages"][i]['id']
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    for j in range(len(message['payload']['headers'])):
        if message['payload']['headers'][j]["name"] == "Subject":
            subject = message['payload']['headers'][j]['value']
        if message['payload']['headers'][j]["name"] == "Date":
            Date = message['payload']['headers'][j]['value']

    try:
        if RedisTime().time_to_seconds_kgi(Date) <= RedisTime().redis_get_time_kgi():
            break
    except:
        continue

    if "台幣委託收款入帳明細檔" in subject:
        try:
            GmailSetting().get_attachments(service, user_id, msg_id, message)
            filename = message['payload']['parts'][1]['filename']
            files = zipfile.ZipFile(filename)
            file_name = files.namelist()[0]
            files.extract(file_name, r'.', pwd=config.key["kgi_mail"].encode('utf-8'))
            try:
                record = record_csvtodf(file_name)
                sheet = record_sheet_create(record)
                record_update(record, accountant_df, sheet)
                print(Date, "update successfully.")
                robot_kgi(Date + " update successfully.")

            except:
                print(Date, "update failed.")
                robot_kgi(Date + " update failed.")
                robot_kgi("Please check the file of transaction record today.")
        except:
            print("key error : parts")
        print("=========================================")
RedisTime().redis_set_time_kgi()
