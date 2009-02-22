#include "img_capture.h"

int main( int argc, char** argv )
{

  /*
  CvCapture* capture;
  capture = cvCaptureFromCAM(0); // capture from video device #0

  //double frameH    = cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
  //double frameW    =  cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);
  
  double frameH = 24;
  double frameW = 32;

  cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_HEIGHT,frameH);
  cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_WIDTH,frameW);
  IplImage* source;
  cvNamedWindow( "source", 24 );

  
  while(1) {
    source = cvQueryFrame(capture);
    cvShowImage("source", source);  

    if(cvWaitKey(0)) break;
  }

  cvReleaseCapture(&capture);

  */

  calibrate_manual(NULL);

  vertex_set_t* verts = get_verts();

  printf("%d\n",verts->length);
  vertex_t* t;
  for(int i = 0; i < verts->length; i++) {
    t = verts->vertices[i];
    printf("%d,%d ",t->x,t->y);
  }
  printf("\n");

  polygon_set_t* polys = get_polys();
  polygon_t* poly;

  printf("polys->num_components = %d\n",polys->num_components);
  for(int i = 0; i < polys->num_components; i++) {
    poly = polys->components[i];
    printf("poly->num_components = %d\n",poly->num_components);
    verts = poly->components[0];
    printf("verts->length = %d\n",verts->length);

    for(int i = 0; i < verts->length; i++) {
      t = verts->vertices[i];
      printf("%d,%d ",t->x,t->y);
    }
    printf("\n");
  }

}
