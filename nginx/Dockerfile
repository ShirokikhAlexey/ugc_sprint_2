FROM nginx:1.19.2
COPY nginx.conf /etc/nginx/
COPY configs/default.conf.template /etc/nginx/templates/
COPY wait-for-it.sh /docker-entrypoint.d
