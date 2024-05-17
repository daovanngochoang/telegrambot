from datetime import datetime
from typing import Optional

from gspread import Spreadsheet, Worksheet
from pandas import DataFrame

white_list = ["andreas_solarstorm"]


class ChatData:
    def __init__(self):
        self.is_shared: bool = False
        self.admins: list[str] = white_list

        self.drive_folder: Optional[str] = None
        self.file: Optional[Spreadsheet] = None
        self.worksheets: list[Worksheet] = []
        self.worksheet_expired: int = 90
        self.worksheet_last_fetch: Optional[datetime] = None
        self.current_worksheet: Optional[Worksheet] = None

        self.data_frame_table: Optional[DataFrame] = None  # Caching the current sheet data!
        self.cache_expired: int = 90
        self.last_update_cache: Optional[datetime] = None
