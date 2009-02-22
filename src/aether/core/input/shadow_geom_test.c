#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "shadow_geom.h"

vertex_set_t* vertex_set_create(int size)
{
	vertex_set_t* vertex_set;
	vertex_set=vertex_set_new();
	for(int i=0;i<size;i++)
		assert(true==vertex_set_append(vertex_set,vertex_new(i+3,i+4)));
	return vertex_set;
}

void vertex_set_check(vertex_set_t* vertex_set)
{
	FOR_EACH_VERTEX(pos,vertex_set)
	{
		assert(pos+3==vertex_set->vertices[pos]->x);
		assert(pos+4==vertex_set->vertices[pos]->y);
	}
}

void polygon_check(polygon_t* polygon)
{
	FOR_EACH_COMPONENT(pos,polygon)
	{
		vertex_set_check(polygon->components[pos]);
	}
}

int main(int ac,char **av)
{
	printf("Running shadow_geom tests...\n");

	/* Test vertex functions */
	vertex_t* vertex;
	vertex=NULL;
	vertex=vertex_new(1,2);
	assert(NULL!=vertex);
	assert(1==vertex->x);
	assert(2==vertex->y);
	vertex_free(&vertex);
	assert(NULL==vertex);

	/* Test vertex_set functions */
	vertex_set_t* vertex_set;
	vertex_set=NULL;
	vertex_set=vertex_set_new();
	assert(NULL!=vertex_set);
	assert(0==vertex_set->length);
	assert(NULL==vertex_set->vertices);
	vertex_set_free(&vertex_set);
	assert(NULL==vertex_set);

	vertex_set=vertex_set_new();
	assert(NULL!=vertex_set);
	vertex=vertex_new(3,4);
	assert(true==vertex_set_append(vertex_set,vertex));
	assert(1==vertex_set->length);
	assert(3==vertex_set->vertices[0]->x);
	assert(4==vertex_set->vertices[0]->y);
	vertex_set_free(&vertex_set);
	assert(NULL==vertex_set);

	for(int i=0;i<10;i++)
	{
		vertex_set=vertex_set_create(4);
		assert(NULL!=vertex_set);
		vertex_set_check(vertex_set);
		vertex_set_free(&vertex_set);
		assert(NULL==vertex_set);
	}

	/* Polygon tests */
	polygon_t* polygon;
	polygon=NULL;
	polygon=polygon_new();
	assert(NULL!=polygon);
	polygon_free(&polygon);
	assert(NULL==polygon);

	for(int i=0;i<10;i++)
	{
		polygon=polygon_new();
		for(int j=0;j<=i;j++)
			polygon_append(polygon,vertex_set_create(5));
		assert(i+1==polygon->num_components);
		polygon_check(polygon);
		polygon_free(&polygon);
		assert(NULL==polygon);
	}

	printf("All shadow_geom tests passed!\n");

	return 0;
}
