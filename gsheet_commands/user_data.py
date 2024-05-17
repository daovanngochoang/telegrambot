from typing import Optional


class UserData:
    def __init__(self):
        # self.current_sheet: Optional[Worksheet] = None
        self.url: Optional[str] = None

        self.selected_range: str = "A:Z"
        self.start_row: Optional[int] = None
        self.end_row: Optional[int] = None
        self.row_data: Optional[list] = None

        self.row: Optional[int] = None
        self.col: Optional[int] = None
        self.col_name: Optional[str] = None
        self.cell_data: Optional[str] = None

        self.gmail_to_share: Optional[str] = None
        self.role: str = 'reader'
        self.input_worksheet_name: Optional[str] = None
