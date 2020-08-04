FROM jupyter/all-spark-notebook
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./jars ./jars
COPY ./src ./src
CMD spark-submit --jars jars/mysql-connector-java-8.0.21.jar ./src/main.py
