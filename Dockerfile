FROM python:3.9

WORKDIR /myApp
 
COPY ./requirements.txt /myApp/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /myApp/requirements.txt
COPY . /myApp
ENV DOCKER_RUNNING Yes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
