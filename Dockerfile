FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.5.1+cpu
RUN pip install --no-cache-dir .
COPY data ./data
EXPOSE 8000
CMD ["uvicorn", "financial_assistant.api:app", "--host", "0.0.0.0", "--port", "8000"]
