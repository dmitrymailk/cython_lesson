# Simple Lesson Cython

### Полезные ссылки

- https://www.peterbaumgartner.com/blog/intro-to-just-enough-cython-to-be-useful/
- https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html
- https://cython.readthedocs.io/en/latest/src/tutorial/strings.html

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

### 1.1 Простой цикл на python с print

Для начала запустим простой скрипт на питоне, который просто будет печатать числа в консоль. (надо же с чего-то начинать)

```console
python loop_python.py
```

```python
# 1_loop_comparison/loop_python.py
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

Довольно медлено для простого вывода в консоль. Теперь попробуем Cython.

### 1.2 Простой цикл на cython с print

Данная функция также просто печатает числа, получая размер цикла извне.

```python
# 1_loop_comparison/loop_cpython.pyx
from libc.stdio cimport printf

cpdef void big_loop_print(long long amount):
    cdef long long i
    for i in range(amount):
        printf("%lld\n", i)
```

Теперь чтобы собрать данный код, необходимо запустить следующий скрипт. На самом деле тоже самое можно сделать и через консоль, но мне удобнее держать все в python, так как его удобнее править.

```python
# 1_loop_comparison/setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(name="loop_cpython", ext_modules=cythonize("./loop_cpython.pyx"))
```

Чтобы собрать данный код необходимо выпонить следующую команду. Она должна скомпилировать нам бинарник и модуль на python, который мы сможем импртировать в обычном скрипте, при этом сам код будет быстрый как си.

```bash
python setup.py build_ext --inplace
```

```console
Compiling ./loop_cpython.pyx because it changed.
[1/1] Cythonizing ./loop_cpython.pyx
/home/kosenko/miniconda3/lib/python3.10/site-packages/Cython/Compiler/Main.py:381: FutureWarning: Cython directive 'language_level' not set, using '3str' for now (Py3). This has changed from earlier releases! File: /cephfs/home/kosenko/cython_lesson/1_loop_comparison/loop_cpython.pyx
  tree = Parsing.p_module(s, pxd, full_module_name)
```

Импортируем модуль **loop_cpython**, который мы скомпилировали ранее.

```python
# 1_loop_comparison/loop_cpython_wrapper.py
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

Запускаем получившуюся программу.

```bash
python loop_cpython_wrapper.py
```

```console
Total loop time = 6.410243034362793
```

Результат отличается не так сильно :(, получается я вас обманул и технология бесполезна? Нет, просто плохой пример, давайте еще раз.

### 1.3 Нахождение большой суммы на python

По настоящему cython начинает показывать себя в вычислительных задачах. Давайте снова попробуем что-то простое, найдем сумму.

```python
# 1_loop_comparison/loop_python.py
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
python loop_python.py
```

```console
Total Sum = 124999999750000000 Total loop time = 13.623712062835693
```

Довольно медленно, фильтры для CV на нем точно лучше не писать. Лучше доверим эту работу cython.

### 1.4 Нахождение большой суммы на cython

В данной функции я используют тип данных _long long_, чтобы уж наверняка число поместилось. А вот на python не пришлось бы париться о таких мелочах.

```python
# 1_loop_comparison/loop_cpython.pyx
cpdef long long big_loop_sum(long long amount):
    cdef long long total_sum = 0
    cdef long long i

    for i in range(amount):
        total_sum += i

    return total_sum
```

Уже знакомый код сборки.

```python
# 1_loop_comparison/setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(name="loop_cpython", ext_modules=cythonize("./loop_cpython.pyx"))
```

Выполняем команду сборки.

```bash
python setup.py build_ext --inplace
```

```python
# 1_loop_comparison/loop_cpython_wrapper.py
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

Запускаем сложные подсчеты...

```bash
python loop_cpython_wrapper.py
```

```console
Total Sum = 124999999750000000 Total loop time = 0.12099981307983398
```

Погодите, это реально?!

Код сложения стал примерно в ~13.623712062835693/0.12099981307983398 = **112.59 раз быстрее**

## 2. Простое интегрирование

- [определение интеграла](https://brilliant.org/wiki/definite-integrals/)
- [оригинальный туториал пандас](https://pandas.pydata.org/docs/user_guide/enhancingperf.html)

### 2.1 Интегрирование на pandas при помощи python

Да простят меня математики... Интегрирование это короче просто большое суммирование столбиков, а сам интеграл в самом простом понимании означает общую площадь данных столбиков, чем столбиков больше тем выше точность, тем больше вычислений нам требуется.

Довольно теории, переходим к практике!

```python
# 2_pandas_integration/python_pandas.py
import pandas as pd
import numpy as np
import time

# это функция, интеграл которой мы хотим найти
def f(x):
    return x * (x - 1)

# это функция интегрирования между двуся чиселками
# а - начало
# b - конец
# N - количество столбиков
# dx - ширина столбика, или если будет угодно шаг
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
            # генерация рандомных отрицательных чисел
            "a": -1 * np.abs(np.random.randn(amount)),
            # генерация рандомных положительных чисел
            "b": np.abs(np.random.randn(amount)),
            # генерация рандомной точности
            "N": np.random.randint(100, amount, (amount)),
            # это куда мы будем сохранять результат, так надо.
            "x": np.float64,
        }
    )
    print(df.head(5))
    start = time.time()
    # применяем функцию интегрирования для всего датасета
    df["x"] = df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration()
