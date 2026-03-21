FROM python:3.10-slim

WORKDIR /app

# Install ffmpeg and libopus for Discord voice support
RUN apt-get update && apt-get install -y ffmpeg libopus0 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Only copy needed files (no keep_alive.py anymore)
COPY bot.py .
COPY .env .

CMD ["python", "bot.py"]
