FROM python:3.14-rc-slim

WORKDIR /app

# Install uv for faster package installation
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies using uv
RUN uv pip install --system .

# Expose the default port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "orlwx.main:app", "--host", "0.0.0.0", "--port", "8000"]
