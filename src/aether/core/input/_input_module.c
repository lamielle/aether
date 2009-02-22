#include <Python.h>
#include "img_capture.h"
#include "shadow_geom.h"

static PyObject* make_2tuple()
{
	PyObject *tuple=PyTuple_New(2);
	PyTuple_SetItem(tuple,0,PyInt_FromLong(6));
	PyTuple_SetItem(tuple,1,PyInt_FromLong(7));
	return tuple;
}

static PyObject* get_tuple_from_vetex(vertex_t *vertex)
{
	PyObject *tuple;
	tuple=PyTuple_New(2);
	PyTuple_SetItem(tuple,0,PyInt_FromLong(vertex->x));
	PyTuple_SetItem(tuple,1,PyInt_FromLong(vertex->y));
	return tuple;
}
static PyObject* get_list_from_vertex_set(vertex_set_t *vertex_set)
{
	PyObject *list;
	list=PyList_New(0);
	if(NULL==list) return NULL;

	PyObject *tuple;
	FOR_EACH_VERTEX(pos,vertex_set)
	{
		PyList_Append(list,get_tuple_from_vetex(vertex_set->vertices[pos]));
	}

	return list;
}

static PyObject* get_list_from_polygon_set(polygon_set_t *polygon_set)
{
	PyObject *list;
	list=PyList_New(0);
	if(NULL==list) return NULL;

	PyObject *sub_list;
	FOR_EACH_COMPONENT(pos,polygon_set)
	{
		sub_list=get_list_from_vertex_set(polygon_set->components[pos]->components[0]);
		PyList_Append(list,sub_list);
	}

	return list;
}

static vertex_set_t* get_vertex_set_from_list(PyObject* list)
{
	Py_ssize_t length,pos;
	int x,y;
	PyObject *item;
	vertex_set_t *vert_set;
	vert_set=vertex_set_new();
	length=PySequence_Length(list);
	for(pos=0;pos<length;pos++)
	{
		item=PySequence_GetItem(list,pos);
		x=PyInt_AsLong(PySequence_GetItem(item,0));
		y=PyInt_AsLong(PySequence_GetItem(item,1));
		vertex_set_append(vert_set,vertex_new(x,y));
	}
	return vert_set;
}

static void get_settings_from_c(settings_t *settings,PyObject *pysettings)
{
	PyObject_SetAttrString(pysettings,"threshold",PyInt_FromLong(settings->threshold));
	PyObject_SetAttrString(pysettings,"transform",get_list_from_vertex_set(settings->transform));
	PyObject_SetAttrString(pysettings,"min_area",PyInt_FromLong(settings->min_area));
}

settings_t* get_settings_from_python(PyObject *pysettings)
{
	PyObject *threshold_obj,*transform_obj,*min_area_obj;
	int threshold, min_area;
	vertex_set_t *transform;

	/* Get the value in the 'threshold' attribute */
	threshold_obj=PyObject_GetAttrString(pysettings,"threshold");
	if(NULL==threshold_obj) return NULL;
	threshold=PyInt_AsLong(threshold_obj);

	/* Get the value in the 'transform' attribute */
	transform_obj=PyObject_GetAttrString(pysettings,"transform");
	if(NULL==transform_obj) return NULL;
	transform=get_vertex_set_from_list(transform_obj);

	/* Get the value in the 'min_area' attribute */
	min_area_obj=PyObject_GetAttrString(pysettings,"min_area");
	if(NULL==min_area_obj) return NULL;
	min_area=PyInt_AsLong(min_area_obj);

	return settings_new(threshold,transform,min_area);
}

/* Method stubs */
static PyObject* input_get_lp_pts(PyObject *self,PyObject *args){return make_2tuple();}

/* Startup */
static PyObject* input_startup(PyObject *self,PyObject *args){startup();Py_RETURN_NONE;}

/* Shutdown */
static PyObject* input_shutdown(PyObject *self,PyObject *args){shutdown();Py_RETURN_NONE;}

/* Returns the center of mass for the shadow */
static PyObject* input_get_com(PyObject *self,PyObject *args)
{
	return get_tuple_from_vetex(get_com());
}
/* Returns a collection of points around the shadow */
static PyObject* input_get_verts(PyObject *self,PyObject *args)
{
	vertex_set_t *verts;
	verts=get_verts();
	PyObject *vert_list=get_list_from_vertex_set(verts);
	vertex_set_free(&verts);
	return vert_list;
}

static PyObject* input_get_polys(PyObject *self,PyObject *args)
{
	polygon_set_t *polys;
	polys=get_polys();
	PyObject *polygon_list=get_list_from_polygon_set(polys);
	polygon_set_free(&polys);
	return polygon_list;
}

/* Runs either manual or automatic calibration using the given settings object */
static PyObject* input_calibrate(PyObject *self,PyObject *args)
{
	PyObject *pysettings;
	settings_t *settings;

	/* Parse the settings object from the arguments */
	if(!PyArg_ParseTuple(args,"O",&pysettings)) return NULL;
	settings=get_settings_from_python(pysettings);
	calibrate_manual(settings);
	get_settings_from_c(settings,pysettings);
	settings_free(&settings);
	Py_RETURN_NONE;
}

/* Module methods */
static struct PyMethodDef _input_methods[]=
{
	{"startup",input_startup,METH_VARARGS,"Runs startup code for the input module"},
	{"shutdown",input_shutdown,METH_VARARGS,"Runs shutdown code for the input module"},
	{"get_com",input_get_com,METH_VARARGS,"Returns the center of mass of the shadow"},
	{"get_verts",input_get_verts,METH_VARARGS,"Returns all vertices on the border of the shadow"},
	{"get_polys",input_get_polys,METH_VARARGS,"Returns a collection of polygons for the shadow"},
	{"get_lp_pts",input_get_lp_pts,METH_VARARGS,"Returns any detected laser pointer points"},
	{"calibrate",input_calibrate,METH_VARARGS,"Run manual or automatic calibration"},
	{NULL,NULL}
};

/* Module documentation */
static char _input_doc[]="Camera input processing module";

/* Module init function */
DL_EXPORT(void) init_input(void)
{
	PyObject *m;

	/* Init the _input module */
	m=Py_InitModule3("_input",_input_methods,_input_doc);
}
