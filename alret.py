import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from IPython.display import clear_output  # Jupyter Notebook 환경에서 출력 초기화
import streamlit as st

def alret():
    # 기본 URL 템플릿
    api_key = st.secrets["api"]["a_key"]
    print(api_key)
    base_url = "https://apihub.kma.go.kr/api/typ03/cgi/wrn/nph-wrn7?out=0&tmef=1&city=1&name=0&lon=126.5&lat=33.5&range=100&tm={date}&size=685&wrn=W,R,C,D,O,V,T,S,Y,H,&authKey={api_key}"
    # 현재 시간을 한국 표준시(KST)로 변환
    utc_time = datetime.utcnow()  # UTC 시간 가져오기
    current_time = utc_time + timedelta(hours=9)  # UTC + 9시간 = 한국 표준시
    formatted_date = current_time.strftime("%Y%m%d%H%M")  # API에 맞는 날짜 포맷
    updated_url = base_url.format(date=formatted_date,api_key = api_key)


    print(f"Requesting data for: {formatted_date} (KST)")
    print(updated_url)  # 생성된 URL 출력

    try:
        # API 호출
        response = requests.get(updated_url)
        if response.status_code == 200 and response.content:
            print("Data received:")
            # API가 이미지 데이터를 반환할 경우
            try:
                image = Image.open(BytesIO(response.content))  # 이미지 데이터 로드

                # 이전 출력 화면 초기화
                clear_output(wait=True)

                # 이미지를 Matplotlib으로 표시
                fig, ax = plt.subplots(figsize=(10, 10))  # 새로운 Figure 생성
                ax.imshow(image)
                ax.axis('off')
                plt.tight_layout()
                plt.show()
                plt.savefig("alret.png")
                plt.close(fig)  # Figure를 명시적으로 닫음

            except Exception as img_error:
                print("Error displaying image:", img_error)

        else:
            print(f"No data available for {formatted_date}. HTTP {response.status_code}")

    except Exception as e:
        print(f"Error during API request: {e}")
