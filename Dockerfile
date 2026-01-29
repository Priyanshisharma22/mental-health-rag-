FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports
EXPOSE 8001
EXPOSE 8501

# Default command (overridden by docker-compose)
CMD ["bash"]
