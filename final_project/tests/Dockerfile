FROM python:3.9


COPY ../../requirements.txt /requirements.txt
RUN yes | pip3.9 install -r requirements.txt
RUN pip3.9 install pytest-xdist==2.5.0 allure_python_commons==2.9.45 allure-pytest