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
    print(lat,lon,address)

nearest_aws = find_nearest(lat,lon,end)
print(nearest_aws)

with col2:
     st.text("✏️자세한 홈페이지 이용방법은 맨 아래 홈페이지 설명서를 참고 부탁드립니다.")
     st.text("✏️강릉원주대학교 대기환경과학과 DELTA_TEAM 프로젝트입니다. 코드는 github에서 확인 가능합니다.")

col3, col4 = st.columns([3, 2])

with col3:
    config = map_config(lat,lon)
    map_1 = KeplerGl()
    map_1.config = config
    map_1.add_data(data=end, name='AWS&ASOS')
    location_data = pd.DataFrame({
    'latitude': [lat],
    'longitude': [lon],
    'address': [address],
    'icon kepler.gl': ['place']  # Kepler.gl 아이콘 레이어 활성화
    })
    map_1.add_data(data=location_data, name='LOC')

    html_path = 'kepler_map.html'
    map_1.save_to_html(file_name=html_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        kepler_html = f.read()
    st.components.v1.html(kepler_html, height=600)
    st.text("📢 원의 크기가 크고 초록색일수록 관광하기 좋은곳 입니다, 검색 위치는 민트색 📍아이콘으로 표시됩니다.")

with col4:
    st.header(" 검색 지역 날씨 정보 🌥️", divider="red")
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

with st.expander("홈페이지 설명서"):
    tab1, tab2, tab3 = st.tabs(["지도 사용 방법", "적외 위성 분석법", "관광지수 알고리즘 설명"])

    with tab1:
        st.header("홈페이지 사용 방법")
        st.text("내가 가려는 관광지가 날씨가 안좋아서 여행을 망치면 어떡하지? 라는 생각 해보셨나요?")
        st.text("내가 가려는 관광지에 대한 날씨 정보 및 제주도에서 여행하기 좋은지 안 좋은지 알려드립니다.")
        st.text("내가 가려는 관광지가 여행하기 좋지 않다면 근처 관광지 추천도 받아보세요!")

        st.subheader("홈페이지 이용 주의 사항")
        st.text("관광지의 실시간 날씨 정보를 이용하는 것이 아닌 근처 날씨 관측 지점의 정보를 이용합니다. 관광지와 관측지점이 많이 떨어져 있으면 홈페이지 결과와 다를 수 있습니다.")
        st.text("10분마다 초단기 예보가 업데이트됩니다. 초단기 예보를 가져올 때 오래 걸릴 수 있습니다.")

        st.subheader("지도 사용 방법")
        st.text("원의 크기가 크고 초록색일수록 관광하기 좋은 곳 입니다.")
        st.text("지도 위에 있는 검색창에 가려 하는 관광지를 입력합니다.")
        st.text("민트색 📍아이콘으로 검색한 관광지의 위치가 표시가 됩니다.")
        st.image("map.png", width=700)
        st.subheader("관광지 추천 사용 방법")
        st.text("관광지 추천 범위를 선택해 주세요.")
        st.text("아래 있는 슬라이드 바로 선택 가능합니다.")
        st.text("선택하면 검색한 관광지에서 선택 범위 안에 있는 관광지를 추천드립니다.")
        st.image("reco.png", width=700)
    with tab2:
        st.header("적외 위성 분석법")
        st.image("inf_sol.png", width=700,caption="출처 : 국가위성센터")
        st.subheader("적외 위성 사진에서")
        st.text("고도가 높은 구름 : 밝게 보인다.")
        st.text("고도가 낮은 구름 : 어둡게 보인다.")
    with tab3:
        st.header("관광지수 알고리즘 설명")
        st.subheader("관광지수 산출")
        st.image("tour_cal_1.png", width=700)
        st.subheader("시정점수 포함을 위한 알고리즘")
        st.image("tour_cal_2.png", width=700)
