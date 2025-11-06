# Official lightweight Python image
FROM python:3.13-slim


WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy just requirements.txt and install deps specified in that
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy app code
COPY . .

# Tell Docker the container will listen on port 8080
EXPOSE 8080

# run the app
CMD ["python", "hello.py"]
