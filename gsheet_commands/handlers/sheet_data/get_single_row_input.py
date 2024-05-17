from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.user_data import UserData


# class GetSingleRowInputHandler(BaseHandler):
#
#     async def _handler(self, req_state: RequestState):
#         usr_input = req_state.update.message.text
#         usr_input = usr_input.strip().split()
#         if len(usr_input) < 2:
#             await req_state.update.message.reply_text(
#                 "Missing input data"
#             )
#         else:
#             row: str
#             row = " ".join(usr_input[1:]).strip()
#             if not row.isnumeric():
#                 await req_state.update.message.reply_text(
#                     "Invalid Row, its must be a number!"
#                 )
#             else:
#                 usr_data: UserData = self._get_user_data(req_state.update, req_state.ctx)
#                 usr_data.row = int(row)
#                 await self._next(req_state)
