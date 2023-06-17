FROM python:3.8
WORKDIR /app/vhostPop
RUN mkdir -p /app/containers
RUN mkdir -p /app/containers/nginx/vhost.d
COPY . .
RUN echo "* * * * * /usr/local/bin/python /app/vhostPop/vhostPop.py > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/cronjob
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install cron
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN touch /var/log/cron.log
RUN touch /app/vhostPop/vhost_pop_logs.log
CMD cron && tail -f /app/vhostPop/vhost_pop_logs.log