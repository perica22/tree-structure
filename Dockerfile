FROM python:3.4
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN python3 -m virtualenv env
CMD ["export MODE=files"]
CMD ["python3", "app.py"]
