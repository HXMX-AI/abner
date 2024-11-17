import pandas as pd


wd    = "C:/Users/ridva/OneDrive/Documents/WELLS/Test_Well/"
fName = "logs v2 14 well Donny Ovintiv.csv"

df = pd.read_csv(wd + fName)

logs = ['UWI','GR','DEPT', 'LLD','LLM','LLS','RHOB','NPHI','DTC','PEF', 'DRHO']

df_short = df[logs].copy()

inventory = df_short.groupby('UWI').count()


uwi_selected  = 5123336320000
df_w          = df[df['UWI'] == uwi_selected][logs].copy()
print(df_w.head())

df_w.to_csv(wd + 'Well_Selected.csv')


print('done')