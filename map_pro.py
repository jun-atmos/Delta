from keplergl import KeplerGl
import pandas as pd
import numpy as np
import os

from preprocessing import *
from api import *
from geofind import *
from map_def import *
from datetime import datetime,timedelta
from pytz import timezone

def map_data_pro(tm2,jeju_aws):
    AWS = pd.read_csv('AWS_Point.csv',  encoding='cp949', header=None, skiprows=20, delim_whitespace=True, on_bad_lines='skip')[:-1]
    AWS = AWS[[0,1,2,8]]
    AWS.columns = ['STN_ID','Longitude', 'Latitude', 'Name']
    stn_AWS = ['870', '965', '869', '868', '871', '867', '782', '753', '980', '780',
            '960', '885', '726', '855', '793', '328', '884', '752', '989', '890',
            '792', '861', '862', '781', '329', '883', '893', '727', '865', '863',
            '182', '725', '330', '751', '724', '990', '993', '779']  #여기에 884가 다운이 안받아져서 따로 추가해야함.
    AWS = AWS[AWS['STN_ID'].isin(stn_AWS)].reset_index(drop=True)


    ASOS = pd.read_csv('ASOS_Point.csv',  encoding='cp949', header=None, skiprows=20, delim_whitespace=True, on_bad_lines='skip')[:-1]
    ASOS = ASOS[[0,1,2,10]]
    ASOS.columns = ['STN_ID','Longitude', 'Latitude', 'Name']
    stn_ASOS = ['182', '184', '185', '188', '189']   #184:제주  /  182:제주공항(공항기상관측AMOS)
    ASOS = ASOS[ASOS['STN_ID'].isin(stn_ASOS)].reset_index(drop=True)

    new_row = pd.DataFrame({'STN_ID':[884], 'Longitude':[126.5176], 'Latitude':[33.2593], 'Name':'서호'})  #여기에 884가 다운이 안받아져서 따로 추가한 것.

    Point = pd.concat([AWS,ASOS, new_row]).reset_index(drop=True)

    wea_api_jeju = preprocessing(0,tm2,jeju_aws)
    vi_api_jeju = preprocessing(2,tm2,jeju_aws)

    Point['STN_ID'] = Point['STN_ID'].astype(str)
    vi_api_jeju['STN_ID'] = vi_api_jeju['STN_ID'].astype(str)

    vi_marge = pd.merge(Point, vi_api_jeju, on='STN_ID', how='inner')

    a = pd.read_csv('aws_data.csv')

    stn_AWS = ['870', '965', '869', '868', '871', '867', '782', '753', '980', '780',
            '960', '885', '726', '855', '793', '328', '884', '752', '989', '890',
            '792', '861', '862', '781', '329', '883', '893', '727', '865', '863',
            '182', '725', '330', '751', '724', '990', '993', '779']  #여기에 '184', '185', '188', '189', '884'가 아예 존재하지 않음. / '993'존재

    # STN_SP : AWS 특성코드
    # HT : AWS 해발고도(m)
    # FCT_ID : 예보구역코드
    # WRN_ID : 특보구역코드

    a['STN_ID'] = a['STN_ID'].astype(str)       #STN_ID를 문자열로.
    filtered_a = a[a['STN_ID'].isin(stn_AWS)].reset_index(drop=True)
    filtered_a.columns = ['STN_ID', 'Name', 'STN_SP', 'Longitude', 'Latitude', 'HT', 'FCT_ID', 'WRN_ID']
        
    # 필요한 변수만 가져오기
    wea_api_jeju = wea_api_jeju[['TIME', 'STN_ID', 'WS10', 'TA', 'RN-15m', 'HM']]
    #cloud_api_jeju = cloud_api_jeju[['TIME', 'STN_ID', 'CA_TOP']]
    vi_api_jeju = vi_api_jeju[['TIME', 'STN_ID', 'VIS1', 'WW1']]

    #병합하기 전에 숫자로 바꾸기
    wea_api_jeju['STN_ID'] = pd.to_numeric(wea_api_jeju['STN_ID'], errors='coerce')
    vi_api_jeju['STN_ID'] = pd.to_numeric(vi_api_jeju['STN_ID'], errors='coerce')

    # 모든 변수를 하나의 DataFrame으로 병합
    total_api = wea_api_jeju.merge(vi_api_jeju, on=["TIME",'STN_ID'], how="outer")
    #total_api = total_api.merge(vi_api_jeju, on=["TIME",'STN_ID'], how="outer")

    # 계절 구분하기
    total_api["Month"] = pd.to_datetime(total_api["TIME"]).dt.month
    total_api["season"] = total_api["Month"].apply(determine_season)

    total_api['RN-15m'] = total_api['RN-15m'].fillna(0)     #15분 누적 강수량의 NaN값은 0으로.

    #위경도 data와 합치기
    Point = Point.sort_values(by='STN_ID').reset_index().drop('index', axis=1)
    Point['STN_ID'] = Point['STN_ID'].astype(str)
    total_api['STN_ID'] = total_api['STN_ID'].astype(str)

    total_marge = pd.merge(Point, total_api, on='STN_ID')   #marge = columns를 기준으로 합치기

    #시정값이 있는 지점과 없는 지점 분리
    known_values = total_marge.dropna(subset=["VIS1"])         #시정에서 NaN을 제외한 나머지.
    unknown_values = total_marge[total_marge["VIS1"].isna()]   #시정이 Nan인 것만. = 채워 넣을 것.

    # NaN 값을 가진 지점 내삽
    for i, row in unknown_values.iterrows():                                                #행을 하나씩 반복(iterate) = index와 data를 하나씩 가져옴. => row는 한 행이자 pd.Series임.
        lat, lon = row["Latitude"], row["Longitude"]
        unknown_values.at[i, "VIS1"] = inverse_distance_weighting(lat, lon, known_values)   #내삽된 값을 unknown_values(dataframe)의 해당 위치에 넣기

    filled_data = pd.concat([known_values, unknown_values]).sort_index()


    total = filled_data.merge(calculation_scores(filled_data), on=["TIME",'STN_ID'], how="outer")

    end = total[['TIME', 'STN_ID', 'Longitude', 'Latitude', 'Name', 'tourism_index']]
    col_min = end['tourism_index'].min()
    col_max = end['tourism_index'].max()
    end['tourism_index'] = (end['tourism_index'] - col_min) / (col_max - col_min) * 100
    end['tourism_index'] = end['tourism_index'].round(3)    #반올림
    end['TIME'] = end['TIME'].astype(str)
    return end, total_api