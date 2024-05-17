from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import load_new_data


class AppendRowHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        usr_data = self._get_user_data(
            req_state.update,
            req_state.ctx
        )
        row_data = usr_data.row_data
        req_state.chat_data.current_worksheet.append_row(row_data)
        await req_state.update.message.reply_text(
            "Row is appended successfully!"
        )
        load_new_data(req_state)
