from typing import Optional

from gsheet_commands.handlers.base_handler import RequestState


def extract_worksheet_name(req_state: RequestState) -> Optional[str]:
    user_input = req_state.update.message.text
    user_input = user_input.strip()
    args = user_input.split(" ")
    return " ".join(args[1:]).strip()
