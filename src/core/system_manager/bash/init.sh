export PYTHONPATH=/usr/ichnosat/
nohup supervisord -c /usr/ichnosat/src/core/system_manager/config/supervisord.conf &
sleep infinity