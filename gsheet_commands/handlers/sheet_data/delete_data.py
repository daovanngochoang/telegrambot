from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache, load_new_data


class DeleteDataByRange(BaseHandler):

    async def _handler(self, req_state: RequestState):
        df = get_data_in_cache(req_state)

        usr_data = self._get_user_data(req_state.update, req_state.ctx)

        start, end = usr_data.start_row, usr_data.end_row

        if start > len(df):
            await req_state.update.message.reply_text(
                f"Invalid range, the sheet has only {df.shape[0]} rows"
            )
            return

        req_state.chat_data.current_worksheet.delete_rows(
            start + 1, end + 1
        )

        await req_state.update.message.reply_text(
            "Success!"
        )

        load_new_data(req_state)
