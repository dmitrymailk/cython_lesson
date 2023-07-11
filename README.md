# Simple Lesson Cython

### Полезные ссылки

- https://www.peterbaumgartner.com/blog/intro-to-just-enough-cython-to-be-useful/

#### версия python

```bash
python -m venv env
```

```console
Python 3.9.0
```

#### создать окружение среды

```bash
python -m venv env
```

#### активировать среду (win 10)

```bash
.\env\Scripts\activate
```

#### установить все нужные пакеты

```bash
pip install -r requirements.txt
```

## 1. Сравнение циклов на python и cython

### 1.1 Simple python loop with print

```console
python .\loop_python.py
```

```python
import time


def big_loop():
    amount = 10**4 * 5
    start = time.time()

    for i in range(amount):
        print(i)

    now = time.time()
    total = now - start

    print(f"Total loop time = {total}")


if __name__ == "__main__":
    big_loop()


```

```console
Total loop time = 7.097778081893921
```

### 1.2 Simple cython loop with print

```python
# loop_cpython.pyx
from libc.stdio cimport printf

cpdef void big_loop_print(long long amount):
    cdef long long i
    for i in range(amount):
        printf("%lld\n", i)
```

```python
# loop_cpython_setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(name="loop_cpython", ext_modules=cythonize("./loop_cpython.pyx"))
```

#### сборка данного кода

```bash
python .\loop_cpython_setup.py build_ext --inplace --plat-name win-amd64
```

```console
running build_ext
building 'loop_cpython' extension
creating build
creating build\temp.win-amd64-3.9
creating build\temp.win-amd64-3.9\Release
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.31.31103\bin\HostX86\x64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -ID:\programming\concurrency\cython_lesson\env\include -IC:\Users\dimweb\.pyenv\pyenv-win\versions\3.9.0\include -IC:\Users\dimweb\.pyenv\pyenv-win\versions\3.9.0\include -IC:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.31.31103\ATLMFC\include -IC:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.31.31103\include -IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\include\um -IC:\Program Files (x86)\Windows Kits\10\include\10.0.19041.0\ucrt
-IC:\Program Files (x86)\Windows Kits\10\\include\10.0.19041.0\\shared -IC:\Program Files (x86)\Windows Kits\10\\include\10.0.19041.0\\um -IC:\Program Files (x86)\Windows Kits\10\\include\10.0.19041.0\\winrt -IC:\Program Files (x86)\Windows Kits\10\\include\10.0.19041.0\\cppwinrt /Tc./loop_cpython.c /Fobuild\temp.win-amd64-3.9\Release\./loop_cpython.obj
loop_cpython.c
./loop_cpython.c(1279): warning C4477: 'printf' : format string '%lld' requires an argument of type '__int64', but variadic argument 1 has type 'int'
./loop_cpython.c(1279): note: consider using '%d' in the format string
./loop_cpython.c(1279): note: consider using '%I32d' in the format string
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.31.31103\bin\HostX86\x64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:D:\programming\concurrency\cython_lesson\env\libs /LIBPATH:C:\Users\dimweb\.pyenv\pyenv-win\versions\3.9.0\libs /LIBPATH:C:\Users\dimweb\.pyenv\pyenv-win\versions\3.9.0 /LIBPATH:D:\programming\concurrency\cython_lesson\env\PCbuild\amd64 /LIBPATH:C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.31.31103\ATLMFC\lib\x64 /LIBPATH:C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.31.31103\lib\x64 /LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\lib\um\x64 /LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.19041.0\ucrt\x64 /LIBPATH:C:\Program Files (x86)\Windows Kits\10\\lib\10.0.19041.0\\um\x64 /EXPORT:PyInit_loop_cpython build\temp.win-amd64-3.9\Release\./loop_cpython.obj /OUT:D:\programming\concurrency\cython_lesson\1_loop_comparison\loop_cpython.cp39-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.9\Release\.\loop_cpython.cp39-win_amd64.lib
   Creating library build\temp.win-amd64-3.9\Release\.\loop_cpython.cp39-win_amd64.lib and object build\temp.win-amd64-3.9\Release\.\loop_cpython.cp39-win_amd64.exp
Generating code
Finished generating code
```

```python
# loop_cpython_wrapper.py
from loop_cpython import big_loop_print
import time

def loop_print():
    amount = 10**4 * 5
    start = time.time()
    big_loop_print(amount)
    now = time.time()
    total = now - start

    print(f"Total loop time = {total}")

if __name__ == "__main__":
    loop_print()

```

```bash
python .\loop_cpython_wrapper.py
```

```console
Total loop time = 6.410243034362793
```

Print function is really slow!

### 1.3 Simple python loop with sum

```python
import time

def big_loop_sum():
    amount = 10**8 * 5
    start = time.time()
    total_sum = 0

    for i in range(amount):
        total_sum += i

    now = time.time()
    total = now - start

    print(f"Total Sum = {total_sum} Total loop time = {total}")

if __name__ == "__main__":
    big_loop_sum()
```

```bash
python .\loop_python.py
```

```console
Total Sum = 124999999750000000 Total loop time = 13.623712062835693
```

### 1.4 Simple cython loop with sum

```python
# loop_cpython.pyx
cpdef long long big_loop_sum(long long amount):
    cdef long long total_sum = 0
    cdef long long i

    for i in range(amount):
        total_sum += i

    return total_sum
```

```python
# loop_cpython_setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(name="loop_cpython", ext_modules=cythonize("./loop_cpython.pyx"))
```

```bash
python .\loop_cpython_setup.py build_ext --inplace --plat-name win-amd64
```

