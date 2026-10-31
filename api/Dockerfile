FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/Doxah/k3s-lab-app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
# Jamais root dans le conteneur 
USER 10001
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "app:app"]