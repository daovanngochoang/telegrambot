from gspread import Client

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState


class SetDrive(BaseHandler):
    def __init__(self, gsheet_client: Client):
        super().__init__()
        self.gsheet_client = gsheet_client

    async def _handler(self, req_state: RequestState):
        user_input = req_state.update.message.text
        user_input = user_input.strip().split(" ")
        if len(user_input) < 2:
            await req_state.update.message.reply_text(
                "Missing Folder ID."
            )
        else:
            req_state.chat_data.drive_folder = user_input
