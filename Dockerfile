FROM python:3.10-slim

WORKDIR /app

# Install ffmpeg (required for Discord voice)
RUN apt-get update && apt-get install -y ffmpeg libopus0 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
