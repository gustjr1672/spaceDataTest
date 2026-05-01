# satellite_service.py
import requests
from skyfield.api import EarthSatellite, load, wgs84
from datetime import datetime, timezone
    #API로 받아온 response 아래처럼 생겼음.
    #BSERVER-1A             
1   #58323U 23174BV  26114.94179074  .00010890  00000+0  29902-3 0  9995
2   #58323  97.3937 198.3167 0007377 358.4465   1.6755 15.37393351137022
def fetch_tle(norad_id):
    """CelesTrak API를 통해 최신 TLE 데이터를 가져옵니다."""
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=tle"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        
        if len(lines) >= 3:
            return lines[0].strip(), lines[1].strip(), lines[2].strip()
        else:
            print("❌ TLE 데이터 형식이 올바르지 않습니다.")
            return None
    except Exception as e:
        print(f"❌ API 호출 중 오류 발생: {e}")
        return None

def calculate_position(name, line1, line2):
    """TLE 데이터를 기반으로 현재의 위도, 경도, 고도를 계산합니다."""
    ts = load.timescale()
    satellite = EarthSatellite(line1, line2, name, ts)
    
    now = datetime.now(timezone.utc)
    t = ts.from_datetime(now)
    
    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)
    
    return {
        "name": name,
        "time": now.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "lat": round(subpoint.latitude.degrees, 4),
        "lon": round(subpoint.longitude.degrees, 4),
        "alt": round(subpoint.elevation.km, 2)
    }