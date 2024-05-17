import os
from datetime import datetime

import dataframe_image as dfi
import pandas as pd
from pandas import DataFrame

from gsheet_commands.handlers.base_handler import RequestState


async def send_data_frame(df: DataFrame, req_data: RequestState):
    pd.set_option("display.max_column", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option('display.width', -1)
    pd.set_option('display.max_rows', None)

    path = f"tmp/sheet_of_{req_data.update.message.chat.username}_chat_{req_data.update.message.id}.png"

    if len(df) < 3:
        # df.add(axis='rows', fill_value="")
        row = []
        for i in range(3):
            row.append([" " for j in df.columns])

        new_df = DataFrame(row)
        new_df.columns = df.columns

        df = pd.concat([df, new_df])

    dfi.export(
        df,
        path,
        table_conversion="matplotlib"
    )

    await req_data.update.message.reply_photo(path)

    # remove image
    os.remove(path)


def check_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False


def convert_dtypes(df: DataFrame):
    for col in df.columns:
        head = df[[col]].head(10).values.tolist()
        list_data = []

        for i in head:
            if len(i) > 0:
                list_data.append(i[0])

        is_int = False
        is_float = False
        item: str

        for item in list_data:
            if item is not None and item.isdigit():
                is_int = True
            elif item is not None and check_float(item):
                is_float = True
        if is_int and is_float or is_float:
            df[[col]] = df[[col]].astype(dtype="float", errors='ignore')
        elif is_int:
            df[[col]] = df[[col]].astype(dtype="int", errors='ignore')

    df.fillna(value="", inplace=True)


def load_new_data(req_data: RequestState):
    data = req_data.chat_data.current_worksheet.get(
        "A:Z"
    )

    df: DataFrame = DataFrame(data)
    if len(df) > 0:
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        convert_dtypes(df)
        req_data.chat_data.data_frame_table = df
        req_data.chat_data.last_update_cache = datetime.now()
        return req_data.chat_data.data_frame_table
    return df


def get_data_in_cache(req_data: RequestState) -> DataFrame:
    chat_data = req_data.chat_data
    if chat_data.last_update_cache is not None:
        time_duration = datetime.now() - chat_data.last_update_cache

        if chat_data.data_frame_table is not None and time_duration.seconds < chat_data.cache_expired:
            return chat_data.data_frame_table

    return load_new_data(req_data)


async def send_data(df, req_state: RequestState, start, end):
    if start > len(df):
        await req_state.update.message.reply_text(
            f"Invalid range, the sheet has only {df.shape[0]} rows"
        )
        return
    if start == end:
        df_to_send = df.iloc[[start - 1]]
        await req_state.update.message.reply_text(
            "Request: 1\n"
            f"Total: {df.shape[0]}\n"
            f"Response: 1"
        )
        await send_data_frame(df_to_send, req_state)
    else:
        if end - start > 50:
            end = start + 50

        end = min(end, len(df))

        df_to_send = df[max(start - 1, 0):end]

        await req_state.update.message.reply_text(
            f"Total: {df.shape[0]}\n"
            f"Response: {end - start}\n" +
            (f"due to data limitation" if end - start > 50 else "")
        )
        await send_data_frame(df_to_send, req_state)
