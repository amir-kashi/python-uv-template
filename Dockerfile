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

# Default command
CMD ["uv", "run", "streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
# OR (non Streamlit apps):
# CMD ["/workspace/.venv/bin/python", "-m", "app.main"]

# expose the streamlit port for documentation purposes
EXPOSE 8501
