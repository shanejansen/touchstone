FROM jupyter/all-spark-notebook
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./jars ./jars
COPY ./src ./src
CMD spark-submit --jars jars/postgresql-42.7.1.jar ./src/main.py
