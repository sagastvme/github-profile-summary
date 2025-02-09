FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir debugpy  # <---- Install debugpy

EXPOSE 5000

VOLUME [ "/app" ]

# CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]