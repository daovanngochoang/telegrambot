open_file = """
/open - open a file sheet via url
    Usage: open [URL]
    example: '/open https://docs.google.com..."""

select_sheet = """
/select - set worksheet to use command
    Usage: /select [worksheet name]
    example: /select Financial Reports"""

publish = """
/publish - publish worksheet so that member can use it
    Usage: /publish [worksheet name]
    Example: /publish Financial Reports"""

share = """
/share - share the current file to email
    Usage: /share [gmail]
    Example: abc@gmail.xyz"""

stop_publish = """/stop_publish - stop publish, member will not allowed to access your file and worksheet."""
export = "/export - export to open sheet file."

add_worksheet = """
/add_worksheet - add new worksheet to the file.
    Usage: /add_worksheet [new worksheet name]
    Example: /add_worksheet Sheet2"""

del_worksheet = """
/del_worksheet - del worksheet from the file.
    Usage: /del_worksheet [new worksheet name]
    Example: /del_worksheet Sheet2
"""

get_range = """
/range - get data by range start row to end row
    Usage: /range [r1]:[r2]
    Example: /range 1:10, /range 10:100
"""

delete = """
/del - delete data by range
    Usage: del [r1]:[r2]
    Example: /del 10:15, /del 15:30"""

head = """/head - get first 10 rows"""
tail = """/tail - get 10 row at the end."""

add_row = """
/add_row - append new row data
    Note: each col is separated by '|'
    Usage:  /add_row  [data]
    Example:  /add_row  data1 | data2 | data3 | data4"""

add_col = """
/add_col - add column by name
    Usage: /add_col  [column_name]
    Example: /add_col  new column name"""

query = """
/query - query data
    Usage: /query [your query]
    Note:
        1. you can query for specific value in column.
        2. Column name are not in ' ' but column name with 2 or more words
           and separated by space will be contain in ' '.
        3. and, in, ><= is works fine!
        4. the value should be in '' too, look at the example below.  
    Example:
        1. /query Role == 'Membership'
        2. /query 'Is Registered' == 'Yes'
        3. /query Role == 'Membership' and 'Is Registered' == 'Yes' and Age >= '30'
        4. /query Role == 'Membership' and 'Is Registered' == 'Yes'
                  and Age >= '30' and LastName == 'Chan'
"""

del_col = """
/del_col - delete column by name
    Usage: /add_col  [column_name]
    Example: /add_col  new column name"""

update_at = """
/update_at - update data value by row, colname
    Usage: /update_at  [row] | [col name] | [data]
    Example: /update_at  1 | new column name | This is new column data.
            
            => Update data at row 1 and column name 'new column name'
               with value 'This is new column data'.
"""

header = """
        BOT4US
The General Assistance.
author: andreas_solarstorm 
"""
plot = """
/areaplot - area plot
/histogramplot - histogram plot
/lineplot - line plot

Usage: [plotcommand] x=colname | y=colname | color=colname where [query]
    1. To plot you must tell the bot the exact column name you want to plot.
    2. x, y is the intercepts of the graph.
    3. each column is separated by '|' symbol.
    4. we can leverage the query power to plot data from query.
Example:
    /areaplot x=Date | y=Volume
    /areaplot x=Date | y=Volume where Date > '2019-06-20'
    /areaplot x=Date | y=Volume where Date > '2019-06-20' and StockSymbol == 'APLE'
"""
