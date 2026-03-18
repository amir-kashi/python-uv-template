# Use official Python runtime
FROM python:3.13-slim

# Prevent Python from writing pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /workspace

# Copy dependency files first (for better Docker caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (system-wide inside container)
RUN uv sync --frozen --no-cache --no-dev

# Copy source code
COPY src ./src

# Copy documentation files so the Streamlit app can load them
COPY README.md ./
COPY docs ./docs

# Create logs directory
RUN mkdir -p logs

# Set Python path
ENV PYTHONPATH=/workspace/src

# Default command — overridden per service in docker-compose.yml
CMD ["uv", "run", "streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Streamlit port
EXPOSE 8501
# FastAPI port
EXPOSE 8000
