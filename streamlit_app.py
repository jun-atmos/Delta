import api 
import rain
import geofind

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


col1, col2 = st.columns([3, 1])

with col1:
    tourist_spot = st.text_input("관광지 검색","한라산")
    lat,lon,address = get_location_info(tourist_spot)
