FROM python:3.9  

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/
COPY ./auth.py /code/
COPY ./settings.py /code/
COPY ./core /code/core
COPY ./v1 /code/v1
COPY ./scripts /code/scripts


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]