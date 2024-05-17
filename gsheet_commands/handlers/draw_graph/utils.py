from typing import Optional, Union

from gsheet_commands.handlers.base_handler import RequestState

arg_x = "x="
arg_y = "y="
arg_color = "color="
separator = ","
separator_bound_left = "["
separator_bound_right = "]"


class GraphTypes:
    area = "area"
    bar: str = "bar"
    histogram = "histogram"
    line = "line"


def remove_special_char(input_txt: str) -> str:
    return input_txt.strip().replace(separator_bound_left, "").replace(separator_bound_right, "")


def get_args(input_txt: str, arg: str) -> Optional[Union[list, str]]:
    args_data: Optional[Union[list, str]] = None
    if arg in input_txt.strip():
        input_txt = input_txt.replace(arg, "")
        if (separator in input_txt
                and separator_bound_left in input_txt
                and separator_bound_right in input_txt
        ):
            split = input_txt.split(",")
            args_data = [spl.strip() for spl in split]
            args_data = [remove_special_char(ag) for ag in args_data]
        elif (separator not in input_txt
              and separator_bound_left not in input_txt
              and separator_bound_right not in input_txt
        ):
            args_data = input_txt.strip()
    return args_data


async def get_column_from_input(cmds: list[str], req_state: RequestState) \
        -> tuple[Optional[Union[list, str]], Optional[Union[list, str]], Optional[Union[list, str]], Optional[
            Union[list, str]]]:
    usr_input = req_state.update.message.text

    for cmd in cmds:
        usr_input = usr_input.replace(f"/{cmd}plot", "").strip()

    x: Optional[Union[list, str]] = None
    y: Optional[Union[list, str]] = None
    color: Optional[Union[list, str]] = None
    query_part: Optional[str] = None
    args_part: Optional[str] = None

    if usr_input == "":
        await req_state.update.message.reply_text(
            "Command is invalid, please read the command guideline using\n"
            "/help plot"
        )
    else:
        if "where" in usr_input:
            usr_input = usr_input.split("where")
            if len(usr_input) < 2:
                await req_state.update.message.reply_text(
                    "Invalid Query, please use /help plot for more information!"
                )
            else:
                args_part = usr_input[0]
                query_part = usr_input[1]
        else:
            args_part = usr_input

        args_list: list = args_part.split("|")

        for ip in args_list:
            if x is None:
                x = get_args(ip, arg_x)
            if y is None:
                y = get_args(ip, arg_y)
            if color is None:
                color = get_args(ip, arg_color)

        return x, y, color, query_part
