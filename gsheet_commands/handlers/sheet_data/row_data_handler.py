from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache


class RowDataHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        row_data = req_state.update.message.text
        row_data = row_data.strip().split(" ")
        df = get_data_in_cache(req_state)
        row, col = df.shape
        error_msg = (f"Not enough data, The current Sheet has {col} columns\n"
                     f" your must provide a list of data d1 | d2 | d3 | d4 | d..{col}"
                     f"\nplease make sure you add enough data!")

        if len(row_data) < 2:
            await req_state.update.message.reply_text(
                error_msg
            )
        else:
            row_data = " ".join(row_data[1:])
            row_data = row_data.split("|")
            row_data = [data.strip() for data in row_data]

            if len(row_data) != col:
                await req_state.update.message.reply_text(
                    error_msg
                )
            else:
                usr_data = self._get_user_data(req_state.update, req_state.ctx)
                usr_data.row_data = row_data
                await self._next(req_state)
