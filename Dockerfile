FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the files
COPY . .

# Run the bot
CMD ["python", "bot.py"]