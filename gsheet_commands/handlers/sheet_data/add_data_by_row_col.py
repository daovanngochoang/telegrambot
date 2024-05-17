from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache, load_new_data


class AddCellDataInPutHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        usr_data = self._get_user_data(req_state.update, req_state.ctx)
        usr_input = req_state.update.message.text
        usr_input = usr_input.strip().split(" ")
        if len(usr_input) < 2:
            await req_state.update.message.reply_text(
                "Missing Arguments, your have to provide [row] | [colname] | data!"
            )
        else:
            usr_input = " ".join(usr_input[1:]).strip().split("|")
            usr_input = [ip.strip() for ip in usr_input]

            if len(usr_input) < 3:
                await req_state.update.message.reply_text(
                    "Not Enough arguments, [row] | [colname] | Data"
                )
            else:
                usr_data.row = int(usr_input[0])
                usr_data.col_name = usr_input[1]
                usr_data.cell_data = usr_input[2]

                await self._next(req_state)


class AddDataByRowColHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):
        df = get_data_in_cache(req_state)
        usr_data = self._get_user_data(req_state.update, req_state.ctx)
        list_cols = df.columns.tolist()
        if usr_data.col_name in list_cols:
            at = list_cols.index(usr_data.col_name)
            req_state.chat_data.current_worksheet.update_cell(usr_data.row + 1, at + 1, usr_data.cell_data)
            await req_state.update.message.reply_text(
                f"Data Added to row {usr_data.row} at colum {usr_data.col_name} successfully"
            )
            load_new_data(req_state)
        else:
            await req_state.update.message.reply_text(
                f"Column {usr_data.col_name} not exist in Sheet!"
            )
