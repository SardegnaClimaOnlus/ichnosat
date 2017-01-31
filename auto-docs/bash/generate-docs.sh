

sphinx-apidoc  -o /usr/ichnosat/auto-docs/source/ /usr/ichnosat/src/
make -C /usr/ichnosat/auto-docs/ html
make -C /usr/ichnosat/auto-docs/ epub