```

Запускаем научные вычисления, данной заумной командой.

```bash
python python_pandas.py
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

В результате мы получили результат интегрирования для рандомных чисел. Иными словами, мы просто так потратили энергию, вам должно быть стыдно.

### 2.2 Компиляция python кода в cython без каких либо изменений

Внимательный читатель может заметить, что я ничего не поменял, только названия функций, суть осталась та же.

```python
# 2_pandas_integration/cython_pandas.pyx
def f_plain(x):
    return x * (x - 1)

def integrate_f_plain(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f_plain(a + i * dx)
    return s * dx
```

Код сборки мало чем отличается, уже скучно...

```python
# 2_pandas_integration/cython_pandas.pyx
from distutils.core import setup
from Cython.Build import cythonize

setup(name="cython_pandas", ext_modules=cythonize("./cython_pandas.pyx"))
```

Запускаем сборку...

```bash
python setup.py build_ext --inplace
```

Напишем небольшой враппер для нашего модуля, чтобы мы могли его запустить.

```python
# 2_pandas_integration/cython_pandas_wrapper.py
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
    # код ничем не отличается от предыдущего, только теперь мы используем
    # функцию для вычисления, которая была скомпилирована на си
    df["x"] = df.apply(lambda x: integrate_f_plain(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration()

```

Запускаем...

```bash
python cython_pandas_wrapper.py
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

Мы просто скопировали и скомпилировали код, а уже получили **прирост в 2х раза**!

Заставляем задуматься. Но давайте пойдем дальше и ускорим наш код еще сильнее.

### 2.3 Добавляем в Cython типы данных

Ранее мы просто добавили python код в cython и скомпилировали его, но смысл Cython заключается не в этом.

```python
# 2_pandas_integration/cython_pandas.pyx

# добавляем типы из языка си, чтобы уже компилятор знал как оптимизировать данный код
# except? означает что cython помечает возникающую ошибку номером -2
# для данной функции мы ожидаем что получим double и вернем double
cdef double f_typed(double x) except? -2:
    return x * (x - 1)

# также как и для прошлой, объявляем типы из си
cpdef double integrate_f_typed(double a, double b, int N):
    cdef int i
    cdef double s, dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f_typed(a + i * dx)
    return s * dx
```

Собираем...

```bash
python setup.py build_ext --inplace
```

Код сборки почти не поменялся, только теперь все функции оказались типизированы.

```python
# 2_pandas_integration/cython_pandas_wrapper.py

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
python cython_pandas_wrapper.py
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

На этом моменте стоит остановится и честно признаться вам.. Я говорил правду, но не всю :) Да, Cython помогает ускорить код, но давайте будем благоразумны, даже для простой программы нам пришлось почти полностью переписать программу. А это даже не программа, она умещается на ладони, я говорю про реальные программы.

Так вот, для всяких вычислений(научных) **в 2023 году** используются другие подходы.

- [NumPy](https://numpy.org/) - это база, не знать что это позор.
- [Numba](https://numba.pydata.org/), она позволяет компилировать код и получать его почти таким же быстрым, но для этого достаточно одного декоратора н-жид, ну то есть **@njit**
- [taichi](https://www.taichi-lang.org/) - самый быстрый в мире компилятор для python, они написали все с нуля и заточили все для скорости. Думаю к ним долгое время ничего не сможет приблизиться, советую попробовать, если вдруг numpy вас чем-то не устроил.
