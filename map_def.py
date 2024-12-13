import numpy as np
import pandas as pd

def wet_bulb_temperature(temp, RH):   #습구온도
    return temp * np.arctan(0.151977 * (RH + 8.313659)**0.5) + np.arctan(temp + RH) - np.arctan(RH - 1.676331) + 0.00391838 * RH**(3/2) * np.arctan(0.023101 * RH) - 4.686035

def discomfort_index(temp, RH):   #여름철 불쾌지수
    return (0.81 * temp) + (0.01 * RH * (0.99 * temp - 14.3)) + 46.3


def apparent_temperature(temp, RH, wind_speed, season):   #체감온도 계산 함수

    if season == "winter" and wind_speed > 1.3 and temp <= 10:
        return 13.12 + (0.6215 * temp) - (11.37 * wind_speed**0.16) + (0.3965 * temp * wind_speed**0.16)

    #봄/가을 온도 조건 - 20이상(여름), 20미만(겨울)
    elif season == "spring_fall":
        if temp >= 20:
            tw = wet_bulb_temperature(temp, RH)
            return -0.2442 + (0.55399 * tw) + (0.45535 * temp) - (0.0022 * tw**2) + (0.00278 * tw * temp) + 3.0
        else:
            return 13.12 + (0.6215 * temp) - (11.37 * wind_speed**0.16) + (0.3965 * temp * wind_speed**0.16)

    elif season == "summer":
        tw = wet_bulb_temperature(temp, RH)
        return -0.2442 + (0.55399 * tw) + (0.45535 * temp) - (0.0022 * tw**2) + (0.00278 * tw * temp) + 3.0
    else:
        return temp    #조건에 맞지 않으면 경우 관측값

def calculation_scores(total_api_values):
    tourism_scores = []   #결과 저장

    #각 행을 반복하며 계산
    for _, row in total_api_values.iterrows():
      #행을 하나씩 반복(iterate) = index와 data를 하나씩 가져옴. => row는 한 행이자 pd.Series임.
        visibility_score = (row["VIS1"] / 1000) if pd.notnull(row["VIS1"]) else 0
        #시정 단위 m -> km : Nan이면 0으로 채우기

        if row["season"] == "summer":
            discomfort = discomfort_index(row["TA"], row["HM"])
            score = visibility_score + (68 - discomfort) - row["RN-15m"] - row["WS10"]

        elif row["season"] == "winter":
            apparent_temp = apparent_temperature(row["TA"], row["HM"], row["WS10"], "winter")
            if apparent_temp == row["TA"]:  # 관측된 온도만 사용
                score = visibility_score + apparent_temp - row["RN-15m"] - row["WS10"]
            else:
                score = visibility_score + apparent_temp - row["RN-15m"]

        elif row["season"] == "spring_fall":
            apparent_temp = apparent_temperature(row["TA"], row["HM"], row["WS10"], "spring_fall")
            score = visibility_score + apparent_temp - row["RN-15m"]
        else:
            score = np.nan

        tourism_scores.append({"TIME": row["TIME"], "STN_ID": row["STN_ID"], "tourism_index": score})

    tourism_df = pd.DataFrame(tourism_scores)

    return tourism_df

def determine_season(month):
    if month in [5, 6, 7, 8, 9]:
        return "summer"
    elif month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4]:
        return "spring_fall"
    elif month in [10, 11]:
        return "spring_fall"
    else:
        return None

# IDW 보간 함수 정의
def inverse_distance_weighting(lat, lon, known_points, power=2):                                     #p = 거리 가중치 지수
    distances = np.sqrt((known_points["Latitude"] - lat)**2 + (known_points["Longitude"] - lon)**2)  #NaN인 한 지점을 중심으로 직선 거리 계산
    distances = np.where(distances == 0, 1e-10, distances)                                           #거리차가 만약 0이라면, 1e-10로 대체
    weights = 1 / (distances**power)                                                                 #거리 기반 가중치 -> p를 2로 두어서, 거리가 멀수록 가중치가 급격히 감소하게함.
    weighted_sum = np.sum(weights * known_points["VIS1"])                                            #각 관측값에 가중치를 곱해서 합산
    return weighted_sum / np.sum(weights)                                                            #가중치의 합으로 나눔
