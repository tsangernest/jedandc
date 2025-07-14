FROM python:3.13.2-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt /app/


WORKDIR /var
RUN python -m venv venv/


WORKDIR /app


RUN pip install --upgrade pip
RUN pip install -U setuptools wheel psycopg2-binary
RUN pip install -r requirements.txt --no-cache-dir


COPY . .


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

