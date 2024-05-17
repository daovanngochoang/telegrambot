from gspread import Worksheet

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.worksheet.extract_name import extract_worksheet_name


class CreateWorksheetHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):
        new_worksheet_name = extract_worksheet_name(req_state)
        if new_worksheet_name != "":
            created_worksheet: Worksheet = req_state.chat_data.file.add_worksheet(
                new_worksheet_name,
                rows=100,
                cols=100
            )

            req_state.chat_data.worksheets.append(created_worksheet)
            await req_state.update.message.reply_text(
                f"Worksheet {created_worksheet.title} is added successfully!\nURL: {created_worksheet.url}"
            )
        else:
            await req_state.update.message.reply_text(
                f"Missing Worksheet's name!"
            )
