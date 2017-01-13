g++ -fPIC \
    -shared \
    -I/usr/local/include \
    /usr/local/lib/libgdal.so.20.1.2  \
    $1/$2/*.cc -o \
    $1/$2/build/$2.so ;

