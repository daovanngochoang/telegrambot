from gsheet_commands.handlers.base_handler import BaseHandler, RequestState


class ExtractRangeFromInput(BaseHandler):

    async def _handler(self, req_state: RequestState):

        format_msg = (" the format should be 'r:rn' "
                      "where r is the first row to the row r at n (rn)\n example : '1:2, 1:50 '")
        user_input = req_state.update.message.text
        split_data = user_input.strip().split(" ")
        if len(split_data) < 2:
            await req_state.update.message.reply_text(
                "Missing Range information, " + format_msg
            )
        else:
            user_input = " ".join(split_data[1:]).strip()
            usr_data = self._get_user_data(req_state.update, req_state.ctx)
            if ":" not in user_input:
                if user_input.isnumeric():
                    usr_data.selected_range = f"{user_input}:{user_input}"
                    usr_data.start_row = int(user_input)
                    usr_data.end_row = int(user_input)
                    await self._next(req_state)
                else:
                    await req_state.update.message.reply_text(
                        "The range you entered is wrong format, " + format_msg
                    )
            else:
                r1: int  # start row
                r2: int  # end row

                r1_str, r2_str = user_input.split(":")

                if not r1_str.isnumeric() or not r2_str.isnumeric():
                    await req_state.update.message.reply_text(
                        "The range you entered is wrong format, "
                        "the input range is not a number" + format_msg
                    )
                    return

                r1 = int(r1_str.strip())
                r2 = int(r2_str.strip())
                if r2 < r1:
                    await req_state.update.message.reply_text(
                        f"Invalid range, {r2} < {r1}"
                        + format_msg
                    )

                else:
                    usr_data.selected_range = f"A{r1}:Z{r2}"
                    usr_data.start_row = int(r1)
                    usr_data.end_row = int(r2)
                    await self._next(req_state)