```python
# loop_cpython_wrapper.py
from loop_cpython import  big_loop_sum
import time

def loop_sum():
    amount = 10**8 * 5
    start = time.time()
    total_sum = big_loop_sum(amount)
    now = time.time()
    total = now - start

    print(f"Total Sum = {total_sum} Total loop time = {total}")


if __name__ == "__main__":
    loop_sum()
```

```bash
python .\loop_cpython_wrapper.py
```

```console
Total Sum = 124999999750000000 Total loop time = 0.12099981307983398
```

Код сложения стал примерно в ~13.623712062835693/0.12099981307983398 = **112.59 раз быстрее**

## 2. Simple integration

- [определение интеграла](https://brilliant.org/wiki/definite-integrals/)
- [оригинальный туториал пандас](https://pandas.pydata.org/docs/user_guide/enhancingperf.html)

### 2.1 Python pandas integration

```python
import pandas as pd
import numpy as np
import time


def f(x):
    return x * (x - 1)


def integrate_f(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    result = s * dx
    return result


def simple_integration():
    amount = 10**4 * 2
    df = pd.DataFrame(
        {
            "a": -1 * np.abs(np.random.randn(amount)),
            "b": np.abs(np.random.randn(amount)),
            "N": np.random.randint(100, amount, (amount)),
            "x": np.float64,
        }
    )
    print(df.head(5))
    start = time.time()
    df["x"] = df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration()
```

```bash
python .\python_pandas.py
```

```console
         a         b      N                        x
0 -0.895617  0.116314  17235  <class 'numpy.float64'>
1 -1.146209  1.313681  12825  <class 'numpy.float64'>
2 -1.501192  1.131736   3999  <class 'numpy.float64'>
3 -1.123872  0.785894  19235  <class 'numpy.float64'>
4 -0.800014  0.222322  16083  <class 'numpy.float64'>
          a         b      N         x
0 -0.895617  0.116314  17235  0.634344
1 -1.146209  1.313681  12825  1.051875
2 -1.501192  1.131736   3999  2.098433
3 -1.123872  0.785894  19235  0.957836
4 -0.800014  0.222322  16083  0.469687
Total integration time = 22.239185571670532
```

### 2.2 Cython simple copy paste

```python
def f_plain(x):
    return x * (x - 1)

def integrate_f_plain(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f_plain(a + i * dx)
    return s * dx
```

```python
from distutils.core import setup
from Cython.Build import cythonize

setup(name="cython_pandas", ext_modules=cythonize("./cython_pandas.pyx"))
```

```bash
python .\cython_pandas_setup.py build_ext --inplace --plat-name win-amd64
```

```python
import pandas as pd
import numpy as np
import time
from cython_pandas import integrate_f_plain


def simple_integration():
    amount = 10**4 * 2
    df = pd.DataFrame(
        {
            "a": -1 * np.abs(np.random.randn(amount)),
            "b": np.abs(np.random.randn(amount)),
            "N": np.random.randint(100, amount, (amount)),
            "x": np.float64,
        }
    )
    print(df.head(5))
    start = time.time()
    df["x"] = df.apply(lambda x: integrate_f_plain(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration()

```

```bash
python .\cython_pandas_wrapper.py
```

```console
          a         b      N                        x
0 -0.351611  0.798271   8040  <class 'numpy.float64'>
1 -0.278288  1.861562   6194  <class 'numpy.float64'>
2 -0.155229  0.043896   5357  <class 'numpy.float64'>
3 -0.015697  0.648400   7157  <class 'numpy.float64'>
4 -0.728737  0.307716  18081  <class 'numpy.float64'>
          a         b      N         x
0 -0.351611  0.798271   8040 -0.072705
1 -0.278288  1.861562   6194  0.463344
2 -0.155229  0.043896   5357  0.012364
3 -0.015697  0.648400   7157 -0.119208
4 -0.728737  0.307716  18081  0.356940
Total integration time = 12.960063934326172
```

Мы просто скомпилировали код, а уже получили прирост почти в 2х раза!

### 2.3 Cython add datatypes

```python
cdef double f_typed(double x) except? -2:
    return x * (x - 1)

cpdef double integrate_f_typed(double a, double b, int N):
    cdef int i
    cdef double s, dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f_typed(a + i * dx)
    return s * dx
```

```bash
python .\cython_pandas_setup.py build_ext --inplace --plat-name win-amd64
```

```python
import pandas as pd
import numpy as np
import time
from cython_pandas import integrate_f_plain, integrate_f_typed


def simple_integration_typed():
    amount = 10**4 * 2
    df = pd.DataFrame(
        {
            "a": -1 * np.abs(np.random.randn(amount)),
            "b": np.abs(np.random.randn(amount)),
            "N": np.random.randint(100, amount, (amount)),
            "x": np.float64,
        }
    )
    print(df.head(5))
    start = time.time()
    df["x"] = df.apply(lambda x: integrate_f_typed(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration_typed()

```

```bash
python .\cython_pandas_wrapper.py
```

```console
          a         b      N                        x
0 -0.827819  0.130310  17336  <class 'numpy.float64'>
1 -0.223284  0.437670  12644  <class 'numpy.float64'>
2 -0.686149  0.260230  16746  <class 'numpy.float64'>
3 -1.703770  1.133487   9982  <class 'numpy.float64'>
4 -2.181895  0.943481  19789  <class 'numpy.float64'>
          a         b      N         x
0 -0.827819  0.130310  17336  0.524032
1 -0.223284  0.437670  12644 -0.039179
2 -0.686149  0.260230  16746  0.315133
3 -1.703770  1.133487   9982  2.943673
4 -2.181895  0.943481  19789  5.678181
Total integration time = 0.2722744941711426
```

По итогу у нас получилось ускорить изначальную функцию в 22.239185571670532 / 0.2722744941711426 = **в 81.6792833988 раз!**

И это еще далеко не предел.
