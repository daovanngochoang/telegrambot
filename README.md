# telegrambot
Telegram bot - Bot4US

### Bot Description.

1. The admin of a chat is the creator of the chat by default.
2. Admin can add multiple people as admin by their username.
3. File just open 1 file at a time and share 1 Sheet to chat (For security concerns).
4. Members in the chat can edit and query the Sheet only when the admin publishes a sheet to the group.
5. File can be shared over email.
6. The file can be exported as the open-source sheet file format.
7. Data in the sheet can be queried flexibly.
8. Append row, col, get by range, delete by range ...
9. Data can be updated for a particular cell by column name and row.

### Google Sheet File.
-----------------------------------------------

```text
/open - open a file sheet via url
    Usage: open [URL]
    example: '/open https://docs.google.com...

/select_sheet - set worksheet to use command
    Usage: /select_sheet [worksheet name]
    example: /select_sheet Financial Reports

/publish - publish worksheet so that member can use it
    Usage: /publish [worksheet name]
    Example: /publish Financial Reports


/share - share the current file to email
    Usage: /share [gmail]
    Example: abc@gmail.xyz


/stop_publish - stop publish, member will not allowed to access your file and worksheet.
/export - export to open sheet file.
```

### Worksheets.
-----------------------------------------------

```text
/add_worksheet - add new worksheet to the file.
    Usage: /add_worksheet [new worksheet name]
    Example: /add_worksheet Sheet2

/del_worksheet - del worksheet from the file.
    Usage: /del_worksheet [new worksheet name]
    Example: /del_worksheet Sheet2
```

### Worksheet Data.
-----------------------------------------------

```text
/range - get data by range start row to end row
    Usage: /range [r1]:[r2]
    Example: /range 1:10, /range 10:100

/del - delete data by range
    Usage: del [r1]:[r2]
    Example: /del 10:15, /del 15:30

/head - get first 10 rows
/tail - get 10 row at the end.

/add_row - append new row data
    Note: each col is separated by '|'
    Usage:  /add_row  [data]
    Example:  /add_row data1 | data2 | data3 | data4

/add_col - add column by name
    Usage: /add_col  [column_name]
    Example: /add_col  new column name

/query - query data
    Usage: /query [your query]
    Note:
        1. you can query for specific value in column.
        2. column name with 2 or more words will be contain in ' '.
    Example:
        1. /query Role == 'Membership'
        2. /query 'Is Registered' == 'Yes'
        3. /query Role == 'Membership' and 'Is Registered' == 'Yes' and Age >= '30'

/del_col - delete column by name
    Usage: /add_col  [column_name]
    Example: /add_col  new column name

/update_at - update data value by row, colname
    Usage: /update_at  [row] | [col name] | [data]
    Example: /update_at  1 | new column name | This is new column data.
            => Update data at row 1 and column name 'new column name'
               with value 'This is new column data'.```

