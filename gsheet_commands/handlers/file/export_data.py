from gspread.utils import ExportFormat

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState


class ExportHandler(BaseHandler):
    async def _handler(self, req_state: RequestState):
        byte_data: bytes = req_state.chat_data.file.export(
            format=ExportFormat.OPEN_OFFICE_SHEET
        )
        await req_state.update.message.reply_document(
            document=byte_data,
            caption=req_state.chat_data.file.title,
            filename=req_state.chat_data.file.title
        )
