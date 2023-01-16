FROM python:3.9

WORKDIR /code

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

COPY ./app /code/app

EXPOSE 8000

CMD sed -i.bak 's#<URL>#'$URL'#' app/omada.cfg; \
    sed -i.bak 's/<USERNAME>/'$USERNAME'/' app/omada.cfg; \
    sed -i.bak 's/<PASSWORD>/'$PASSWORD'/' app/omada.cfg; \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
