FROM python:wheezy

RUN pip install Flask && mkdir /tmp/pipevis
COPY core /tmp/pipevis/core
COPY static /tmp/pipevis/static
COPY app.py /tmp/pipevis/app.py
EXPOSE 5000

CMD [ "python", "/tmp/pipevis/app.py" ]
