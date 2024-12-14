import requests
from datetime import datetime, timedelta
from pytz import timezone
from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime, timedelta
import os
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime
import math
from pytz import timezone

def infrared():
    # 현재 시간에서 10분 전 시간 계산
    current_time = datetime.now()
    ten_minutes_ago = current_time - timedelta(minutes=10)

    # 10분 전의 시간을 원하는 형식으로 변환 (YYYYMMDDHHMM)
    tm2 = ten_minutes_ago.strftime('%Y%m%d%H%M')

    # 예보 시간을 맞추기 위해 round(float(tm2) * 0.1) * 10 사용

    tm2_adjusted = str(int(math.floor(float(tm2) * 0.1) * 10))

    print(f"예보 시간에 맞춘 조정된 시간: {tm2_adjusted}")

    # 결과 출력
    print(f"현재 시각: {current_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"10분 간격에 맞춘 조정된 시각: {tm2_adjusted}")

    def download_file(file_url, save_path):
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # 요청 중 에러가 발생하면 예외를 발생시킴
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):  # 데이터 조각(chunk)별로 쓰기
                    f.write(chunk)
            print(f"파일이 성공적으로 저장되었습니다: {save_path}")
        except Exception as e:
            print(f"파일 다운로드 중 오류 발생: {e}")

    # auth_key 설정
    auth_key = "829vQlOcRAuvb0JTnFQLrQ"

    # URL 및 파일 경로 생성
    url = f"https://apihub.kma.go.kr/api/typ05/api/GK2A/LE1B/IR105/KO/image?date={tm2_adjusted}&authKey={auth_key}"
    save_file_path = 'infrared.jpg'

    # URL 출력
    print(f"현재에 근접한 구름영상 URL: {url}")

    # 파일 다운로드 호출
    download_file(url, save_file_path)
    print("제주도 추출중...")
    try:
        # 예보 시간을 "HH : MM" 형식으로 변환
        kst = timezone('Asia/Seoul')
        tm2_adjusted = datetime.strptime(tm2_adjusted, "%Y%m%d%H%M")
        tm2_adjusted_kst = tm2_adjusted.astimezone(kst)
        tm2_adjusted_str = tm2_adjusted_kst.strftime('%H : %M')  # "19 : 50" 형식으로 변환

        with Image.open(save_file_path) as img:
            # 제주도 영역의 좌표 설정
            crop_box = (350, 575, 600, 825)  # 최종 조정된 좌표

            # 이미지 자르기
            cropped_img = img.crop(crop_box)

            # 잘라낸 이미지 출력 (공백 제거)
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(cropped_img)
            ax.axis('off')  # 축 제거

            # 텍스트 추가 (좌측 위에 시간 표시)
            ax.text(
                5, 5,  # 텍스트 위치 (픽셀 단위 좌표)
                tm2_adjusted_str,  # 표시할 텍스트
                color='white',  # 텍스트 색상
                fontsize=20,  # 폰트 크기
                fontweight='bold',  # 굵은 글씨
                ha='left', va='top',  # 텍스트 정렬
                bbox=dict(facecolor='black', edgecolor='white', alpha=0.6, boxstyle="round,pad=0.3")  # 배경 스타일
            )

            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.savefig(save_file_path)
            plt.close()
    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {e}")
