from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.file.open_file_handler import show_worksheets
from gsheet_commands.handlers.file.utils import is_sheet_valid
from gsheet_commands.handlers.worksheet.extract_name import extract_worksheet_name


class PublishWorksheetHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):

        input_worksheet = extract_worksheet_name(req_state)

        if req_state.chat_data.current_worksheet is not None:
            req_state.chat_data.is_shared = True
            await req_state.update.message.reply_text(
                f"{req_state.chat_data.current_worksheet.title} is shared to your chat members!"
            )
        else:
            valid, wsh = is_sheet_valid(input_worksheet, req_state)
            if valid:
                # if the input sheet exist => set and return
                if wsh.id == input_worksheet or wsh.title == input_worksheet:
                    req_state.chat_data.current_worksheet = wsh
                    req_state.chat_data.is_shared = True
                    await req_state.update.message.reply_text(
                        f"{wsh.title} is shared to your chat members!"
                    )
            else:
                # if input sheet is not exist -> send error
                _, msg = show_worksheets(req_state)
                await req_state.update.message.reply_text(
                    f"Your worksheet '{input_worksheet}' is not exist in {msg} "
                )


class StopSharingHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        req_state.chat_data.is_shared = False
        await req_state.update.message.reply_text(
            "Stop sharing!"
        )
