FROM ubuntu
RUN apt-get update -y
RUN apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y nginx python3 python3-pip gunicorn cron sudo net-tools nano postgresql-contrib libpq-dev postgresql-contrib libpq-dev
COPY ./ /srv/hackathon
WORKDIR /srv/hackathon
RUN pip3 install -r requirements.txt && cp /srv/hackathon/nginx.conf /etc/nginx/sites-available/default
RUN chown -R www-data:www-data /srv/hackathon && chmod +x /srv/hackathon/run.sh
EXPOSE 89:89
ENTRYPOINT /srv/hackathon/run.sh
