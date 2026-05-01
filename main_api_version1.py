# main.py
from fastapi import FastAPI, HTTPException
from satellite_service import fetch_tle, calculate_position

# 1. FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Nara Space Observer-1A Tracker API",
    description="나라스페이스 옵저버-1A 위성의 실시간 위치를 제공하는 API 서버입니다.",
    version="1.0.0"
)

# 나라스페이스 옵저버-1A의 NORAD ID
OBSERVER_1A_ID = 58323

@app.get("/")
def read_root():
    return {"message": "Welcome to Satellite Tracker API! Go to /docs for Swagger UI."}

# 2. 위성 위치 조회 엔드포인트 (REST API)
@app.get("/api/satellite/observer-1a")
def get_satellite_location():
    """
    CelesTrak에서 최신 TLE를 가져와 현재 위성의 위도, 경도, 고도를 계산하여 반환합니다.
    """
    # 1) 실시간 TLE 데이터 수집
    tle_result = fetch_tle(OBSERVER_1A_ID)
    
    if not tle_result:
        raise HTTPException(status_code=500, detail="위성 데이터를 가져오는 데 실패했습니다.")
    
    name, l1, l2 = tle_result
    
    # 2) 위치 계산 로직 실행
    pos_data = calculate_position(name, l1, l2)
    
    # 3) JSON 형태로 자동 응답 (Dict를 리턴하면 FastAPI가 JSON으로 변환해줍니다)
    return pos_data

# 실행 시 진입점
if __name__ == "__main__":
    import uvicorn
    # 서버 실행: 8000번 포트에서 실행하며, 코드가 수정되면 자동으로 재시작(--reload) 합니다.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)