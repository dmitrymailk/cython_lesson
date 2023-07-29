from libc.stdlib cimport malloc
from libc.string cimport strcpy, strlen

cdef extern from "llama_c.h":
	void generate_1(char* checkpoint)
	char* generate_2(char* checkpoint)

def llama_generate_1():
	# https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html
	# simple call from python
	cdef char* checkpoint = 'stories15M.bin'
	generate_1(checkpoint)

def llama_generate_2(checkpoint: str = 'model.bin'):
	# pass checkpoint name to our c code
	c_name = checkpoint.encode('utf-8')
	cdef char* c_checkpoint = c_name
	generate_1(c_checkpoint)

def llama_generate_3(checkpoint: str = 'model.bin'):
	# pass checkpoint name to our c code and get result
	c_name = checkpoint.encode('utf-8')
	cdef char* c_checkpoint = c_name
	cdef char* generation_result = generate_2(c_checkpoint)
	result = generation_result.decode('unicode_escape')
	print(result)