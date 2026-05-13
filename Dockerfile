FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

# 2. Install uv and project dependencies
RUN pip install --no-cache-dir uv \
    && uv pip install --system --no-cache -r pyproject.toml \
    && pip install --no-cache-dir gunicorn



COPY . .

RUN mkdir -p /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn QuickPay.wsgi:application --bind 0.0.0.0:8000"]