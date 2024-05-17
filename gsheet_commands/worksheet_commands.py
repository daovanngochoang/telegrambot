from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from gsheet_commands.gsheet_commands import GSheetBaseCommand
from gsheet_commands.handlers.base_handler import RequestState
from gsheet_commands.handlers.error_handler import ErrorHandler
from gsheet_commands.handlers.validators import MemberValidator, CheckChatData, AdminValidator
from gsheet_commands.handlers.worksheet.create_worksheet import CreateWorksheetHandler
from gsheet_commands.handlers.worksheet.delete_work_sheet import DeleteWorksheetHandler


class WorksheetCommands(GSheetBaseCommand):

    def command_handlers(self) -> list[CommandHandler]:
        return [
            CommandHandler("add_worksheet", self.add),
            CommandHandler("del_worksheet", self.delete),
        ]

    async def add(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(CreateWorksheetHandler()))

        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def delete(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):  # only admin can del
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(DeleteWorksheetHandler()))

        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))
