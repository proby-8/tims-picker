CC = gcc
CFLAGS = -fPIC -shared
LIBS = 

all: sharedLib.so myLib

sharedLib.so: testingC.c helper.c testingC.h
	$(CC) $(CFLAGS) $(LIBS) testingC.c helper.c -o sharedLib.so

myLib: testingC.c
	$(CC) -c testingC.c -o myLib