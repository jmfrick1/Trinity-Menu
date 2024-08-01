CC = g++
CFLAGS = -Wall
LIBS = -ldwmapi

all: overlay

overlay: overlay.cpp
	$(CC) $(CFLAGS) -o overlay overlay.cpp $(LIBS)

clean:
	rm -f overlay
