from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from gsheet_commands.gsheet_commands import GSheetBaseCommand
from gsheet_commands.handlers.base_handler import RequestState
from gsheet_commands.handlers.error_handler import ErrorHandler
from gsheet_commands.handlers.sheet_data.add_data_by_row_col import AddDataByRowColHandler, AddCellDataInPutHandler
from gsheet_commands.handlers.sheet_data.apprend_rows_handler import AppendRowHandler
from gsheet_commands.handlers.sheet_data.col_handler import AppendColHandler, DeleteColHandler
from gsheet_commands.handlers.sheet_data.delete_data import DeleteDataByRange
from gsheet_commands.handlers.sheet_data.get_data_by_range import GetDataByRangeHandler, GetHeadDataHandler, \
    GetTailDataHandler
from gsheet_commands.handlers.sheet_data.query import QueryDataHandler
from gsheet_commands.handlers.sheet_data.range_input_handler import ExtractRangeFromInput
from gsheet_commands.handlers.sheet_data.row_data_handler import RowDataHandler
from gsheet_commands.handlers.validators import MemberValidator, CheckChatData


class DataCommands(GSheetBaseCommand):
    def command_handlers(self) -> list[CommandHandler]:
        return [
            CommandHandler("range", self.get_by_range),
            CommandHandler("del", self.delete_by_range),
            CommandHandler("head", self.head),
            CommandHandler("tail", self.tail),
            CommandHandler("add_row", self.append_rows),
            CommandHandler("add_col", self.append_cols),
            CommandHandler("query", self.query),
            CommandHandler("del_col", self.del_col),
            CommandHandler("update_at", self.update_at),
        ]

    async def update_at(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(AddCellDataInPutHandler())
         .set_next(AddDataByRowColHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def del_col(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(DeleteColHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def head(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(GetHeadDataHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def query(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(QueryDataHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def tail(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(GetTailDataHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def append_rows(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(RowDataHandler())
         .set_next(AppendRowHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def append_cols(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(AppendColHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def get_by_range(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(ExtractRangeFromInput())
         .set_next(GetDataByRangeHandler()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def delete_by_range(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(ExtractRangeFromInput())
         .set_next(DeleteDataByRange()))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))
