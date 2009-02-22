#include "img_capture.h"

int threshold;
int min_contour_area;

// capture stuff
CvCapture* capture;
IplImage* raw;
IplImage* src;
IplImage* dst;
double frameW, frameH;
CvPoint mousePos;
CvSeq* contours;
CvMemStorage* storage1;
CvMemStorage* storage2;

// perspective related members
CvPoint2D32f* src_crd;
CvPoint2D32f* dst_crd;
CvMat* map;

void startup() {

	storage1 = cvCreateMemStorage(0);
	storage2 = cvCreateMemStorage(0);

	capture = cvCaptureFromCAM(0); // capture from video device #0
	//frameH		= (int) cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
	//frameW		= (int) cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);

	frameH = 240;
	frameW = 320;

	cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, frameH);
	cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, frameW);

	raw=get_img();	// retrieve the captured frame
	src=cvCloneImage(raw);	// retrieve the captured frame
	dst=cvCreateImage(cvSize(frameW,frameH),src->depth,src->nChannels);

	threshold = 224;
	min_contour_area = 2000;

	mousePos = cvPoint(0,0);

	// the rest is for perspective stuff
	map = cvCreateMat(3,3,CV_32FC1);
	cvSetIdentity(map,cvRealScalar(2));

	src_crd = (CvPoint2D32f*) malloc(sizeof(CvPoint2D32f)*4);
	dst_crd = (CvPoint2D32f*) malloc(sizeof(CvPoint2D32f)*4);

	src_crd[0] = cvPoint2D32f(0,0);
	src_crd[1] = cvPoint2D32f(frameW,0);
	src_crd[2] = cvPoint2D32f(frameW,frameH);
	src_crd[3] = cvPoint2D32f(0,frameH);

	dst_crd[0] = cvPoint2D32f(0,0);
	dst_crd[1] = cvPoint2D32f(frameW,0);
	dst_crd[2] = cvPoint2D32f(frameW,frameH);
	dst_crd[3] = cvPoint2D32f(0,frameH);

}

void set_persp_coord(int coord, CvPoint* pt) {
	src_crd[coord].x = (float)pt->x;
	src_crd[coord].y = (float)pt->y;
}

void set_threshold(int t) {
	threshold = t;
}

void set_min_contour_area(int t) {
	min_contour_area = t;
}

void do_perspective(IplImage* src, IplImage* dst, CvMat* map) {
		CvMat* persp_mat = cvGetPerspectiveTransform(src_crd,dst_crd,map);
		cvWarpPerspective(src,dst,persp_mat,CV_INTER_LINEAR+CV_WARP_FILL_OUTLIERS,cvScalarAll(0));
}

void mouse_callback(int event, int x, int y, int flags, void* param) {
	mousePos = cvPoint(x,y);
}

IplImage* get_img() {
	if(!cvGrabFrame(capture))							// capture a frame
		return NULL;
	return cvRetrieveFrame(capture);	// retrieve the captured frame
}

IplImage* get_mod() {
	do_perspective(get_img(),dst,map);
	return dst;
}

IplImage* get_thresholded() {

	IplImage* source = get_mod();
	IplImage* conv = cvCreateImage(cvGetSize(source), source->depth, 1);
	cvCvtColor(source,conv,CV_RGB2GRAY);
	cvSubRS(conv, cvRealScalar(255), conv, NULL); //image negative

	IplImage* img = cvCreateImage(cvGetSize(source), source->depth, 1);

	// some pre-processing, threshold, smooth, erosion
	cvThreshold(conv, img, threshold, 255, CV_THRESH_BINARY);
	cvSmooth(img,img,CV_GAUSSIAN,3, 0, 0, 0 );
	cvErode(img, img, NULL, 1);
	cvDilate(img, img, NULL, 1);

	cvReleaseImage(&conv);

	return img;

}

polygon_set_t* get_polys() {

	contours = get_cv_polys();

	polygon_set_t* polys;
	polys = polygon_set_new();
	polys->num_components = 0;

	if(!contours) return polys;

	CvSeqReader reader;
	cvStartReadSeq(contours, &reader, 0);

	//printf("===========================\n");
	int i;
	polygon_t* poly;
	vertex_set_t* verts;

	for(; contours!=0;contours=contours->h_next) {

			verts = vertex_set_new();

			poly = polygon_new();
			polygon_append(poly,verts);

			polygon_set_append(polys,poly);

			//printf("%d(%f):",contours->total,cvContourArea(contours,CV_WHOLE_SEQ));
			for( i = 0; i < contours->total; i++ ) {
				CvPoint p;
				p = *(CvPoint*)cvGetSeqElem(contours,i);
				//CV_READ_SEQ_ELEM(p,reader);
				//printf("%d,%d ",p.x,p.y);
				vertex_set_append(verts,vertex_new((int)(100*p.x/frameW),(int)(100*p.y/frameH)));
				//vertex_set_append(verts,vertex_new(p.x,p.y));
			//printf("\n");
			}
	}

	//printf("===========================\n");

	return polys;

}

