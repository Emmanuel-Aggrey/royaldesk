import pyodbc 

conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};" + "SERVER=APP-SERVER-RCH;"
            "DATABASE=anviz;"
            "UID=rch-sql-server;"
            "PWD=3marymoney500%@;")
            # 3marymoney500%
cursor = conn.cursor()



sql = "SELECT [Department], Count(case Status when 'In' then 1 end) as Count_In, Count(case Status when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Clean_Data] WHERE [Status] in ('In', 'Out') AND Date='2022-08-06'   GROUP BY [Department] ORDER BY [Department]" 

sql3 = "SELECT 'Department',[Department], 'In' as [Status In], Count(case Status when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case Status when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Clean_Data] WHERE [Status] in ('In', 'Out') AND Date='2022-08-06' AND Name LIKE '%Teye'  GROUP BY [Department] ORDER BY [Department]" 

sql1= "SELECT * FROM dbo.V_Clean_Data WHERE [Date] = '2022-08-04' ORDER BY [Date] ASC"
sql2 ="SELECT * FROM dbo.V_Clean_Data"



cursor.execute(sql2)
for row in cursor:
    print(row)





