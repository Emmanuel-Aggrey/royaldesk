import pandas
import pyodbc 
from HRMSPROJECT import sql_server




# sql =  "SELECT TOP 1  FROM [anviz].[dbo].[Userinfo] ORDER BY UserCode;"
# sql = "SELECT  COUNT([Userid]) FROM [anviz].[dbo].[MemStat];"
sql = "SELECT MAX(cast(Userid as int))   FROM [anviz].[dbo].[Userinfo]"
# Userid
nums = ()

cursor = sql_server.cursor.execute(sql)
rows = cursor.fetchone()

values = (*nums,rows[0],23)
print(values)
# engine = create_engine("access:///?DataSource=20220701.mdb")

# conn = pyodbc.connect(
#             "DRIVER={ODBC Driver 17 for SQL Server};" + "SERVER=APP-SERVER-RCH;"
#             "DATABASE=anviz;"
#             "UID=rch-sql-server;"
#             "PWD=3marymoney500%;")

# # sql2 ="SELECT Department FROM dbo.V_Clean_Data"
# sql3 = "SELECT [Department], 'In' as [Status In], Count(case Status when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case Status when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Clean_Data] WHERE [Status] in ('In', 'Out') AND Date='2022-08-06' AND Name LIKE '%Teye'  GROUP BY [Department] ORDER BY [Department]" 


# df = pandas.read_sql(sql3, conn)
# df.to_csv('clean_data.csv')

# print(df)


