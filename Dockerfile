FROM python:2-onbuild

EXPOSE 3000

RUN mkdir /pick

WORKDIR /pick

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]
