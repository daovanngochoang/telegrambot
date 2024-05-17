from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from gsheet_commands.gsheet_commands import GSheetBaseCommand
from gsheet_commands.handlers.base_handler import RequestState
from gsheet_commands.handlers.draw_graph.charplot import PlotGraph
from gsheet_commands.handlers.draw_graph.utils import GraphTypes
from gsheet_commands.handlers.error_handler import ErrorHandler
from gsheet_commands.handlers.validators import MemberValidator, CheckChatData


class PlotCommand(GSheetBaseCommand):

    def command_handlers(self) -> list[CommandHandler]:
        return [
            CommandHandler("barplot", self.bar_plot),
            CommandHandler("lineplot", self.line_plot),
            CommandHandler("histogramplot", self.histogram_plot),
            CommandHandler("areaplot", self.area_plot),

        ]

    async def bar_plot(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain
         .set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(PlotGraph(type=GraphTypes.bar)))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def area_plot(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain
         .set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(PlotGraph(type=GraphTypes.area)))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def histogram_plot(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain
         .set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(PlotGraph(type=GraphTypes.histogram)))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))

    async def line_plot(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        chain = MemberValidator()
        (chain
         .set_next(ErrorHandler())
         .set_next(CheckChatData())
         .set_next(PlotGraph(type=GraphTypes.line)))
        await chain.handle(RequestState(update, ctx, await self.get_chat_data(update)))
