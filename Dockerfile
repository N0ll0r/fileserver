FROM python:slim
WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
VOLUME /opt/uploads
EXPOSE 80
ENTRYPOINT ["python3", "app.py"]
