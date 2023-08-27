FROM python:3.10

WORKDIR /device_manager
COPY . /device_manager/
RUN pip install -r requirements.txt
RUN 
EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
CMD python manage.py runserver 0.0.0.0:8000