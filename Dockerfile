FROM python:3.11.6-alpine
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY migrations migrations
COPY src src
ENV PYTHONPATH=/code/src
EXPOSE 8000
CMD ["gunicorn", "-w 4", "fairs_api:create_app()", "-b 0.0.0.0:8000"]
