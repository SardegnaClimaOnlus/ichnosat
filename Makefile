build_template:
	cd /usr/ichnosat/scientific-processor/src/plugins/template/; \
	g++ -fPIC -shared -I/usr/local/include /usr/local/lib/libgdal.so.20.1.2  *.cc -o build/template.so;
run_template:
	cd /usr/ichnosat/scientific-processor/src/plugins/template/; \
	python3.4 load_test.py
sender_test:
	cd /usr/ichnosat/scientific-processor/src/; \
	python3.4 send_message.py
start-scientific-processor:
	cd /usr/ichnosat/scientific-processor/src/; \
	service rabbitmq-server start; \
	python3.4 main.py
start-rabbitmq:
	service rabbitmq-server start


