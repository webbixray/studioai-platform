FROM python:3.10-slim
WORKDIR /app
COPY packages/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY packages/backend/ .
CMD ["python", "app.py"]
