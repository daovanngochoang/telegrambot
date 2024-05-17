from gspread import Client
from telegram.ext import CommandHandler

from gsheet_commands.chat_data import ChatData
from gsheet_commands.data_commands import DataCommands
from gsheet_commands.gsheet_commands import GSheetCommands
from gsheet_commands.plot_commands import PlotCommand
from gsheet_commands.worksheet_commands import WorksheetCommands


def gsheet_chat_commands(gsheet_client: Client) -> list[CommandHandler]:
    bot_data: dict[int, ChatData] = {}
    spread_sheet_commands = GSheetCommands(gsheet_client, bot_data)
    worksheet_cmd = WorksheetCommands(gsheet_client, bot_data)
    data_cmd = DataCommands(gsheet_client, bot_data)
    plot_cmd = PlotCommand(gsheet_client, bot_data)

    cmds = []
    cmds.extend(spread_sheet_commands.command_handlers())
    cmds.extend(worksheet_cmd.command_handlers())
    cmds.extend(data_cmd.command_handlers())
    cmds.extend(plot_cmd.command_handlers())

    return cmds
