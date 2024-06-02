# 빌드 단계
FROM python:3.10-slim as builder

WORKDIR /app

# 시스템 종속성 설치 (빌드용)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 가상환경 생성
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 실행 단계
FROM python:3.10-slim

WORKDIR /app

# 시스템 종속성 (런타임 필수)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 가상환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 애플리케이션 코드 복사
COPY . .

# Gunicorn 실행 (Celery는 docker-compose에서 별도 실행)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "appstore_review.wsgi:application"]