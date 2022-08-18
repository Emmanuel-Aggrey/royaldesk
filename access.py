

import pandas_access as mdb

db_filename = '20220701.mdb'

# Listing the tables.
# for tbl in mdb.list_tables(db_filename):
    # print(tbl)
    # pass

# print(help(mdb))

# Read a small table.
# df = mdb.read_table(db_filename, "Userinfo")

# print(df)


d = mdb.read_table(db_filename, "SELECT * FROM Dept")

print(d)