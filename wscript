import os

srcdir='.'
blddir='obj'

def set_options(opt):
	#Add config options for the c compiler
	opt.tool_options('compiler_cc')

	#Add config options for python
	opt.tool_options('python')

	opt.sub_options('src')

def configure(conf):
	#Configure the c compiler
	conf.check_tool('compiler_cc')

	#Configure python
	conf.check_tool('python')
	conf.check_python_version((2,4,2))
	conf.check_python_headers()

	conf.sub_config('src')

def build(bld):
	bld.add_subdirs('src')
