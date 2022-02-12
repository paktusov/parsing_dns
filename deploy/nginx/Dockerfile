FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY /deploy/nginx/default.conf /etc/nginx/conf.d/

RUN mkdir -p /date/static/

COPY /app/web/static/. /etc/nginx/date/static/

CMD ["nginx", "-g", "daemon off;"]