FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "mdac.wsgi:application"]