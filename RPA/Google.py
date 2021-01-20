from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import mimetypes
from pprint import pprint


class Spreadsheet(object):
    def __init__(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        self.spreadsheet = build(
            'sheets', 'v4', credentials=creds).spreadsheets()

    def Auth():
        SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    def Get_values(self, Spreadsheet_id: str, Range: str):
        result = self.spreadsheet.values().get(
            spreadsheetId=Spreadsheet_id, range=Range).execute()
        values = result.get('values', [])
        sheet = pd.DataFrame(values, columns=values[0])
        sheet = sheet.drop(0)
        sheet = sheet.reset_index()
        return sheet

    def　Set_DataFrame(self, Spreadsheet_id: str, Range: str, DataFrame):
        self.spreadsheet.values().append(spreadsheetId=Spreadsheet_id,
                                         valueInputOption="USER_ENTERED",
                                         range=Range,
                                         body={"values": DataFrame.values.tolist()}).execute()

    def Set_values(self, Spreadsheet_id: str, Range: str, Values):
        self.spreadsheet.values().update(spreadsheetId=Spreadsheet_id,
                                         valueInputOption="USER_ENTERED",
                                         range=Range,
                                         body={"values": [[Values]]}).execute()

    def Get_sheets(self, Spreadsheet_id: str):
        sheet_metadata = self.spreadsheet.get(
            spreadsheetId=Spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        Sheet_Name = [Sheet_Name["properties"]["title"]
                      for Sheet_Name in sheets]
        return Sheet_Name

    def Clear(self, Spreadsheet_id: str, Range: str):
        self.spreadsheet.values().clear(spreadsheetId=Spreadsheet_id, range=Range).execute()


class Drive(object):
    def　__init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def Trash(self, Drive_id: str):
        query = f"'{Drive_id}' in parents and trashed=false"
        file_lists = self.drive.ListFile({'q': query}).GetList()
        for file_id in file_lists:
            f = self.drive.CreateFile({'id': file_id["id"]})
            f.Trash()

    def Upload(self, Dir_path: str, File_name: str, Folder_id: str):
        mime = mimetypes.guess_type(f"{Dir_path}/{File_name}")[0]
        file_set = self.drive.CreateFile({
            'title': File_name,
            'mimeType': mime,
            "parents": [{"id": Folder_id}]
        })
        file_set.SetContentFile(f"{Dir_path}/{File_name}")
        file_set.Upload()

    def Download(self, Drive_id: str, File_name: str, Dir_path: str):
        query = f"'{Drive_id}' in parents and trashed=false"
        file_id = self.drive.ListFile({'q': query}).GetList()
        try:
            for i in range(len(file_id)):
                if File_name == file_id[i]["title"]:
                    f = drive.CreateFile({'id': file_id[i]["id"]})
                    f.GetContentFile(os.path.join(PATH, file_id[i]["title"]))
                    break
        except Exception as e:
            print(e)

    def Get_files(self, Drive_id: str):
        query = f"'{Drive_id}' in parents and trashed=false"
        file_ids = self.drive.ListFile({'q': query}).GetList()
        flist = []
        for file in file_ids:
            flist.append({f'{file["title"]}': f'{file["id"]}'})
        return pprint(flist)
