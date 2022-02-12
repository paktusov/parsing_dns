FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY /deploy/nginx/default.conf /etc/nginx/conf.d/

RUN mkdir -p /var/www/static/

COPY /app/web/static/. /var/www/static/

CMD ["nginx", "-g", "daemon off;"]