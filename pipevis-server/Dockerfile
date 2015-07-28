FROM python:2-wheezy

RUN pip install Flask && mkdir /tmp/pipevis
COPY core /tmp/pipevis/core
COPY static /tmp/pipevis/static
COPY pipevis-backend.py /tmp/pipevis/pipevis-backend.py
EXPOSE 5000

ENTRYPOINT ["/tmp/pipevis/pipevis-backend.py"]
