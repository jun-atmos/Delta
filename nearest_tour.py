import pandas as pd
from geopy.distance import geodesic

def find_nearest_tour(lat, lon, dis, end):
    # 관광지 데이터를 불러오기
    print(end)
# 관광지 데이터를 불러오기
    tourist_point = pd.read_csv('jeju_tourist_spots.csv')
    tourist_point.rename(columns={'latitude': 'Latitude', 'longitude': 'Longitude'}, inplace=True)

    # 검색 지점의 위치
    search_location = (lat, lon)

    # 관광지와의 거리 계산 함수
    def calculate_distance(row):
        tourist_location = (row['Latitude'], row['Longitude'])
        return geodesic(search_location, tourist_location).kilometers

    # 관광지 데이터프레임에 거리 열 추가
    tourist_point['Distance'] = tourist_point.apply(calculate_distance, axis=1)

    # 검색 범위(dis) 내의 관광지 필터링
    tourism_within_dis = tourist_point[tourist_point['Distance'] <= dis].sort_values(by=['Distance'])

    # 근처 관측 지점의 tourism_index 매핑
    def find_closest_station(row):
        tourist_location = (row['Latitude'], row['Longitude'])
        end['Station_Distance'] = end.apply(
            lambda x: geodesic(tourist_location, (x['Latitude'], x['Longitude'])).kilometers,
            axis=1
        )
        # 가장 가까운 관측 지점의 tourism_index 반환
        closest_station = end.loc[end['Station_Distance'].idxmin()]
        return closest_station['tourism_index']

    # 가장 가까운 관측 지점의 tourism_index 추가
    tourism_within_dis['nearest_tourism_index'] = tourism_within_dis.apply(find_closest_station, axis=1)
    tourism_within_dis = tourism_within_dis.dropna(subset=['nearest_tourism_index'])
    # tourism_index에 따라 순위 매기기
    tourism_within_dis['rank'] = tourism_within_dis['nearest_tourism_index'].rank(method='min', ascending=False).astype(int)
    tourism_within_dis = tourism_within_dis.sort_values(by='rank')

    # 결과 반환
    return tourism_within_dis