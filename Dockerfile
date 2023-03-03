FROM python:3.9.7-buster
WORKDIR /app
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["run.py"]
ENTRYPOINT ["python3"]
