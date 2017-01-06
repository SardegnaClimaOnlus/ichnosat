g++ -fPIC \
    -shared \
    -I/usr/local/include \
    /usr/local/lib/libgdal.so.20.1.2  \
    /usr/ichnosat/scientific-processor/src/plugins/$1/*.cc -o \
    /usr/ichnosat/scientific-processor/src/plugins/$1/build/$1.so ;

