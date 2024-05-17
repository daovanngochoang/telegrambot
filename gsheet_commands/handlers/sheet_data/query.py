from pandas import DataFrame

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache, send_data

cmd = "/query"


def has_bool(q: str):
    lower = q.lower()
    return "yes" in lower or "no" in lower or "true" in lower or "false" in lower


def has_and(q: str):
    return "and" in q


def process_query(q: str):
    bool_part = []
    rest = []
    if has_bool(q):
        if has_and(q):
            split = q.split("and")
            for ip in split:
                if has_bool(ip):
                    bool_part.append(ip.strip())
                else:
                    rest.append(ip.strip())
        else:
            bool_part.append(q)
    else:
        return [], [q]
    return bool_part, rest


def query(data: DataFrame, q: str):
    bol, nor = process_query(q)
    result: DataFrame = data
    for que in bol:
        col, val = que.split("==")
        col = col.strip()
        val = val.strip()

        result = result[result[f"{col}".replace("'", "")] == f"{val}".replace("'", "")]
    nor_que = ""
    if len(nor) > 0:
        if len(nor) > 1:
            nor_que = " and ".join(nor)
        elif len(nor) == 1:
            nor_que = nor[0]
        result = result.query(nor_que)
    return result


class QueryDataHandler(BaseHandler):

    async def _handler(self, req_state: RequestState):
        usr_input = req_state.update.message.text

        usr_input = usr_input.strip().replace(cmd, "")
        if usr_input == "":
            await req_state.update.message.reply_text(
                "Missing Query data!"
            )
        else:
            try:
                usr_input = usr_input.strip()

                df = get_data_in_cache(req_state)

                result = query(df, usr_input)

                if len(result) > 0:
                    start = 0
                    end = len(result)
                    await send_data(result, req_state, start, end)
                else:
                    await req_state.update.message.reply_text(
                        f"No Result found for query {usr_input}"
                    )

            except Exception as ex:
                if type(ex) == KeyError:
                    await req_state.update.message.reply_text(
                        "Wrong column name!"
                    )

                else:
                    await req_state.update.message.reply_text(
                        "The query you just sent is not correct, use /help to read more"
                    )
