import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_gspread(creds_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(credentials)
    return client

def write_to_sheet(client, spreadsheet_name, worksheet_name, data):
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    worksheet.update('A1', data)

def read_from_sheet(client, spreadsheet_name, worksheet_name):
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet.get_all_records()
