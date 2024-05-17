import validators
from gspread import Client, Spreadsheet

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.user_data import UserData


class EmailValidator(BaseHandler):
    def __init__(self):
        super().__init__()
        self.roles = ["reader", "writer"]

    async def _handler(self, req_state: RequestState):
        user_input = req_state.update.message.text
        user_input = user_input.strip().split(" ")

        if len(user_input) < 2:
            await req_state.update.message.reply_text(
                "Missing email!, Make sure you use the right format "
                "\n'/share [email] [role[reader, writer] default is reader]'"
            )

        else:
            user_input = " ".join(user_input[1:]).strip().split(" ")

            if len(user_input) == 1:
                email = user_input[-1]
                role = self.roles[0]

            else:
                email = user_input[0]
                role = user_input[-1]

            if validators.email(email):
                if role not in self.roles:
                    await req_state.update.message.reply_text(
                        "in valid role, role should be one of [reader, writer] "
                    )
                    return
                    # get user data
                u_data: UserData = self._get_user_data(req_state.update, req_state.ctx)
                u_data.gmail_to_share = email
                u_data.role = role
                await self._next(req_state)

                # Remove after share!
                u_data.gmail_to_share = None
                u_data.role = None

            else:
                await req_state.update.message.reply_text(
                    "The email is in valid!"
                )


class ShareEmailHandler(BaseHandler):
    def __init__(self, gsheet_client: Client):
        super().__init__()
        self.gsheet_client = gsheet_client

    async def _handler(self, req_state: RequestState):
        u_data: UserData = self._get_user_data(req_state.update, req_state.ctx)
        file: Spreadsheet = req_state.chat_data.file

        file.share(u_data.gmail_to_share, role=u_data.role, perm_type="user")
        await req_state.update.message.reply_text(
            f"You shared a file to {u_data.gmail_to_share}!"
        )
