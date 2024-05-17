import os
from datetime import datetime

import plotly.express as px

from gsheet_commands.handlers.base_handler import BaseHandler, RequestState
from gsheet_commands.handlers.draw_graph.utils import get_column_from_input, GraphTypes
from gsheet_commands.handlers.sheet_data.query import query
from gsheet_commands.handlers.sheet_data.utils import get_data_in_cache


class PlotGraph(BaseHandler):
    def __init__(self, type='histogram'):
        super().__init__()
        self.graph_type: str = type

    async def _handler(self, req_state: RequestState):
        cmds = [GraphTypes.histogram, GraphTypes.bar, GraphTypes.line, GraphTypes.area]

        x, y, color, query_str = await get_column_from_input(cmds, req_state)
        df = get_data_in_cache(req_state)

        if query_str is not None:
            df = query(df, query_str)

        path = f"tmp/bar_plot_of_{req_state.update.message.chat.username}_chat_{req_state.update.message.id}_{datetime.now()}.png"

        try:
            if self.graph_type == GraphTypes.histogram:
                fig = px.histogram(df, x, y, color=color)
                fig.write_image(path)
            elif self.graph_type == GraphTypes.bar:
                fig = px.bar(df, x, y, color=color)
                fig.write_image(path)
            elif self.graph_type == GraphTypes.line:
                fig = px.line(df, x, y, color=color)
                fig.write_image(path)
            elif self.graph_type == GraphTypes.area:
                fig = px.area(df, x, y, color=color)
                fig.write_image(path)
            await req_state.update.message.reply_photo(
                path
            )
            os.remove(path)
        except Exception as err:
            print(err)
            await  req_state.update.message.reply_text(
                "Cannot Plot Graph, Please check the command again!"
            )
