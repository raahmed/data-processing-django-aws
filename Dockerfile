FROM python:3

ADD . /web_project
COPY start.sh /start.sh

WORKDIR /web_project

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["/start.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]