FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
CMD ["python", "-m", "structextract.cli", "extract", "--text", "sample"]