from abc import ABC

from gspread import Client
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, CommandHandler

from BaseCmd import BaseCommand
from gsheet_commands.chat_data import ChatData
from gsheet_commands.handlers.error_handler import ErrorHandler
from gsheet_commands.handlers.file.export_data import ExportHandler
from gsheet_commands.handlers.file.open_file_handler import OpenFileHandler, OpenFileInputHandler, ListSheets
from gsheet_commands.handlers.file.publish_to_group_handler import PublishWorksheetHandler, StopSharingHandler
from gsheet_commands.handlers.file.set_sheet_handler import SetSpreadSheetHandler
from gsheet_commands.handlers.file.share_email_handler import EmailValidator, ShareEmailHandler
from gsheet_commands.handlers.grant_admin_handler import GrantAdminHandler, RemoveAdmin
from gsheet_commands.handlers.validators import AdminValidator, RequestState, AnyFileOpenCheck, MemberValidator


class GSheetBaseCommand(BaseCommand, ABC):
    def __init__(self, gsh_client: Client, bot_data: dict[int, ChatData]):
        self.GSClient = gsh_client
        self.bot_data: dict[int, ChatData] = bot_data

    async def get_chat_data(self, update: Update):
        if update.message is not None:
            result = self.bot_data.get(update.message.chat_id)
            if result is None:
                self.bot_data[update.message.chat_id] = ChatData()
                check_admin = (await update.message.chat.get_member(update.message.from_user.id))
                if check_admin.status == ChatMember.OWNER:
                    self.bot_data[update.message.chat_id].admins.append(check_admin.user.username)
            return self.bot_data.get(update.message.chat_id)


class GSheetCommands(GSheetBaseCommand):
    def __init__(self, gsh_client: Client, bot_data: dict[int, ChatData]):
        super().__init__(gsh_client, bot_data)

    async def share(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        chain.set_next(ErrorHandler()).set_next(AnyFileOpenCheck()).set_next(EmailValidator()).set_next(
            ShareEmailHandler(self.GSClient))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def share_to_group(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())  # check if any file is opened
         .set_next(PublishWorksheetHandler()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def open_by_link(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        # set chain
        (chain
         .set_next(ErrorHandler())
         .set_next(OpenFileInputHandler())
         .set_next(OpenFileHandler(self.GSClient))
         )
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def set_sheet(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())  # check if any file is opened
         .set_next(SetSpreadSheetHandler()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def stop_share(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())  # check if any file is opened
         .set_next(StopSharingHandler()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def export(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())
         .set_next(ExportHandler()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def grant_admin(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())
         .set_next(GrantAdminHandler()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def remove_admin(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())
         .set_next(RemoveAdmin()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def list_sheets(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = AdminValidator()
        (chain.set_next(ErrorHandler())
         .set_next(AnyFileOpenCheck())
         .set_next(ListSheets()))  # Publish to group so that member can use it
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    def command_handlers(self) -> list[CommandHandler]:
        return [
            CommandHandler("open", self.open_by_link),
            CommandHandler("publish", self.share_to_group),
            CommandHandler("select", self.set_sheet),
            CommandHandler("ls", self.list_sheets),
            CommandHandler("share", self.share),
            CommandHandler("stop", self.stop_share),
            CommandHandler("export", self.export),
            CommandHandler("grant_admin", self.grant_admin),
            CommandHandler("rm_admin", self.remove_admin)
        ]
