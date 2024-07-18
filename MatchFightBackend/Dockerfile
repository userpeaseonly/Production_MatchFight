# MatchFightBackend/Dockerfile
FROM python:3.9

WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the Gunicorn server
CMD ["gunicorn", "MatchFight.wsgi:application", "--bind", "0.0.0.0:8000"]
