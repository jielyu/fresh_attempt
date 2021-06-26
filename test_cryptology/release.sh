
# create and enter build/ dir
if ! [ -d build ]; then
    mkdir build && cd build
else
    cd build
fi

# run compiler
cmake .. && make

# run demos
./crypt_impl

# return back dir
cd ..

