CC=gcc
INCLUDE=-I/usr/include/opencv
LIBS=-L/usr/lib -lcv -lcvaux -lhighgui

all: shadows camera

shadows:
	${CC} ${INCLUDE} ${LIBS} -o shadows shadows.c

camera:
	${CC} ${INCLUDE} ${LIBS} -fPIC -Wall -std=c99 -shared -o libimgcap.so img_capture.c shadow_geom.c
	${CC} ${INCLUDE} ${LIBS} -fPIC -Wall -std=c99 -L. -limgcap -o camera camera.c 

clean:
	rm -rf shadows camera
