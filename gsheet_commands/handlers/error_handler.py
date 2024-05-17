from gsheet_commands.handlers.base_handler import BaseHandler, RequestState


class ErrorHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        try:
            await self._next(req_state)
        except Exception as ex:
            await req_state.update.message.reply_text(
                f"Cannot Run Command '{req_state.update.message.text}'"
                f", \nContact developer for feedback the Unexpected Error."
            )
