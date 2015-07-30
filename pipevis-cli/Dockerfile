FROM python:2-wheezy

COPY pipevis-cli.py /usr/bin/pipevis-cli
run chmod +x /usr/bin/pipevis-cli
run mkdir /var/pipeline-data
run pip install click


ENTRYPOINT ["pipevis-cli"]
