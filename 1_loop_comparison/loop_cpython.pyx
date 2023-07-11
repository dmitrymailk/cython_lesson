from libc.stdio cimport printf

cpdef void big_loop_print(long long amount):
    cdef long long i
    for i in range(amount):
        printf("%lld\n", i)

cpdef long long big_loop_sum(long long amount):
    cdef long long total_sum = 0
    cdef long long i 

    for i in range(amount):
        total_sum += i

    return total_sum

