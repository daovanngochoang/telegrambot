from pandas import DataFrame

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache, load_new_data


async def col_name_extract(req_state: RequestState):
    usr_input = req_state.update.message.text
    usr_input = usr_input.strip().split(" ")

    if len(usr_input) < 2:
        await req_state.update.message.reply_text(
            "Command Panic!!\n"
            "Missing column name, /add_col [column name]"
        )
        return None
    else:
        new_col_name = " ".join(usr_input[1:]).strip()

        return new_col_name


def update(df: DataFrame, req_state: RequestState):
    data = [df.columns.tolist()]
    data.extend(df.values.tolist())

    req_state.chat_data.current_worksheet.update(
        "A:Z",
        data
    )


class AppendColHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        new_col_name = await col_name_extract(req_state)
        df = get_data_in_cache(req_state)

        if new_col_name is not None:
            if new_col_name not in df.columns.tolist():
                df[new_col_name] = ''

                update(df, req_state)

                await req_state.update.message.reply_text(
                    f"New column {new_col_name} is added"
                )
                load_new_data(req_state)
            else:
                await req_state.update.message.reply_text(
                    f"The column is already existed in the Sheet."
                )


class DeleteColHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):
        col_name = await col_name_extract(req_state)

        if col_name is not None:
            df = get_data_in_cache(req_state)
            col_list = df.columns.tolist()
            if col_name in col_list:
                at = col_list.index(col_name)
                req_state.chat_data.current_worksheet.delete_columns(at + 1)
                await req_state.update.message.reply_text(
                    f"Column {col_name} is Dropped!"
                )
                load_new_data(req_state)
            else:
                await req_state.update.message.reply_text(
                    f"Column {col_name} is not existed in the Sheet so no column is dropped!"
                )
