CC = gcc
CFLAGS = -fPIC -shared
LIBS = 

all: sharedLib.so myLib

sharedLib.so: testingC.c
	$(CC) $(CFLAGS) $(LIBS) testingC.c -o sharedLib.so

myLib: testingC.c
	$(CC) -c testingC.c -o myLib