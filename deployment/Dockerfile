FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY src/ ./src/

# Set working directory to src (optional if your main.py is inside src/)
WORKDIR /app/src

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

