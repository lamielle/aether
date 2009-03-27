import os

srcdir='.'
blddir='obj'

def set_options(opt):
	#Add config options for python
	opt.tool_options('python')

	opt.sub_options('src')
	opt.sub_options('bin')
	opt.sub_options('data')

def configure(conf):
	#Configure python
	conf.check_tool('python')
	conf.check_python_version((2,4,2))
	conf.check_python_module('yaml')

	conf.sub_config('src')
	conf.sub_config('bin')
	conf.sub_config('data')

def build(bld):
	bld.add_subdirs('src')
	bld.add_subdirs('data')
