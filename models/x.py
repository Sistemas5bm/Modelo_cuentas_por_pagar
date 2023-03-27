from sqlalchemy import create_engine
import pandas as pd

SERVER='192.168.88.214:49706'
DATABASE='document_b293efb8-0254-4a13-8ab5-dd78af6bfc8b_metadata'
DRIVER='SQL Server'
USERNAME='sa'
PASSWORD='HideMyPassBm123'
DATABASE_CONNECTION= f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

engine = create_engine(DATABASE_CONNECTION)
connection = engine.connect()

query_cp_lotes = pd.read_sql_query("Select nombreemisor from [document_b293efb8-0254-4a13-8ab5-dd78af6bfc8b_metadata].dbo.Comprobante WHERE CONVERT(DATE,fecha) BETWEEN "
                                   "'2021-09-23' AND '2021-09-23' AND UsoCFDI='G01'",connection)

print(query_cp_lotes)