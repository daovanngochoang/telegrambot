from typing import Optional

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache, send_data


class GetDataByRangeHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):
        df = get_data_in_cache(req_state)
        usr_data = self._get_user_data(req_state.update, req_state.ctx)
        await send_data(df, req_state, usr_data.start_row, usr_data.end_row)


class GetHeadDataHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):
        df = get_data_in_cache(req_state)

        if len(df) > 0:
            true, size = get_size_arg(req_state.update.message.text, "/head")

            if not true:
                await req_state.update.message.reply_text(
                    "The argument you enter is invalid, it must be a number."
                )
                return

            start = 0
            end = min(size, len(df))

            await send_data(df, req_state, start, end)
        else:
            await req_state.update.message.reply_text(
                f"Sheet {req_state.chat_data.current_worksheet.title} is empty!"
            )


class GetTailDataHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):

        df = get_data_in_cache(req_state)
        if len(df) == 0:
            await req_state.update.message.reply_text(
                f"Sheet {req_state.chat_data.current_worksheet.title} is empty!"
            )
        else:
            true, size = get_size_arg(req_state.update.message.text, "/tail")

            if not true:
                await req_state.update.message.reply_text(
                    "The argument you enter is invalid, it must be a number."
                )
                return

            start = max(0, len(df) - size)
            end = len(df)
            await send_data(df, req_state, start, end)


def get_size_arg(txt: str, cmd: str) -> tuple[bool, Optional[int]]:
    usr_input = txt.replace(cmd, "").strip()
    if usr_input != "" and usr_input.isdigit():
        size = int(usr_input)
        return True, size
    elif usr_input != "" and not usr_input.isdigit():
        return False, None
    return True, 10
