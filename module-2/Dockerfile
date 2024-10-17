FROM python:3.9-slim-buster
RUN useradd -m appuser
USER appuser
EXPOSE 8080
CMD ["python3", "-m", "http.server", "8080"]
