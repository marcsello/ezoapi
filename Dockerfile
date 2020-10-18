FROM python:3

ADD ezoapi requirements.txt /ezoapi/
WORKDIR /ezoapi/

RUN pip3 install -r requirements.txt && pip3 install gunicorn

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]

