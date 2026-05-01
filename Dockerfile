# 1. 가볍고 최신 버전인 파이썬 3.11 이미지 사용
FROM python:3.11-slim

# 2. 컨테이너 내부의 작업 폴더 지정
WORKDIR /app

# 3. 패키지 목록을 복사하고 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 내 코드와 static 폴더를 통째로 복사
COPY . .

# 5. 컨테이너가 켜질 때 실행할 명령어 (uvicorn 실행)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]