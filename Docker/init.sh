( rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user admin password 2>/dev/null ; \
rabbitmqctl set_user_tags admin administrator ; \
rabbitmqctl set_permissions -p / admin  ".*" ".*" ".*" ; \
echo "*** User 'admin' with password '230251' completed. ***" ; \
echo "*** Log in the WebUI at port 5672 (example: http:/localhost:5672) ***") &
