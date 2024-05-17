import validators
from gspread import Client, Spreadsheet

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.file.utils import show_worksheets
from gsheet_commands.user_data import UserData


class OpenFileInputHandler(BaseHandler):

    async def _handler(self, req_state):
        user_input = req_state.update.message.text
        user_input = user_input.strip()

        args = user_input.split(" ")
        if len(args) >= 2 and validators.url(args[-1]):
            u_data: UserData = self._get_user_data(req_state.update, req_state.ctx)
            u_data.url = args[-1]
            await self._next(req_state)

        else:
            await req_state.update.message.reply_text(
                "The input message is invalid, it's must be a link to google sheet!"
            )
            return


class OpenFileHandler(BaseHandler):
    def __init__(self, gsheet_client: Client):
        super().__init__()
        self.gsheet_client = gsheet_client

    async def _handler(self, req_state):
        u_data = self._get_user_data(req_state.update, req_state.ctx)
        file: Spreadsheet = self.gsheet_client.open_by_url(u_data.url)
        req_state.chat_data.file = file
        req_state.chat_data.worksheets = file.worksheets()
        req_state.chat_data.current_worksheet = None

        n_wsh, msg = show_worksheets(req_state)

        await req_state.update.message.reply_text(
            f"File is opened! \nTotal sheet in this file is {n_wsh}\n{msg}"
        )


class ListSheets(BaseHandler):
    async def _handler(self, req_state: RequestState):
        n_wsh, msg = show_worksheets(req_state)
        await req_state.update.message.reply_text(
            f"Total sheet in this file is {n_wsh}\n{msg}"
        )
