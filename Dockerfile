FROM python:3.12
WORKDIR /src
COPY . /src
CMD ["python3", "-u", "src/main.py"]