# main.py
import time
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from satellite_service import fetch_tle, calculate_position

app = FastAPI(title="Observer-1A Tracker API")

OBSERVER_1A_ID = 58323

# 핵심 아키텍처: 데이터 캐싱 (IP 차단 방지) => 이거 안하면 1초마다 계속CelesTrak API 호출해서 DDos로 오해받을 수도
# TLE 데이터는 자주 안 변하므로 메모리에 들고 있습니다.
tle_cache = {
    "data": None,
    "last_updated": 0
}

@app.get("/api/satellite/observer-1a")
def get_satellite_location():
    current_time = time.time()
    
    # 캐시가 비어있거나, 업데이트 된 지 1시간(3600초)이 지났을 때만 API를 호출합니다.
    if tle_cache["data"] is None or (current_time - tle_cache["last_updated"] > 3600):
        print("CelesTrak API에서 최신 TLE를 다운로드합니다...")
        result = fetch_tle(OBSERVER_1A_ID)
        if result:
            tle_cache["data"] = result
            tle_cache["last_updated"] = current_time
        else:
            raise HTTPException(status_code=500, detail="TLE 갱신 실패")
    
    name, l1, l2 = tle_cache["data"]
    
    # 위치 계산(SGP4)은 캐싱된 데이터를 이용해 호출될 때마다(1초마다) 수행합니다.
    pos_data = calculate_position(name, l1, l2)
    return pos_data

# 🔥 프론트엔드 연결: static 폴더 마운트
# 주의: 이 라우팅은 항상 가장 아래에 있어야 API 경로와 충돌하지 않습니다.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    # 기본 경로('/') 접속 시 index.html을 반환합니다.
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)