from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.worksheet.extract_name import extract_worksheet_name


class DeleteWorksheetHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):

        new_wsh_name = extract_worksheet_name(req_state)

        list_wsh = req_state.chat_data.worksheets
        len_wsh = len(list_wsh)
        for idx in range(len_wsh):
            if list_wsh[idx].title == new_wsh_name:
                worksheet_id = list_wsh[idx].id

                req_state.chat_data.file.del_worksheet_by_id(
                    worksheet_id
                )

                await req_state.update.message.reply_text(
                    f"Worksheet {new_wsh_name} is deleted successfully!\n"
                )
                list_wsh.pop(idx)
                return

        await req_state.update.message.reply_text(
            f"Worksheet {new_wsh_name} is not existed!"
        )
