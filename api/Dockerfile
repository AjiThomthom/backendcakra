FROM python:3.13-slim

WORKDIR /app

# Menggabungkan instalasi OS & Node.js dalam 1 layer untuk menghemat ukuran image
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg libgl1 libglib2.0-0 ffmpeg gcc \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin sisa kode sumber
COPY . .

RUN prisma generate

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]