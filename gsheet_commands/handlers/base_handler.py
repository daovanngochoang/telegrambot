from abc import ABC, abstractmethod
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes
from typing_extensions import Self

from gsheet_commands.chat_data import ChatData
from gsheet_commands.user_data import UserData


class RequestState:
    def __init__(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE, chat_data: ChatData):
        self.update: Update = update
        self.ctx: ContextTypes.DEFAULT_TYPE = ctx
        self.chat_data: ChatData = chat_data


class BaseHandler(ABC):
    def __init__(self):
        self._next_handler: Optional[BaseHandler] = None

    def _get_user_data(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> UserData:
        chat_id = update.message.chat_id
        if ctx.user_data.get(chat_id) is None:
            ctx.user_data[chat_id] = UserData()
        u_data: UserData = ctx.user_data.get(chat_id)
        return u_data

    def set_next(self, next_handler) -> Self:
        self._next_handler: Optional[BaseHandler] = next_handler
        return next_handler

    @abstractmethod
    async def _handler(self, req_state: RequestState):
        pass

    async def _next(self, req_state: RequestState):
        if self._next_handler is not None:
            await self._next_handler.handle(req_state)

    async def handle(self, req_state: RequestState):
        await self._handler(req_state)
        del req_state  # delete object after complete request
