FROM python:3.8-slim-buster
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ~/.aws/credentials credentials
RUN mkdir ~/.aws
RUN mv credentials ~/.aws/credentials
EXPOSE 80
COPY . .
ENV FLASK_APP=wordle_target.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
