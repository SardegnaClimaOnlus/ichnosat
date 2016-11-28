build_template:
	cd /usr/ichnosat/scientific-processor/src/plugins/template/; \
	g++ -fPIC -shared -I/usr/local/include /usr/local/lib/libgdal.so.20.1.2  *.cc -o build/template.so;
run_template:
	cd /usr/ichnosat/scientific-processor/src/plugins/template/; \
	python3.4 load_test.py



