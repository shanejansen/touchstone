FROM python:3-slim
WORKDIR /app
COPY app .
EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=3s CMD exit 0
CMD python ./main.py
