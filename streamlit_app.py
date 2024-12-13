from api import *
from rain import *
from geofind import *
from preprocessing import *
from map_pro import *
from map_config import *

import streamlit as st
from streamlit_keplergl import keplergl_static
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
end = map_data_pro(tm2,jeju_aws)

col1, col2 = st.columns([3, 2])

with col1:
    tourist_spot = st.text_input("관광지 검색","한라산")
    lat,lon,address = get_location_info(tourist_spot)


col3, col4 = st.columns([3, 2])

with col3:
    config = map_config()
    map_1 = KeplerGl()
    #map_1.config = config
    map_1.add_data(data=end, name='AWS&ASOS')

    html_path = 'kepler_map.html'
    map_1.save_to_html(file_name=html_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        kepler_html = f.read()
    st.components.v1.html(kepler_html, height=600)


with col4:
    tour_name, = st.columns(1)
    tour_name.metric(f"지점명", "서귀포",border=True)
    tour1, tour2 = st.columns(2)
    tour1.metric(f"관광 점수", "23.758",border=True)
    tour2.metric(f"관광 등수", "3등",border=True)
    col5, col6, col7 = st.columns(3)
    col5.metric(f"기온", "14 °C",border=True)
    col6.metric(f"풍속", "9 m/s",border=True)
    col7.metric(f"15분 평균 풍속", "4 m/s",border=True)
    col8, col9, col10 = st.columns(3)
    col8.metric(f"1분 강수량", "70 mm",border=True)
    col9.metric(f"15분 강수량", "9 mm",border=True)
    col10.metric(f"습도", "86%",border=True)

col11, col12 = st.columns([2, 3])
with col11:
    st.header("기상 특보 🚨", divider="red")
    st.image("https://static.streamlit.io/examples/dice.jpg")
with col12:
    tab1, tab2, tab3 = st.tabs(["초단기 예측 (30분)", "적외위성영상", "영상 사용 설명서"])
    with tab1:
        rain()
        st.header("초단기 예측 (30분)")
        html_path = "rain.html"
        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        st.components.v1.html(html_content)
    with tab2:
        st.header("적외위성영상")
        st.image("https://static.streamlit.io/examples/dog.jpg")
    with tab3:
        st.header("영상 사용 설명서")
        st.image("https://static.streamlit.io/examples/owl.jpg")