CvSeq* get_cv_polys() {

	IplImage* img = get_thresholded();

	// find contours of blobs, allow for nested contours
	if(contours > 0) cvRelease((void *)&contours);	//release old data first...
	cvFindContours( img, storage1, &contours, sizeof(CvContour),
									CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, cvPoint(0,0) );


	// find polygon approximation of contours
	if(contours) contours = cvApproxPoly( contours, sizeof(CvContour), storage1, CV_POLY_APPROX_DP, 3, 1 );

	cvReleaseImage(&img);

	CvSeq* contours_itr = contours;

	if(contours) {
		int area = 0;

		for(; contours_itr!=0 ;contours_itr=contours_itr->h_next) {
			area = cvContourArea(contours_itr,CV_WHOLE_SEQ);
			if(abs(area) < min_contour_area) {

				if(!contours_itr->h_prev && !contours_itr->h_next) { // only thing in the list, set contours to 0 and get the hell outta here
					contours = 0;
					break;
				}

				if(contours_itr->h_prev) {
					contours_itr->h_prev->h_next = contours_itr->h_next;
				} else {
					contours_itr->h_next->h_prev = 0;
					contours = contours_itr->h_next;
				}

				if(contours_itr->h_next) {
					contours_itr->h_next->h_prev = contours_itr->h_prev;
				} else {
					contours_itr->h_prev->h_next = 0;
					break;
				}
			}
		}
	}
	return contours;
}

vertex_set_t* get_verts() {

	contours = get_cv_polys();

	vertex_set_t* verts;
	verts = vertex_set_new();

	if(!contours) return verts;

	CvSeqReader reader;
	cvStartReadSeq(contours, &reader, 0);
	CvSeq* maxContour = 0;

	int max_area = 0, cur_max = 0, i;
	for(; contours!=0;contours=contours->h_next) {
		cur_max = (int)abs(cvContourArea(contours,CV_WHOLE_SEQ));
		if( cur_max > max_area) {
			max_area = cur_max;
			maxContour = contours;
		}
	}

	for( i = 0; i < maxContour->total; i++ ) {
		CvPoint p;
		p = *(CvPoint*)cvGetSeqElem(maxContour,i);
		vertex_set_append(verts,vertex_new((int)(100*p.x/frameW),(int)(100*p.y/frameH)));
		//vertex_set_append(verts,vertex_new(p.x,p.y));
	}

	return verts;

}

vertex_t* get_com() {
	vertex_set_t *verts;
	vertex_t *vert,*curr_vert;

	vert=vertex_new(0,0);

	verts=get_verts();

	FOR_EACH_VERTEX(pos,verts)
	{
		curr_vert=verts->vertices[pos];
		vert->x=(vert->x+curr_vert->x)/((float)verts->length);
		vert->y=(vert->y+curr_vert->y)/((float)verts->length);
	}

	/* Normalize to 0-100 */
	vert->x=(int)(vert->x*100.)/(float)frameW;
	vert->y=(int)(vert->y*100.)/(float)frameH;

	return vert;
}

void shutdown() {
	free(src_crd);
	free(dst_crd);
	cvReleaseCapture(&capture);
	cvReleaseImage(&src);
	cvReleaseImage(&dst);
	cvRelease((void *)map);
	cvReleaseMemStorage(&storage1);
	cvReleaseMemStorage(&storage2);
}

settings_t* settings_new(int threshold,vertex_set_t *transform,int min_area)
{
	settings_t *settings;
	settings=NULL;
	settings=malloc(sizeof(settings_t));
	if(NULL!=settings)
	{
		settings->threshold=threshold;
		settings->transform=transform;
		settings->min_area=min_area;
	}
	return settings;
}

void settings_free(settings_t **settings)
{
	vertex_set_free(&(*settings)->transform);
	free(*settings);
	*settings=NULL;
}

void settings_get(settings_t *settings)
{
	if(NULL!=settings)
	{
		threshold=settings->threshold;
		min_contour_area=settings->min_area;
		if(settings->transform->vertices) {
			for(int i=0;i<4;i++)
			{
				src_crd[i].x = (float)settings->transform->vertices[i]->x;
				src_crd[i].y = (float)settings->transform->vertices[i]->y;
			}
		}
	}
}

void settings_set(settings_t *settings)
{
	if(NULL!=settings)
	{
		settings->threshold=threshold;
		settings->min_area=min_contour_area;
		if(settings->transform->vertices) {
			printf("Setting existing vertices\n");
			for(int i=0;i<4;i++)
			{
				settings->transform->vertices[i]->x=(int)src_crd[i].x;
				settings->transform->vertices[i]->y=(int)src_crd[i].y;
			}
		} else { //settings->transform->vertices was never populated, has no memory
			printf("No existing vertices\n");
			for(int i=0;i<4;i++)
				vertex_set_append(settings->transform,vertex_new(src_crd[i].x,src_crd[i].y));
		}
	}
}

