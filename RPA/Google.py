
class Spreadsheet:
    def __init__(self):
        from googleapiclient.discovery import build
        import pickle
        import os
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        self.service = build('sheets', 'v4', credentials=creds)
    
    def Auth():
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
        import os
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

    def Get_values(self, Spreadsheet_id:str, Range:str):
        import pandas as pd
        result = self.service.spreadsheets().values().get(spreadsheetId=Spreadsheet_id, range=Range).execute()
        values = result.get('values', [])
        sheet = pd.DataFrame(values, columns=values[0])
        sheet = sheet.drop(0)
        sheet = sheet.reset_index()
        return sheet
    
    def Set_DataFrame(self, Spreadsheet_id:str, Range:str, DataFrame):
        import pandas as pd
        self.service.spreadsheets().values().append(spreadsheetId=Spreadsheet_id,
                                                    valueInputOption="USER_ENTERED",
                                                    range=Range,
                                                    body={"values":DataFrame.values.tolist()}).execute()

    def Set_values(self, Spreadsheet_id:str, Range:str, Values):
        self.service.spreadsheets().values().update(spreadsheetId=Spreadsheet_id,
                                                    valueInputOption="USER_ENTERED",
                                                    range=Range,
                                                    body={"values":[[Values]]}).execute()
    
    def Get_sheets(self, Spreadsheet_id:str):
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=Spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        Sheet_Name = [Sheet_Name["properties"]["title"] for Sheet_Name in sheets]
        return Sheet_Name
    
    def Clear(self, Spreadsheet_id:str, Range:str):
        self.service.spreadsheets().values().clear( spreadsheetId=Spreadsheet_id, range=Range).execute()


class Drive:
    def __init__(self):
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive
        import mimetypes
        import os
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)
    
    def Trash(self, DRIVE_ID:str):
        from pprint import pprint
        query = f"'{DRIVE_ID}' in parents and trashed=false"
        file_lists = self.drive.ListFile({'q': query}).GetList()
        for file_id in file_lists:
            f = self.drive.CreateFile({'id': file_id["id"]})
            f.Trash()
    
    def Upload(self, DIR_PATH:str, FILE_NAME:str, FOLDER_ID:str):
        import mimetypes
        mime = mimetypes.guess_type(f"{DIR_PATH}/{FILE_NAME}")[0]
        file_set = self.drive.CreateFile({'title': FILE_NAME, 
                                    'mimeType': mime, 
                                    "parents": [{"id": FOLDER_ID}]})
        file_set.SetContentFile(f"{DIR_PATH}/{FILE_NAME}")
        file_set.Upload()
    
    def Download(self, DRIVE_ID:str, FILE_NAME:str, PATH:str):
        query = f"'{DRIVE_ID}' in parents and trashed=false"
        file_id = self.drive.ListFile({'q': query}).GetList()
        try:
            for i in range(len(file_id)):
                if FILE_NAME == file_id[i]["title"]:
                    f = drive.CreateFile({'id': file_id[i]["id"]})
                    f.GetContentFile(os.path.join(PATH, file_id[i]["title"]))
                    break
        except Exception as e:
            print(e)
    
    def Get_files(self, DRIVE_ID:str):
        from pprint import pprint
        query = f"'{DRIVE_ID}' in parents and trashed=false"
        file_ids = self.drive.ListFile({'q': query}).GetList()
        flist = []
        for file in file_ids:
            flist.append({f'{file["title"]}':f'{file["id"]}'})
        return flist
