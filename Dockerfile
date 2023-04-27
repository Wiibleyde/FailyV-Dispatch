FROM python:3.10

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.3.1/tailwindcss-linux-x64 && chmod +x tailwindcss-linux-x64 && mv tailwindcss-linux-x64 tailwindcss
RUN ./tailwindcss -i static/style.css -o static/output.css

CMD ["python", "main.py"]

# Path: /app
COPY . .