void calibrate_manual(settings_t* settings) {

	printf("To set the perspective transform:\n");
	printf("\tPlace mouse over desired coordinate in 'source' window\n");
	printf("\tPress 1,2,3, or 4 for the top left, top right, bottom right, or bottom left coordinate as necessary.\n");

	if(storage1 == 0) startup();

	settings_get(settings);

	cvNamedWindow( "source", 24 );
	//cvNamedWindow( "dest", 24 );
	cvNamedWindow( "threshold", 24);
	cvCreateTrackbar( "thresh", "threshold", &threshold, 255, set_threshold);

	cvNamedWindow( "contours", 24);
	cvCreateTrackbar( "min_area", "contours", &min_contour_area, 10000, set_min_contour_area);

	cvSetMouseCallback("source",mouse_callback,NULL);

	CvFont font;
	cvInitFont( &font, CV_FONT_HERSHEY_COMPLEX_SMALL, 1, 1, 0.0, 1, CV_AA);

	int key;
	IplImage* source;
	//IplImage* dest;
	IplImage* thresh;
	IplImage* contour;

	//CvSeq* contours;

	source = get_img();
	//dest = cvCreateImage(cvGetSize(source), source->depth, source->nChannels);
	thresh = cvCreateImage(cvGetSize(source), source->depth, 1);
	contour = cvCreateImage( cvGetSize(source), source->depth, source->nChannels );
	//cvCvtColor(source,thresh,CV_RGB2GRAY);

	while(1) {

		// get the source image
		source = get_img();
		//dest = get_mod();
		thresh = get_thresholded();
		contours = get_cv_polys();

		//erase contour image (whatever might have been drawn last time...)
		cvZero( contour );
		//draw the new contours
		int levels = 1;
		if(contours) cvDrawContours( contour, contours, CV_RGB(255,0,0), CV_RGB(0,255,0), levels, 3, CV_AA, cvPoint(0,0) );

		// draw the four source coordinates
		cvPutText(source, "1", cvPointFrom32f(src_crd[0]), &font, CV_RGB(255,0,0));
		cvCircle(source,cvPointFrom32f(src_crd[0]),2,CV_RGB(255,0,0),-1,8,0);
		cvPutText(source, "2", cvPointFrom32f(src_crd[1]), &font, CV_RGB(255,0,0));
		cvCircle(source,cvPointFrom32f(src_crd[1]),2,CV_RGB(255,0,0),-1,8,0);
		cvPutText(source, "3", cvPointFrom32f(src_crd[2]), &font, CV_RGB(255,0,0));
		cvCircle(source,cvPointFrom32f(src_crd[2]),2,CV_RGB(255,0,0),-1,8,0);
		cvPutText(source, "4", cvPointFrom32f(src_crd[3]), &font, CV_RGB(255,0,0));
		cvCircle(source,cvPointFrom32f(src_crd[3]),2,CV_RGB(255,0,0),-1,8,0);

		//display it
		cvShowImage("source", source);
		//cvShowImage("dest", dest);
		cvShowImage("threshold", thresh);
		cvShowImage("contours", contour );

		if((key = cvWaitKey(3)) >= 0) {
			//printf("key=%d\n",key);
			fflush(stdout);
			if(key == 27 || key == 1048603)
			{
					//printf("breaking...\n");
					break;
			}
			else {
				switch(key) {
					case 49: // pressed 1
					case 1048625:
						//printf("1 pressed...\n");
						set_persp_coord(0,&mousePos);
						break;
					case 50: // pressed 2
					case 1048626:
						//printf("2 pressed...\n");
						set_persp_coord(1,&mousePos);
						break;
					case 51: // pressed 3
					case 1048627:
						//printf("3 pressed...\n");
						set_persp_coord(2,&mousePos);
						break;
					case 52: // pressed 4
					case 1048628:
						//printf("4 pressed...\n");
						set_persp_coord(3,&mousePos);
						break;
				}
			}
		}
	}

	//cvReleaseImage(&source);
	cvReleaseImage(&thresh);
	cvReleaseImage(&contour);

	//cvReleaseImage(&dest);
	cvDestroyWindow("source");
	//cvDestroyWindow("dest");
	cvDestroyWindow("threshold");
	cvDestroyWindow("contours");
	//cvRelease((void *)&font);
	//cvRelease((void *)&contours);

	//printf("1:(%f,%f) ",src_crd[0].x,src_crd[0].y);
	//printf("2:(%f,%f) ",src_crd[1].x,src_crd[1].y);
	//printf("3:(%f,%f) ",src_crd[2].x,src_crd[2].y);
	//printf("4:(%f,%f) ",src_crd[3].x,src_crd[3].y);
	//printf("thresh:%d\n",threshold);

	settings_set(settings);
}
