#ifdef _CH_
#pragma package <opencv>
#endif

#ifndef _EiC
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <string.h>
#endif

#define FIRSTIMG "./blue/1.jpg"
#define IMAGEDIR "./blue/"
int imageIdx = 51;

int levels = 2;
CvSeq* contours = 0;
int threshold = 167;
IplImage* source = 0;
IplImage* img = 0;
IplImage* cnt_img = 0;
CvMemStorage* storage = 0;


///A utility function to reverse the characters in a string (char array)
void reverse(char s[]){
		 int c,i,j;
		 for( i=0, j=strlen(s)-1; i<j; i++,j--){
					c = s[i];
					s[i] = s[j];
					s[j] = c;
		 }
}

///A utility function to convert an integer into a character array
void int2str(int n, char s[]){
	int i, sign;

	if( (sign=n) < 0 )
		 n = -n;
	i=0;
	do{
			s[i++] = n%10 + '0';
			} while ( (n /=10 ) > 0);
	if( sign < 0 )
		 s[i++] = '-';
	s[i] = '\0';
	reverse(s);
}

///when the user changes the threshold slider, this function is called
void on_thresh_change(int pos){
		//some pre-processing, threshold, smooth, erosion
		cvThreshold(source, img, threshold, 255, CV_THRESH_BINARY);
		cvSmooth(img,img,CV_GAUSSIAN,3, 0, 0, 0 );
		cvErode(img, img, NULL, 1);
		cvDilate(img, img, NULL, 1);
		cvShowImage( "thresholded", img );

		// find contours of blobs, allow for nested contours
		if(contours > 0) cvRelease((void*)&contours);	//release old data first...
		cvFindContours( img, storage, &contours, sizeof(CvContour),
										CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, cvPoint(0,0) );

		// find polygon approximation of contours
		contours = cvApproxPoly( contours, sizeof(CvContour), 
							 storage, CV_POLY_APPROX_DP, 3, 1 );

		//erase contour image (whatever might have been drawn last time...)
		cvZero( cnt_img );
		//draw the new contours
		cvDrawContours( cnt_img, contours, CV_RGB(255,0,0), CV_RGB(0,255,0), 
										levels, 3, CV_AA, cvPoint(0,0) );
		//and show the results
		cvShowImage( "contours", cnt_img );
}

///when a user changes the image index slider bar, this function is called
void on_imageIdx_change(int pos){
		char filename[255] = IMAGEDIR;
		char tmp[5];

		//build filename string from base directory, image index, .jpg extension
		int2str(imageIdx, tmp);
		strcat(filename, tmp );
		strcat(filename, ".jpg");

		//load image, get the negative image, display in a window
		if( source > 0) cvReleaseImage(&source); //release prev image first...
		source = cvLoadImage( filename, CV_LOAD_IMAGE_GRAYSCALE ); //load new image
		cvSubRS(source, cvRealScalar(255), source, NULL); //image negative
		cvShowImage("source", source);	//display it

		on_thresh_change(threshold);
}

/*main function. Finds the polygon approximations to the contours present
	in the negative image. Simple thresholding is done to separate the
	area of interest (a shadow projected onto a screen, which will be dark)
	from the background.*/
int main( int argc, char** argv )
{
		storage = cvCreateMemStorage(0); 

		//load the "first image" so we can get the dimensions, etc.
		source = cvLoadImage( FIRSTIMG, CV_LOAD_IMAGE_GRAYSCALE ); 
		img = cvCreateImage(cvGetSize(source), 8, 1);
		cnt_img = cvCreateImage( cvGetSize(source), 8, 3 );

		//setup a window for the source image and a slider bar
		cvNamedWindow( "source", 1 );
		cvCreateTrackbar("image number", "source", &imageIdx, 158,
				on_imageIdx_change);

		//setup another window for the thresholded image and a slider bar
		cvNamedWindow( "thresholded", 1 );
		cvCreateTrackbar( "thresh", "thresholded", &threshold, 255, on_thresh_change );

		//setup a third window to display the found contours
		cvNamedWindow( "contours", 1 );

		//kick it off the first time, then it's all event handling
		on_imageIdx_change(51);	//start with image 51 for example...

		//exit when user hits esc key
		cvWaitKey(0);

		//release memory
		cvReleaseMemStorage( &storage );
		cvReleaseImage( &cnt_img );
		cvReleaseImage( &img );
		cvReleaseImage( &source);
		return 0;
}

#ifdef _EiC
main(1,"");
#endif
