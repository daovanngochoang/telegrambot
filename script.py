from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pandas import DataFrame

#

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google_api_token.json'

credentials: Credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

import gspread

#
gs = gspread.authorize(credentials)

file = gs.open("APPLE STOCK")

sheet = file.worksheet("APLE")

data = sheet.get("A:Z")
#
df = DataFrame(data)
#
df.columns = df.iloc[0]
df = df.iloc[1:]


# fig = px.histogram(df[['Role', 'Is Registered']], x='Role', color="Role")
# fig.show()
# fig.write_image("tmp/test.png")
#
# import pandas as pd
#
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
# df = df.loc[(df["Date"] >= "2016-07-01") & (df["Date"] <= "2016-12-01")]




# fig = px.line(df, x='Date', y='AAPL.High')
# fig.show()
