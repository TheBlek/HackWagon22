FROM ubuntu
RUN apt update -y
RUN apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y nginx python3 python3-pip gunicorn cron sudo net-tools nano postgresql-contrib libpq-dev postgresql-contrib libpq-dev
COPY ./ /srv/hackathon
WORKDIR /srv/hackathon
RUN pip3 install -r requirements.txt && cp /srv/hackathon/nginx.conf /etc/nginx/sites-available/default
RUN chown -R www-data:www-data /srv/hackathon && chmod +x /srv/hackathon/run
EXPOSE 88:88
ENTRYPOINT /srv/hackathon/run
