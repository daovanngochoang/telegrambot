import os

import gspread
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from gspread import Client
from telegram import Update
from telegram.ext import Application

from gsheet_commands import gsheet_chat_commands
from help import HelpCommands

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google_api_token.json'
TELEGRAM_API_KEY = "6537692822:AAHtXX9IpYL8kD4uvsNZf6nRsEns1W9YnBU"
FOLDER_ID = "1sfrim941Wiz5VaT3gjaEj_V214HKLimA"
# os.mkdir("./tmp")


def main() -> None:
    # Create the Application and pass it your bot's token.
    load_dotenv()
    application = (Application
                   .builder()
                   .token(TELEGRAM_API_KEY)
                   .build())

    creds: Credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    gsheet_client: Client = gspread.authorize(creds)

    application.add_handlers(gsheet_chat_commands(gsheet_client))
    application.add_handlers(HelpCommands().command_handlers())

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
