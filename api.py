import requests

def download_file(tm2):
    # URL 및 파일 경로 설정
    wea_url = f"https://apihub-pub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min?tm2={tm2}&stn=0&disp=1&help=1&authKey=zbvBntvMSSK7wZ7bzDkiLg"
    cloud_url = f"https://apihub-pub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min_cloud?tm2={tm2}&stn=0&disp=1&help=1&authKey=zbvBntvMSSK7wZ7bzDkiLg"
    vi_url = f"https://apihub-pub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min_vis?tm2={tm2}&stn=0&disp=1&help=1&authKey=zbvBntvMSSK7wZ7bzDkiLg"

    wea_save_file_path = f'./weather_csv/wea_{tm2}.csv'
    cloud_save_file_path = f'./weather_csv/cloud_{tm2}.csv'
    vi_save_file_path = f'./weather_csv/vi_{tm2}.csv'

    # 저장 경로와 파일 URL을 리스트로 설정
    save_paths = [wea_save_file_path, cloud_save_file_path, vi_save_file_path]
    file_urls = [wea_url, cloud_url, vi_url]

    # 파일 다운로드 반복문
    for save_path, file_url in zip(save_paths, file_urls):
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"File saved to {save_path}")
        else:
            print(f"Failed to download from {file_url}. Status code: {response.status_code}")