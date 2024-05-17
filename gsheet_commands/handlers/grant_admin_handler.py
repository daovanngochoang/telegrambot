from gsheet_commands.handlers.base_handler import BaseHandler, RequestState


class GrantAdminHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        usr_input = req_state.update.message.text
        usr_input = usr_input.replace("/grant_admin", "").strip()
        if usr_input == "":
            await req_state.update.message.reply_text(
                "Missing username!"
            )
        else:
            req_state.chat_data.admins.append(usr_input)
            await req_state.update.message.reply_text(
                f"User {usr_input} is added to admin group!"
            )


class RemoveAdmin(BaseHandler):

    async def _handler(self, req_state: RequestState):
        usr_input = req_state.update.message.text
        usr_input = usr_input.replace("/rm_admin", "").strip()
        if usr_input == "":
            await req_state.update.message.reply_text(
                "Missing username!"
            )
        else:
            if usr_input in req_state.chat_data.admins:
                req_state.chat_data.admins.remove(usr_input)
                await req_state.update.message.reply_text(
                    f"User {usr_input} is removed from admin group!"
                )
            else:
                await req_state.update.message.reply_text(
                    f"User {usr_input} is not in the admin group!"
                )
