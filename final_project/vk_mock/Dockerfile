FROM python:latest
WORKDIR /vk_api
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV VK_URL=0.0.0.0:8543
CMD [ "python3", "./app.py"]
