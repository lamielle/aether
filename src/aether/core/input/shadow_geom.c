#include <stdbool.h>
#include <stdlib.h>
#include "shadow_geom.h"

vertex_t* vertex_new(int x,int y)
{
	vertex_t* vertex;
	vertex=malloc(sizeof(vertex_t));
	if(NULL!=vertex)
	{
		vertex->x=x;
		vertex->y=y;
	}
	return vertex;
}

void vertex_free(vertex_t** vertex)
{
	free(*vertex);
	*vertex=NULL;
}

vertex_set_t* vertex_set_new()
{
	vertex_set_t* vertex_set;
	vertex_set=NULL;
	vertex_set=malloc(sizeof(vertex_set_t));
	if(NULL!=vertex_set)
	{
		vertex_set->vertices=NULL;
		vertex_set->length=0;
	}
	return vertex_set;
}

void vertex_set_free(vertex_set_t** vertex_set)
{
	FOR_EACH_VERTEX(pos,(*vertex_set))
	{
		vertex_free(&(*vertex_set)->vertices[pos]);
	}
	free((*vertex_set)->vertices);
	(*vertex_set)->vertices=NULL;
	free(*vertex_set);
	*vertex_set=NULL;
}

bool vertex_set_append(vertex_set_t* vertex_set,vertex_t* vertex)
{
	vertex_t** new_vertices;
	bool res;
	res=false;

	new_vertices=NULL;
	new_vertices=realloc(vertex_set->vertices,sizeof(vertex_t*)*(vertex_set->length+1));
	if(NULL!=new_vertices)
	{
		vertex_set->vertices=new_vertices;
		vertex_set->vertices[vertex_set->length]=vertex;
		vertex_set->length+=1;
		res=true;
	}
	return res;
}

polygon_t* polygon_new()
{
	polygon_t* polygon;
	polygon=NULL;
	polygon=malloc(sizeof(polygon_t));
	if(NULL!=polygon)
	{
		polygon->components=NULL;
		polygon->num_components=0;
	}
	return polygon;
}

void polygon_free(polygon_t** polygon)
{
	FOR_EACH_COMPONENT(pos,(*polygon))
	{
		vertex_set_free(&(*polygon)->components[pos]);
	}
	free((*polygon)->components);
	(*polygon)->components=NULL;
	free(*polygon);
	*polygon=NULL;
}

bool polygon_append(polygon_t* polygon,vertex_set_t* component)
{
	vertex_set_t** new_vertex_sets;
	bool res;
	res=false;

	new_vertex_sets=NULL;
	new_vertex_sets=realloc(polygon->components,sizeof(vertex_set_t*)*(polygon->num_components+1));
	if(NULL!=new_vertex_sets)
	{
		polygon->components=new_vertex_sets;
		polygon->components[polygon->num_components]=component;
		polygon->num_components+=1;
		res=true;
	}
	return res;
}

polygon_set_t* polygon_set_new()
{
	polygon_set_t* polygon_set;
	polygon_set=NULL;
	polygon_set=malloc(sizeof(polygon_set_t));
	if(NULL!=polygon_set)
	{
		polygon_set->components=NULL;
		polygon_set->num_components=0;
	}
	return polygon_set;
}

void polygon_set_free(polygon_set_t** polygon_set)
{
	FOR_EACH_COMPONENT(pos,(*polygon_set))
	{
		polygon_free(&(*polygon_set)->components[pos]);
	}
	free((*polygon_set)->components);
	(*polygon_set)->components=NULL;
	free(*polygon_set);
	*polygon_set=NULL;
}

bool polygon_set_append(polygon_set_t* polygon_set,polygon_t* component)
{
	polygon_t** new_polygon_set;
	bool res;
	res=false;

	new_polygon_set=NULL;
	new_polygon_set=realloc(polygon_set->components,sizeof(polygon_t*)*(polygon_set->num_components+1));
	if(NULL!=new_polygon_set)
	{
		polygon_set->components=new_polygon_set;
		polygon_set->components[polygon_set->num_components]=component;
		polygon_set->num_components+=1;
		res=true;
	}
	return res;
}
