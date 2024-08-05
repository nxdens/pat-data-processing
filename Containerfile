FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pat_data_processing"]
