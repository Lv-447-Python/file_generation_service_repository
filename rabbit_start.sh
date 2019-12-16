bash -c "rabbitmq-plugins enable rabbitmq_management;
sleep 3;
rabbitmqctl add_user guest
&& rabbitmqctl set_user_tags guest administrator
&& rabbitmqctl set_permissions -p / guest  ".*" ".*" ".*";
sleep 3;
rabbitmq-server"