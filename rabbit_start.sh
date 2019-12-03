bash -c "rabbitmq-plugins enable rabbitmq_management;
sleep 3;
rabbitmqctl add_user admin admin
&& rabbitmqctl set_user_tags admin administrator
&& rabbitmqctl set_permissions -p / admin ".*" ".*" ".*";
sleep 3;
rabbitmq-server"