# build.sh - Build script for compiling LoanInfo source code.

# Compile microservice.
gcc -c -fPIC -I/usr/include/python3.8 -o loan_info.o lib/c/loan_info.c
gcc -shared -fPIC -I/usr/include/python3.8 -o lib/ext/loan_info.so loan_info.o

# Compile tools for date interpolation. 
gcc -c -fPIC -I/usr/include/python3.8 -o kronos.o kronos.c
gcc -shared -fPIC -I/usr/include/python3.8 -o kronos.so kronos.o
