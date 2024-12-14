import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.colorbar import ColorbarBase
import matplotlib.image as mpimg
import matplotlib.animation as animation
import os
from datetime import datetime, timedelta
import time
from pytz import timezone
import math
import requests
from IPython.display import clear_output
import glob

def download_file_rain(file_url, save_path):
    with open(save_path, 'wb') as f:  # 저장할 파일을 바이너리 쓰기 모드로 열기
        response = requests.get(file_url)  # 파일 URL에 GET 요청 보내기
        f.write(response.content)  # 응답의 내용을 파일에 쓰기

def rain(lat,lon):

    # 현재 시간에서 10분 전 시간 계산
    current_time = datetime.now(timezone('Asia/Seoul'))
    ten_minutes_ago = current_time - timedelta(minutes=10)
    # 10분 전의 시간을 원하는 형식으로 변환 (YYYYMMDDHHMM)
    tm2 = ten_minutes_ago.strftime('%Y%m%d%H%M')

    # 예보 시간을 맞추기 위해 round(float(tm2) * 0.1) * 10 사용
    tm2_adjusted_str = str(int(math.floor(float(tm2) * 0.1) * 10))

    last_time_file = "last_check.txt"
    if os.path.exists(last_time_file):
        with open(last_time_file, "r") as f:
            last_state = f.read().strip().split(',')
            last_tm2 = last_state[0]
            last_lat = float(last_state[1])
            last_lon = float(last_state[2])
    else:
        last_tm2, last_lat, last_lon = None, None, None

    # tm2, lat, lon 값 변경 확인
    if tm2_adjusted_str != last_tm2 or lat != last_lat or lon != last_lon:
        print(f"Change detected: tm2={tm2_adjusted_str}, lat={lat}, lon={lon} (previous: {last_tm2}, {last_lat}, {last_lon})")

        # 상태 저장
        with open(last_time_file, "w") as f:
            f.write(f"{tm2_adjusted_str},{lat},{lon}")

        # 이전 이미지 삭제
        img_dir = 'rain_img/'
        print("Removing old files...")
        [os.remove(file) for file in glob.glob(os.path.join(img_dir, '*'))]

        # 새로운 이미지 다운로드
        print("Starting download...")

        # tm2_adjusted 문자열을 datetime 객체로 변환
        tm2_adjusted_datetime = datetime.strptime(tm2_adjusted_str, '%Y%m%d%H%M')

        # 반복문을 통해 10분 ~ 90분 동안 10분 간격으로 이미지를 다운로드하고 로드
        for minutes_ahead in range(10, 50, 10):
        # 새로운 시간 생성
            tm2_f_datetime = tm2_adjusted_datetime + timedelta(minutes=minutes_ahead)

            # 다시 문자열로 변환하여 파일명에 사용
            tm2_f = tm2_f_datetime.strftime('%Y%m%d%H%M')

            # URL 설정
            url = f"https://apihub.kma.go.kr/api/typ03/cgi/dfs/nph-qpf_ana_img?eva=1&tm={tm2_adjusted_str}&qpf=B&ef={minutes_ahead}&map=HB&grid=0.1&legend=1&size=6000&zoom_level=1000&zoom_x=3000&zoom_y=1000&x1=1000&y1=1000&authKey=829vQlOcRAuvb0JTnFQLrQ"
            save_file_path = f'rain_img/output_file_{tm2_f}.jpg'

            # 파일 다운로드 함수 호출
            print(f"Downloading data for {minutes_ahead} minutes ahead (Time: {tm2_f})")
            download_file_rain(url, save_file_path)
            time.sleep(1)

            # 파일이 존재할 때까지 대기 (파일 다운로드 완료 후 접근)
            while not os.path.exists(save_file_path):
                print(f"Waiting for file to be saved: {save_file_path}")
                time.sleep(1)

            # 파일이 존재하면 이미지를 로드하고 출력
            if os.path.exists(save_file_path):
                try:
                    img = mpimg.imread(save_file_path)

                    # 이미지 크롭
                    cropped_img = img[3000:5000, 2300:4300, :]

                    # 이미지 출력 설정
                    fig, ax = plt.subplots(figsize=(8, 8), dpi=500)
                    ax.imshow(cropped_img)

                    # 축 설정
                    ax.spines['top'].set_color('black')
                    ax.spines['top'].set_linewidth(1)
                    ax.spines['right'].set_color('black')
                    ax.spines['right'].set_linewidth(1)
                    ax.spines['bottom'].set_color('black')
                    ax.spines['bottom'].set_linewidth(1)
                    ax.spines['left'].set_color('black')
                    ax.spines['left'].set_linewidth(1)
                    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

                    #시간을 원하는 형식으로 다시 변환 (YYYYMMDDHHMM)
                    tm2_f_plus_str = tm2_f_datetime.strftime('%H : %M')

                    # 텍스트 추가 (예보 시간)
                    ax.text(10, 20, f"-{tm2_f_plus_str}-", color='black', fontsize=12, fontweight='bold',
                    ha='left', va='top', bbox=dict(facecolor='white', edgecolor='none', alpha=0.1))


                    # 색상 설정
                    colors = [
                        (51/255, 51/255, 51/255), (0/255, 3/255, 144/255), (76/255, 78/255, 177/255),
                        (179/255, 180/255, 222/255), (147/255, 0/255, 228/255), (179/255, 41/255, 255/255),
                        (201/255, 105/255, 255/255), (244/255, 169/255, 255/255), (180/255, 0/255, 0/255),
                        (210/255, 0/255, 0/255), (255/255, 50/255, 0/255), (255/255, 102/255, 0/255),
                        (204/255, 170/255, 0/255), (224/255, 185/255, 0/255), (249/255, 205/255, 0/255),
                        (255/255, 220/255, 31/255), (255/255, 225/255, 0/255), (0/255, 90/255, 0/255),
                        (0/255, 140/255, 0/255), (0/255, 190/255, 0/255), (0/255, 255/255, 0/255),
                        (0/255, 51/255, 245/255), (0/255, 155/255, 245/255), (0/255, 200/255, 255/255)]

                    num_colors = len(colors)
                    colors.reverse()
                    cmap = clr.ListedColormap(colors)

                    # 컬러바 설정
                    cbar_ax = fig.add_axes([0.91, 0.11, 0.02, 0.77])
                    cb = ColorbarBase(cbar_ax, orientation='vertical', cmap=cmap, norm=plt.Normalize(-0.5, num_colors - 0.5), label=r'$\mathrm{mm \; hr^{-1}}$')
                    cb.ax.tick_params(labelsize=10)  # labelsize를 여기서 설정
                    bounds = [0, 0.1, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 110]
                    cb.set_ticks(range(num_colors))
                    cb.ax.set_yticklabels(bounds)

                    # 특정 위치에 점 추가
                    lat = lat
                    lon = lon
                    x1, y1 = 1440, 840  # lat1 = 33.517, lon1 = 126.950
                    x2, y2 = 1148, 797  # lat2 = 33.555, lon2 = 126.6445
                    lat1, lon1 = 33.5181, 126.9490
                    lat2, lon2 = 33.5553, 126.6446

                    # 위경도 -> x, y 변환 함수
                    def latlon_to_xy(lat, lon):
                        x = x1 + (x2 - x1) * (lon - lon1) / (lon2 - lon1)
                        y = y1 + (y2 - y1) * (lat - lat1) / (lat2 - lat1)
                        return x, y

                    x, y = latlon_to_xy(lat, lon)
                    ax.scatter(x, y, s=20, marker='*', color='darkred')

                    output_path = os.path.join(save_file_path)
                    plt.savefig(output_path, dpi=500, bbox_inches='tight')

                except Exception as e:
                    print(f"Error loading image: {e}")
            else:
                print(f"File not found after waiting: {save_file_path}")
        
        img_dir = 'rain_img/'
        img_paths = sorted(glob.glob(os.path.join(img_dir, '*.jpg')), key=os.path.getmtime, reverse=True)[:4]
        #그림 목록을 list로 가져오기, 단 마지막 수정시간을 반환하고 수정시간을 기준으로 정렬. 가장 최근 파일이 먼저오게 정렬. 9개만.

        fig, ax = plt.subplots(figsize=(10,10))

        #초기 이미지 설정
        img = mpimg.imread(img_paths[0])             #첫 번째 이미지를 읽기
        cropped_img = img[:, :, :]                   #이미지를 자르지 않고 사용
        im = ax.imshow(cropped_img, animated=True)   #애니메이션 만들때, 이미지 변경할 수 있게 허용

        # 애니메이션 업데이트 함수
        def update(frame):
            img = mpimg.imread(img_paths[frame])     #[프레임]에 해당하는 이미지 부르기
            cropped_img = img[:, :, :]               #이미지 자르지 않고 사용
            im.set_array(cropped_img)                #이전에 나온 이미지를 새로운 이미지로 업데이트
            plt.axis('off')                          #xy축을 안보이게 하기
            return [im]


        ani = animation.FuncAnimation(fig, update, frames=range(len(img_paths) - 1, -1, -1), interval=500, blit=True)
        #마지막에서 첫번째 이미지 순서로 에니메이션 나오게 하기, 0.5초 간격, 애니메이션 속도 최적화

        plt.tight_layout() #사진이 딱맞게 하기
        gif_path = 'rain.gif'
        ani.save(gif_path, writer='pillow', fps=2)


        #애니메이션 밑에 나오는 마지막 이미지를 지우기
        clear_output(wait=True)  #출력된 것 초기화
        plt.close()

