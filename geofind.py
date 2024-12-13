from geopy.geocoders import Nominatim

def get_location_info(place_name):
    geolocator = Nominatim(user_agent="location_finder")
    try:
        # 장소 이름을 기반으로 위치 정보 검색
        location = geolocator.geocode(place_name)
    except Exception as e:
        print(f"오류 발생: {e}")
    return location.latitude, location.longitude, location.address