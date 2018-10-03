FROM python:3

WORKDIR /loader

COPY . .
RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "-u", "main.py", "config/docker_config.yaml"]


