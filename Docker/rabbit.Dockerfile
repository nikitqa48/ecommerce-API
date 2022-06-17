FROM rabbitmq
ENV RABBITMQ_USER admin
ENV RABBITMQ_PASSWORD password
ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq
ADD init.sh /init.sh
RUN chmod +x /init.sh
EXPOSE 5672
CMD ["/init.sh"]