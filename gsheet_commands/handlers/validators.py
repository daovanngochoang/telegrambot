from gsheet_commands.handlers.base_handler import BaseHandler, RequestState


class CheckChatData(BaseHandler):
    async def _handler(self, req_state: RequestState):
        if req_state.chat_data.file is None:
            await req_state.update.message.reply_text("Please open a file first!")
            return
        elif req_state.chat_data.current_worksheet is None:
            await req_state.update.message.reply_text("Please set a work sheet to share to the group!")
            return
        else:
            await self._next(req_state)


class AdminValidator(BaseHandler):
    async def _handler(self, req_state):
        if req_state.update.message is not None:
            if req_state.update.message.from_user.username not in req_state.chat_data.admins:
                await req_state.update.message.reply_text("You are not allowed to do this!")
                return
            else:
                await self._next(req_state)


class MemberValidator(BaseHandler):
    async def _handler(self, req_state):
        if req_state.update.message is not None:
            if (req_state.update.message.from_user.username not in req_state.chat_data.admins
                    and not req_state.chat_data.is_shared):
                await req_state.update.message.reply_text("Chat Data is not shared!")
                return
            else:
                await self._next(req_state)


class AnyFileOpenCheck(BaseHandler):
    async def _handler(self, req_state: RequestState):
        if req_state.chat_data.file is None:
            await req_state.update.message.reply_text(
                "Please open a file first! \n'/open [link]'"
            )
        else:
            await self._next(req_state)
