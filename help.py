from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from BaseCmd import BaseCommand
from commands.commands import *


class HelpCommands(BaseCommand):

    def __init__(self):
        self.cmds = {
            "open": open_file,
            "select": select_sheet,
            "publish": publish,
            "share": share,
            "stop": stop_publish,
            "export": export,
            "add_worksheet": add_worksheet,
            "del_worksheet": del_worksheet,
            "range": get_range,
            "del": delete,
            "head": head,
            "tail": tail,
            "add_col": add_col,
            "query": query,
            "del_col": del_col,
            "update_at": update_at,
            "plot": plot
        }

    def command_handlers(self) -> list[CommandHandler]:
        return [
            CommandHandler(["help", "start"], self.help),
        ]

    async def help(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_photo("commands/banner.png")

        usr_input = update.message.text
        usr_input = usr_input.replace("/help", "").replace("/start", "").strip()
        if usr_input == "":
            msg = ""
            with open("commands/cmd") as file:
                for line in file:
                    msg += f"{line}"
            await update.message.reply_text(msg, parse_mode="HTML")
        elif usr_input in self.cmds.keys():
            await update.message.reply_text(
                header +
                "\n\nDetail Usage:\n" +
                self.cmds.get(usr_input.strip())
            )
        else:
            await update.message.reply_text(
                "Command not found!"
            )
