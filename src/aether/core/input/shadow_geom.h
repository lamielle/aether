#include <stdbool.h>

#ifndef _SHAD_GEOM
#define _SHAD_GEOM

struct vertex {
  int x;
  int y;
};
typedef struct vertex vertex_t;

struct vertex_set {
  vertex_t** vertices;
  int length;
};
typedef struct vertex_set vertex_set_t;

struct polygon {
  vertex_set_t** components;
  int num_components;
};
typedef struct polygon polygon_t;

struct polygon_set {
  polygon_t** components;
  int num_components;
};
typedef struct polygon_set polygon_set_t;

vertex_t* vertex_new(int x,int y);
void vertex_free(vertex_t** vertex);

vertex_set_t* vertex_set_new();
void vertex_set_free(vertex_set_t** vertex_set);
bool vertex_set_append(vertex_set_t* vertex_set,vertex_t* vertex);

polygon_t* polygon_new();
void polygon_free(polygon_t** polygon);
bool polygon_append(polygon_t* polygon,vertex_set_t* vertex_set);

polygon_set_t* polygon_set_new();
void polygon_set_free(polygon_set_t** polygon_set);
bool polygon_set_append(polygon_set_t* polygon_set,polygon_t* polygon);


#define FOR_EACH_VERTEX(i,vertex_set) for(int i=0;i<vertex_set->length;i++)

#define FOR_EACH_COMPONENT(i,polygon) for(int i=0;i<polygon->num_components;i++)
#endif
