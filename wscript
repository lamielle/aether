import os

srcdir='.'
blddir='obj'

def set_options(opt):
	#Add config options for python
	opt.tool_options('python')

	opt.sub_options('src')

def configure(conf):
	#Configure python
	conf.check_tool('python')
	conf.check_python_version((2,4,2))

	conf.sub_config('src')

def build(bld):
	bld.add_subdirs('src')
