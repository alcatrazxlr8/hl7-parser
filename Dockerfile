FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "hl7_parser.py"]