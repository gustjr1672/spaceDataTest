# main.py
import time

# 분리해둔 satellite_service 파일에서 두 함수를 불러옵니다.
from satellite_service import fetch_tle, calculate_position

def main():
    OBSERVER_1A_ID = 58323
    
    print("위성 데이터를 수집 중입니다...\n")
    
    # 1. API 호출
    tle_result = fetch_tle(OBSERVER_1A_ID)
    print(f"tle row데이터: {tle_result}")
    
    if tle_result:
        name, l1, l2 = tle_result
        
        # 2. 위치 계산
        pos = calculate_position(name, l1, l2)
        
        # 3. 결과 출력
        print(f"🛰️ {pos['name']} 실시간 추적 결과")
        print("-" * 30)
        print(f"⏱️ 기준 시간: {pos['time']}")
        print(f"🌐 현재 위치: 위도 {pos['lat']}°, 경도 {pos['lon']}°")
        print(f"🚀 현재 고도: {pos['alt']} km")

# 여기가 바로 C#의 Main() 역할입니다!
if __name__ == "__main__":
    main()