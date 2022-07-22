from __future__ import print_function

import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from main_app.google_api.config import SPREADSHEET_ID, RANGE, TOKEN, CLIENT_SECRET


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
PATH = Path(__file__).resolve().parent
TOKEN = PATH / TOKEN
CLIENT_SECRET = PATH / CLIENT_SECRET


def get_sheet():
    """Подключается к Google API и возвращает объект таблицы.
    Для работы необходим токен client_secret_***.json в директории рядом с этим модулем"""
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        creds = None
        if os.path.exists(TOKEN):
            creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN, 'w') as token:
                token.write(creds.to_json())
        return sheet

    except HttpError as err:
        print(err)


def execute_data(cell_range):
    """Извлекает данные из таблицы и возвращает их."""
    sheet = get_sheet()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=cell_range).execute()
    values = result.get('values', None)
    if not values:
        print('No data found.')
    return values


if __name__ == '__main__':
    print(execute_data(RANGE))
