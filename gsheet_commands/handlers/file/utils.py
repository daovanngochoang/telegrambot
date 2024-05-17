from datetime import datetime
from typing import Optional

from gspread import Worksheet

from gsheet_commands.handlers.base_handler import RequestState


def is_sheet_valid(input_worksheet: str, req_state: RequestState) -> tuple[bool, Optional[Worksheet]]:
    # if the input sheet is exits in the file
    for wsh in req_state.chat_data.worksheets:

        # if the input sheet exist => set and return
        if wsh.id == input_worksheet or wsh.title == input_worksheet:
            return True, wsh

    return False, None


def show_worksheets(req_data: RequestState) -> tuple[int, str]:
    worksheets: list[Worksheet]
    chat_data = req_data.chat_data
    if (chat_data.worksheet_last_fetch is not None
            and chat_data.worksheets is not None
            and len(chat_data.worksheets) > 0
            and (datetime.now() - chat_data.worksheet_last_fetch).seconds < chat_data.worksheet_expired):
        worksheets = chat_data.worksheets
    else:
        worksheets = chat_data.file.worksheets()
    msg = ""
    for idx in range(len(worksheets)):
        msg += f"\n{idx + 1}: {worksheets[idx].title}"
    return len(worksheets), msg
