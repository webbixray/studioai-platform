FROM python:3.10-slim
WORKDIR /app
COPY packages/llm-gateway/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY packages/llm-gateway/ .
CMD ["python", "gateway.py"]
