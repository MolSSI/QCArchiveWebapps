FROM alpine:latest

LABEL MAINTAINER="Doaa Altarawy <doaa.altarawy@gmail.com>"

RUN apk --update add nginx && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    mkdir /etc/nginx/sites-enabled/ && \
    mkdir -p /run/nginx && \
    rm -rf /etc/nginx/conf.d/default.conf && \
    rm -rf /var/cache/apk/*

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

EXPOSE 443

RUN wget https://dl.eff.org/certbot-auto && \
    mv certbot-auto /usr/local/bin/certbot-auto && \
    chown root /usr/local/bin/certbot-auto && \
    chmod 0755 /usr/local/bin/certbot-auto && \
    /usr/local/bin/certbot-auto --nginx && \
    echo "0 0,12 * * * root /usr/local/bin/certbot-auto renew -q" | sudo tee -a /etc/crontab > /dev/null

CMD ["nginx", "-g", "daemon off;"]