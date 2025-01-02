FROM public.ecr.aws/docker/library/python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD uvicorn configs.app.config.main:app --workers 4 --host 0.0.0.0 --port 11005

