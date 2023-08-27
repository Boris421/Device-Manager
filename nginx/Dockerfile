FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY django-uwsgi.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/ &&  ln -s "/etc/nginx/sites-available/django-uwsgi.conf" "/etc/nginx/sites-enabled/django-uwsgi.conf"
CMD ["nginx", "-g", "daemon off;"]