export PYTHONPATH=/usr/ichnosat/
python3.4 src/core/system_manager/init.py
nohup supervisord -c /usr/ichnosat/src/core/system_manager/config/supervisord.conf &
sleep infinity