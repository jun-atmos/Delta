from api import *
from rain import *
from geofind import *
from preprocessing import *
from map_pro import *
from map_config import *
from alret import *
from infrared import *
from find_nearest import *
from nearest_tour import *

import streamlit as st
from streamlit_image_comparison import image_comparison
from keplergl import KeplerGl
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings(action='ignore')
from geopy.geocoders import Nominatim
import math
import time
import glob

import matplotlib.image as mpimg
import matplotlib.colorbar as colorbar
import matplotlib.colors as clr
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib.colorbar import ColorbarBase
from IPython.display import display, clear_output

from datetime import datetime,timedelta
from pytz import timezone

st.set_page_config(
   page_title="제주도 날시 기반 관광 추천 알고리즘 by delta team",
   page_icon="🧊",
   layout="wide",
)

jeju_aws = jeju_aws()
tm2 = str(int(datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M')) - 1)
download_file(tm2)
end, total_api = map_data_pro(tm2,jeju_aws)
print(total_api)

col1, col2 = st.columns([3, 2])

with col1:
    tourist_spot = st.text_input("관광지 검색","한라산")
    lat,lon,address = get_location_info(tourist_spot)
    print(lat,lon)

nearest_aws = find_nearest(lat,lon,end)
print(nearest_aws)

col3, col4 = st.columns([3, 2])

with col3:
    config = map_config(lat,lon)
    map_1 = KeplerGl()
    map_1.config = config
    map_1.add_data(data=end, name='AWS&ASOS')

    html_path = 'kepler_map.html'
    map_1.save_to_html(file_name=html_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        kepler_html = f.read()
    st.components.v1.html(kepler_html, height=600)
    st.text("📢 원의 크기가 크고 초록색일수록 관광하기 좋은곳 입니다")

with col4:
    st.header("🌥️ 검색 지역 날씨 정보 🌥️", divider="red")
    tour_name,tour_dis = st.columns(2)
    tour_name.metric("근처 관측 지점명", f"{nearest_aws['Name']}",border=True,)
    tour_dis.metric("떨어진 거리",f"{round(nearest_aws['Distance'],3)} km", border=True,)
    tour1, tour2 = st.columns(2)
    tour1.metric("관광 점수", f"{nearest_aws['tourism_index']}",border=True)
    tour2.metric("관광 등수", f"{nearest_aws['rank']}",border=True)
    col5, col7 = st.columns(2)
    col5.metric("기온", f"{total_api[total_api['STN_ID'].isin([nearest_aws['STN_ID']])]['TA'].iloc[0]}°C",border=True)
    col7.metric("10분 평균 풍속", f"{total_api[total_api['STN_ID'].isin([nearest_aws['STN_ID']])]['WS10'].iloc[0]}m/s",border=True)
    col9, col10 = st.columns(2)
    col9.metric("15분 강수량", f"{total_api[total_api['STN_ID'].isin([nearest_aws['STN_ID']])]['RN-15m'].iloc[0]}mm",border=True)
    col10.metric("습도", f"{total_api[total_api['STN_ID'].isin([nearest_aws['STN_ID']])]['HM'].iloc[0]}%",border=True)

slider1, reco1 = st.columns(2)
st.header("관광지 추천 ", divider="red")
with slider1:
    st.header("관광지 추천 범위 선택", divider="red")
    range_sel = st.select_slider(
        "관광지 추천 범위 선택",
        options=[
            2,
            5,
            10,
            20,
            50,
        ],
    )
    st.subheader(f"선택하신 관광지 추천 범위는 근처 {range_sel} km 입니다")
with reco1:
    st.header("관광지 추천 🏝️", divider="red")
    tourism_within_dis = find_nearest_tour(lat, lon, range_sel, end)
    print(tourism_within_dis)
    tourism_within_dis.set_index("rank", inplace=True)

    columns_to_exclude = ['Latitude', 'Longitude']
    filtered_data = tourism_within_dis.drop(columns=columns_to_exclude, errors='ignore')

    # config 설정
    config = {
        "_index": st.column_config.NumberColumn("추천 관광지 등수"),
        "name": "관광지 이름",
        "Distance": st.column_config.NumberColumn("추천 관광지 거리 (km)"),
        "nearest_tourism_index": st.column_config.NumberColumn("추천 관광지 추천 점수"),
    }

    # 수정된 데이터프레임 출력
    st.dataframe(filtered_data, column_config=config,use_container_width=True)

col11, col12 = st.columns(2)
with col11:
    st.header("기상 특보 🚨", divider="red")
    alret()
    st.image("alret.png")
with col12:
    st.header("초단기 예보 & 적외 위성 영상 🖼️", divider="red")
    tab1, tab2= st.tabs(["초단기 예보 (30분)", "적외위성영상"])
    with tab1:
        with st.spinner('초단기 예보 가져오는중....☂️ [초단기 예보가 바뀌거나 검색해서 위치가 변경되면 다운로드를 새롭게 받아 오래 걸릴 수 있어요!]'):
            rain(lat,lon)
        gif_path = "rain.gif"
        st.image(gif_path, caption="초단기 예측 (30분)")
    with tab2:
        with st.spinner('새로운 적외 위성 영상을 가져오는 중....☁️'):
            infrared()
        st.image("infrared.jpg",caption="적외위성영상")
