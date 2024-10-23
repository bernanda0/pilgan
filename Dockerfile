FROM python:3.11

WORKDIR /app
COPY . /app

COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

EXPOSE 6969

CMD ["python", "quiz_server.py"]
