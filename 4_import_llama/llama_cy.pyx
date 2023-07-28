from libc.stdlib cimport malloc
from libc.string cimport strcpy, strlen

cdef extern from "llama_c.h":
	void generate_1(char* checkpoint)

def llama_generate_1():
	cdef char* filename = 'stories15M.bin'
	cdef Py_ssize_t filename_len = strlen(filename)
	cdef char* checkpoint = <char *> malloc((filename_len + 1) * sizeof(char))
	strcpy(checkpoint, filename)
	generate_1(checkpoint)