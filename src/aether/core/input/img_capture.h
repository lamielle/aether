#ifndef _IMG_CAPTURE
#define _IMG_CAPTURE

#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "shadow_geom.h"

#define MIN_CONTOUR_AREA 3000

#define max(x,y) ((x) > (y) ? (x) : (y) )

// functions, etc
void startup();
void set_persp_coord(int,CvPoint*);
void do_perspective(IplImage*,IplImage*,CvMat*);
void mouse_callback(int,int,int,int,void*);
IplImage* get_img();
IplImage* get_mod();

// ILDP interface functions
//polygon_t** get_polys();
CvSeq* get_cv_polys();
polygon_set_t* get_polys();
vertex_set_t* get_verts();
vertex_t* get_com();

// ILDP interface helper functions
IplImage* get_thresholded();
void set_threshold(int);

void shutdown();

struct settings {
  int threshold;
  vertex_set_t *transform;
  int min_area;
};
typedef struct settings settings_t;

settings_t* settings_new(int threshold,vertex_set_t *transform,int min_area);
void settings_free(settings_t **settings);

void calibrate_manual(settings_t*);
void calibrate_auto(settings_t*);

#endif
