FROM python:3.9.7
WORKDIR /app
RUN echo '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' | docker login ghcr.io --user USERNAME --password-stdin
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["run.py"]
ENTRYPOINT ["python3"]
