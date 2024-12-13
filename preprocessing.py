import pandas as pd
import numpy as np

def jeju_aws():
  stn_name = ['진달래밭', '한라산남벽', '영실', '사제비', '윗세오름', '삼각봉', '성판악', '어리목', '강정', '제주남원', '지귀도', '한남', '마라도', '가파도', '대정', '중문', '서귀포', '서호', '성산', '서광', '안덕화순', '제주가시리', '표선', '제주', '제주김녕', '송당', '구좌', '산천단', '새별오름', '애월', '유수암', '오등', '외도', '제주(공)', '우도', '대흘', '와산', '추자도', '고산', '낙천', '제주금악', '한림']
  stn_num = ['870', '965', '869', '868', '871', '867', '782', '753', '980', '780', '960', '885', '726', '855', '793', '328', '189', '884', '188', '752', '989', '890', '792', '184', '861', '862', '781', '329', '883', '893', '727', '865', '863', '182', '725', '330', '751', '724', '185', '990', '993', '779']

  # Create the DataFrame
  jeju_aws = pd.DataFrame({
      'STN_NAME': stn_name,
      'STN_ID': stn_num
  })

  jeju_aws['STN_ID'] = pd.to_numeric(jeju_aws['STN_ID'], errors='coerce').astype('Int64')
  return jeju_aws

def preprocessing(n,tm2,jeju_aws):
  filename = [f'/workspaces/Delta/weather_csv/wea_{tm2}.csv',f'/workspaces/Delta/weather_csv/cloud_{tm2}.csv',f'/workspaces/Delta/weather_csv/vi_{tm2}.csv']
  df_coloums=[
      ['TIME', 'STN_ID', 'WD1', 'WS1', 'WDS', 'WSS', 'WD10', 'WS10', 'TA','RE', 'RN-15m', 'RN-60m', 'RN-12H', 'RN-DAY', 'HM', 'PA', 'PS', 'TD'],
      ['TIME', 'STN_ID', 'LON', 'LAT', 'CH_LOW', 'CH_MID', 'CH_TOP', 'CA_TOP'],
      ['TIME', 'STN_ID', 'LON', 'LAT', 'S', 'VIS1', 'VIS10', 'WW1', 'WW15']
  ]
  df = pd.read_csv(f'{filename[n]}',encoding='cp949',skiprows=22,header=None)
  df = df.iloc[:-1, :-1]
  df.columns = df_coloums[n]
  df['STN_ID'] = df['STN_ID'].astype(int)
  df_jeju = df[df['STN_ID'].isin(jeju_aws['STN_ID'])]
  df_jeju = df_jeju.reset_index(drop=True)
  df_jeju = df_jeju.apply(pd.to_numeric, errors='coerce')
  df_jeju[df_jeju < -50] = np.nan
  df_jeju['TIME']= df_jeju['TIME'].astype('str')
  df_jeju['TIME']= pd.to_datetime(df_jeju['TIME'])
  return df_jeju

