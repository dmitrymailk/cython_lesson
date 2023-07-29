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

### 3. Использования кода на Си в Python

Но понятно что не на только научных вычислениях сошелся мир. Хотя я, честно, долго думал зачем же нужен cython в текущих реалиях. Для себя я нашел только лишь один ответ - написание оберток для c и c++. Cython это клей! Прошу к столу.

Разберем честно украденный пример из официальной документации.

- https://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html
-

В данном примере мы напишем класс прямоугольника на си, а затем воспользуемся некоторыми методами на python.

Сначала код на с++, питонисты только не пугайтесь.

```cpp
// 3_import_c++/Rectangle.h
#ifndef RECTANGLE_H
#define RECTANGLE_H

namespace shapes
{
	class Rectangle
	{
	public:
		int x0, y0, x1, y1;
        // nullable constructor
		Rectangle();
        // basic constructor
		Rectangle(int x0, int y0, int x1, int y1);
		// dummy deconstructor
        ~Rectangle();
		void move(int dx, int dy);
		void print();
	};
}

#endif
```

```cpp
// 3_import_c++/Rectangle.cpp

#include <iostream>
#include "Rectangle.h"

namespace shapes
{

	// Default constructor
	Rectangle::Rectangle() {}

	// Overloaded constructor
	Rectangle::Rectangle(int x0, int y0, int x1, int y1)
	{
		this->x0 = x0;
		this->y0 = y0;
		this->x1 = x1;
		this->y1 = y1;
	}

	// Destructor
	Rectangle::~Rectangle()
	{
		printf("Object deconstruction....\n");
	}

	// Move the rectangle by dx dy
	void Rectangle::move(int dx, int dy)
	{
		printf("Moving...\n");
		this->x0 += dx;
		this->y0 += dy;
		this->x1 += dx;
		this->y1 += dy;
	}

    // функция печати, добавил для наглядности, что мы можем что-то печатать из си кода
	void Rectangle::print()
	{
		printf("x0=%d y0=%d x1=%d y1=%d\n", this->x0, this->y0, this->x1, this->y1);
	}
}
```

Ну что сказать. Простейший класс на с++, который содержит в себе какую-то логику работы с прямоугольником. Теперь попробуем импортировать это в python.

```python
# 3_import_c++/rectangle_cpy.pyx
# distutils: language = c++ <---- данная строчка должна быть в начале файла, только так компилятор поймет что ему нужно работать с с++ кодом

# данная строчка говорит компилятору cython чтобы он нашел данный файл
# и скомпилировал его. Это нужно чтобы мы потом могли вызвать необходимую нам функцию, описанную в данном файле.
cdef extern from "Rectangle.cpp":
    pass


# объявляем еще раз класс, только на cython
# это необходимо чтобы он потом смог найти и сопоставить нужные нам поля.
# согласен некоторый бойлерплейт получается, но кажется это довольно небольшая цена
cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        int x0, y0, x1, y1
        Rectangle() except +
        Rectangle(int, int, int, int) except +
        void move(int, int)
        void print()

# До этого мы работали исключительно с классами на с++, чтобы python нас вообще понял
# нужно создать еще одну обертку(да, как-то многовато уже)
# данная обертка, к примеру, может вынести только нужные нам поля и функции
cdef class PyRectangle:
    cdef Rectangle *c_rect

    # согласно документации __cinit__ это единственное надежное место, где мы
    # можем объвлять переменные ссылочного типа
    def __cinit__(self):
        self.c_rect = new Rectangle()

    # а вот это уже специальный деконструктор, который управляет памятью
    # именно он определяет как уничтожится объект и очиститься память
    def __dealloc__(self):
        del self.c_rect

    def __init__(self, int x0, int y0, int x1, int y1):
        self.c_rect.x0 = x0
        self.c_rect.y0 = y0
        self.c_rect.x1 = x1
        self.c_rect.y1 = y1

    # простые обертки
    def print(self):
        self.c_rect.print()

    def move(self, dx, dy):
        self.c_rect.move(dx, dy)

    # Attribute access
    @property
    def x0(self):
        return self.c_rect.x0
    @x0.setter
    def x0(self, x0):
        self.c_rect.x0 = x0

    # Attribute access
    @property
    def x1(self):
        return self.c_rect.x1
    @x1.setter
    def x1(self, x1):
        self.c_rect.x1 = x1

    # Attribute access
    @property
    def y0(self):
        return self.c_rect.y0
    @y0.setter
    def y0(self, y0):
        self.c_rect.y0 = y0

    # Attribute access
    @property
    def y1(self):
        return self.c_rect.y1
    @y1.setter
    def y1(self, y1):
        self.c_rect.y1 = y1
```

Компилируем...

```bash
python setup.py build_ext --inplace
```

Функция управления данным кодом.

```python
# 3_import_c++/run_example.py
from rectangle_cpy import PyRectangle

if __name__ == "__main__":
    rectangle = PyRectangle(1, 20, 3, 43)
    rectangle.print()
    print("Setting y1")
    rectangle.y1 = 12
    rectangle.print()
    rectangle.move(1, 4)
    rectangle.print()

```

```bash
python run_example.py
```

```console
x0=1 y0=20 x1=3 y1=43
Setting y1
x0=1 y0=20 x1=3 y1=12
Moving...
x0=2 y0=24 x1=4 y1=16
Object deconstruction....
```

Ценность данного примера в том, что мы теперь можем писать всякую крутую фигню на с++, а затем элегантно импортировать ее в python.

Но довольно академических сферических коней в вакууме. Давайте применим cython по назначению!

### 4. Запуск llama2.c от karpathy на cython.

Представим ситуацию. Перед вами черный ящик. Вы не понимаете его структуру, вы не знаете что это такое. Известно лишь одно, чем сильнее вы бъете по этому ящику, тем больше денег из него вываливается. В какой-то момент вам надоело подставлять ладони и захотелось как-то выстроить инфраструкту вокруг этого полезного артефакта.

Так вот это как си бинарники выглядят для питонистов.

В данном случае мы имеем маленькую языковую модель, которая генерирует нам какой-то текст. Данная реализация включает в себя просто вывод чего-то в консоль, а мы хотим как-то перехватить данный текст, может быть даже как-то модифицировать.

Приступим.

Чтобы посмотреть как работает оригинальная модель выполним следующую команду. кто не на linux, соболезную.

```bash
make run
```

```bash
./run stories15M.bin
```

```console
<s>
Once upon a time, there was a little girl named Lily. She loved to play with her toys and eat cookies. One day, she went to the park to play with her friends. While she was playing, she saw a woman who looked very wealthy. She asked her mom what that meant, and her mom explained that the woman was wearing a nice coat.
Lily was curious, and asked if she could go say hello. She waved at the woman and said hello. The woman smiled and said hi back, and Lily was so happy. They played together for a while and had fun.
Suddenly, the woman's cat jumped on Lily's shoulder and surprised her. Lily laughed and laughed, and the woman laughed too. They became friends and played together all day. From that day on, Lily loved visiting people with big smiles and enthusiasm.
<s>
One day, a little girl named Amy went to her wardrobe to find her favorite dress. She opened the wardrobe and saw many things she had never seen before. She saw a shirt, a sock, and a toy. Amy felt very fine because she was having so much fun
achieved tok/s: 65.891473
```

Великолепно, оно генерирует текст. Но мы ничего не можем сделать с этим текстом. Давайте обернем код и посмотрим что будет.

Сначала просто запустим данную программу из python.

Для этого объявим несколько функций.

```c
#ifndef LLAMA2_H
#define LLAMA2_H
// просто вызывает оригинальный код
void generate_1(char *checkpoint);
#endif
```

```c
// 4_import_llama/llama_c.c
/**
 * ДОФИГА УМНОГО КОДА ВЫШЕ
*/

void generate_1(char *checkpoint)
{
    // дефолтная функция генерации без изменений, только мы передаем туда название файла чекпоинта
    basic_generation_1(checkpoint);
}
```

Теперь как-то впихнем написанное в наш cython.

```python
# 4_import_llama/llama_cy.pyx

cdef extern from "llama_c.h":
	void generate_1(char* checkpoint)

def llama_generate_1(checkpoint: str = 'model.bin'):
	# передаем из обычного питона строку
    # затем кодируем ее в байты
	c_name = checkpoint.encode('utf-8')
    # создаем переменную ссылочного типа
	cdef char* c_checkpoint = c_name
    # и наконец вызываем нужную функцию генерации
	generate_1(c_checkpoint)
```

Собираем...

```python
# 4_import_llama/setup.py
from setuptools import setup

from Cython.Build import cythonize
from distutils.extension import Extension

extensions = [Extension("llama_cy", ["llama_cy.pyx", "llama_c.c"])]
setup(
    ext_modules=extensions,
    extra_compile_args=["-O3"],
)

```

```bash
python setup.py build_ext --inplace
```

Теперь для запуска нашей нейронки воспользуемся кодом на python.

```python
# 4_import_llama/run_llama.py
from llama_cy import llama_generate_1

if __name__ == "__main__":
    llama_generate_1("stories15M.bin")
```

На выходе мы получили обертку над си кодом, который можем запускать сколько нашей душе угодно. Но зачем...

Теперь попробуем получить чуть больше полезной нагрузки от данной черной коробки.

Для этого нам придется немного переписать наш код на си (о ужас). Сразу глубоко извиняюсь перед сишниками, так как ничего более сложного чем little c на этом языке я не разбирал и не кодил.

Так вот, по факту нам нужно создать массив строк, затем вычленить токен из генерации, добавить в массив ну и собственно вернуть данную ссылку на этот массив.

Так уж и быть теперь я приведу полный листинг функции.

```c
// 4_import_llama/llama_c.c

char *basic_generation_2(char *checkpoint)
{

    // poor man's C argparse
    // char *checkpoint = NULL;  // e.g. out/model.bin
    float temperature = 0.9f; // e.g. 1.0, or 0.0
    int steps = 256;          // max number of steps to run for, 0: use seq_len
    char *prompt = NULL;      // prompt string

    // ОБЪЯВЛЯЕМ МАССИВ МАССИВОВ
    // ----------
    char **generation_result = (char **)malloc(sizeof(char *) * steps);
    // ----------

    // 'checkpoint' is necessary arg
    if (!checkpoint)
    {
        printf("You should provide some checkpoint\n");
        return 1;
    }

    // seed rng with time. if you want deterministic behavior use temperature 0.0
    rng_seed = (unsigned int)time(NULL);

    // read in the model.bin file
    Config config;
    TransformerWeights weights;
    int fd = 0;         // file descriptor for memory mapping
    float *data = NULL; // memory mapped data pointer
    long file_size;     // size of the checkpoint file in bytes
    {
        FILE *file = fopen(checkpoint, "rb");
        if (!file)
        {
            printf("Couldn't open file %s\n", checkpoint);
            return 1;
        }
        // read in the config header
        if (fread(&config, sizeof(Config), 1, file) != 1)
        {
            return 1;
        }
        // negative vocab size is hacky way of signaling unshared weights. bit yikes.
        int shared_weights = config.vocab_size > 0 ? 1 : 0;
        config.vocab_size = abs(config.vocab_size);
        // figure out the file size
        fseek(file, 0, SEEK_END); // move file pointer to end of file
        file_size = ftell(file);  // get the file size, in bytes
        fclose(file);
        // memory map the Transformer weights into the data pointer
        fd = open(checkpoint, O_RDONLY); // open in read only mode
        if (fd == -1)
        {
            printf("open failed!\n");
            return 1;
        }
        data = mmap(NULL, file_size, PROT_READ, MAP_PRIVATE, fd, 0);
        if (data == MAP_FAILED)
        {
            printf("mmap failed!\n");
            return 1;
        }
        float *weights_ptr = data + sizeof(Config) / sizeof(float);
        checkpoint_init_weights(&weights, &config, weights_ptr, shared_weights);
    }
    // right now we cannot run for more than config.seq_len steps
    if (steps <= 0 || steps > config.seq_len)
    {
        steps = config.seq_len;
    }

    // read in the tokenizer.bin file
    char **vocab = (char **)malloc(config.vocab_size * sizeof(char *));
    float *vocab_scores = (float *)malloc(config.vocab_size * sizeof(float));
    unsigned int max_token_length;
    {
        FILE *file = fopen("tokenizer.bin", "rb");
        if (!file)
        {
            printf("couldn't load tokenizer.bin\n");
            return 1;
        }
        if (fread(&max_token_length, sizeof(int), 1, file) != 1)
        {
            printf("failed read\n");
            return 1;
        }
        int len;
        for (int i = 0; i < config.vocab_size; i++)
        {
            if (fread(vocab_scores + i, sizeof(float), 1, file) != 1)
            {
                printf("failed read\n");
                return 1;
            }
            if (fread(&len, sizeof(int), 1, file) != 1)
            {
                printf("failed read\n");
                return 1;
            }
            vocab[i] = (char *)malloc(len + 1);
            if (fread(vocab[i], len, 1, file) != 1)
            {
                printf("failed read\n");
                return 1;
            }
            vocab[i][len] = '\0'; // add the string terminating token
        }
        fclose(file);
    }

    // create and init the application RunState
    RunState state;
    malloc_run_state(&state, &config);

    // process the prompt, if any
    int *prompt_tokens = NULL;
    int num_prompt_tokens = 0;
    if (prompt != NULL)
    {
        prompt_tokens = (int *)malloc(config.seq_len * sizeof(int));
        bpe_encode(prompt, vocab, vocab_scores, config.vocab_size, max_token_length, prompt_tokens, &num_prompt_tokens);
    }

    // start the main loop
    long start = 0; // used to time our code, only initialized after first iteration
    int next;       // will store the next token in the sequence
    int token = 1;  // init with token 1 (=BOS), as done in Llama-2 sentencepiece tokenizer
    int pos = 0;    // position in the sequence
    // printf("<s>\n"); // explicit print the initial BOS token for stylistic symmetry reasons
    while (pos < steps)
    {

        // forward the transformer to get logits for the next token
        transformer(token, pos, &config, &state, &weights);

        if (pos < num_prompt_tokens)
        {
            // if we are still processing the input prompt, force the next prompt token
            next = prompt_tokens[pos];
        }
        else
        {
            // sample the next token
            if (temperature == 0.0f)
            {
                // greedy argmax sampling: take the token with the highest probability
                next = argmax(state.logits, config.vocab_size);
            }
            else
            {
                // apply the temperature to the logits
                for (int q = 0; q < config.vocab_size; q++)
                {
                    state.logits[q] /= temperature;
                }
                // apply softmax to the logits to get the probabilities for next token
                softmax(state.logits, config.vocab_size);
                // we sample from this distribution to get the next token
                next = sample(state.logits, config.vocab_size);
            }
        }

        // following BOS token (1), sentencepiece decoder strips any leading whitespace (see PR #89)
        char *token_str = (token == 1 && vocab[next][0] == ' ') ? vocab[next] + 1 : vocab[next];
        // СОХРАНЯЕМ СГЕНЕРИРОВАННЫЙ ТОКЕН
        // -------------
        generation_result[pos] = token_str;
        // -------------

        // advance forward
        token = next;
        pos++;
        // init our timer here because the first iteration is slow due to memmap
        if (start == 0)
        {
            start = time_in_ms();
        }
    }

    // report achieved tok/s
    long end = time_in_ms();
    // printf("\nachieved tok/s: %f\n", (steps - 1) / (double)(end - start) * 1000);

    // ПОЛУЧАЕМ КОНЕЧНУЮ СТРОКУ ГЕНЕРАЦИИ
    char *result = malloc(sizeof(char) * 3000);
    for (int i = 0; i < steps; i++)
    {
        strcat(result, generation_result[i]);
    }

    // memory and file handles cleanup
    free_run_state(&state);
    for (int i = 0; i < config.vocab_size; i++)
    {
        free(vocab[i]);
    }
    free(vocab);
    free(vocab_scores);
    if (prompt_tokens != NULL)
        free(prompt_tokens);
    if (data != MAP_FAILED)
        munmap(data, file_size);
    if (fd != -1)
        close(fd);

    // ВОЗВРАЩАЕМ РЕЗУЛЬТАТ, НЕВЕРОЯТНОООООО
    return result;
}

char *generate_2(char *checkpoint)
{
    char *generation_result = (char *)basic_generation_2(checkpoint);
    return generation_result;
}

```

Обновляем файл с заголовками.

```c
#ifndef LLAMA2_H
#define LLAMA2_H

void generate_1(char *checkpoint);
char* generate_2(char *checkpoint);

#endif
```

Обновляем файл с вызовом генерации.

```python
# 4_import_llama/llama_cy.pyx
cdef extern from "llama_c.h":
	void generate_1(char* checkpoint)
	char* generate_2(char* checkpoint)

def llama_generate_2(checkpoint: str = 'model.bin'):
	# pass checkpoint name to our c code and get result
	c_name = checkpoint.encode('utf-8')
	cdef char* c_checkpoint = c_name
	cdef char* generation_result = generate_2(c_checkpoint)
	result = generation_result.decode('unicode_escape')
	print(result)
```

Собираем ...

```bash
python setup.py build_ext --inplace
```

```python
# 4_import_llama/run_llama.py
from llama_cy import llama_generate_2

if __name__ == "__main__":
    llama_generate_2("stories15M.bin")
```

По итогу мы получили текст из си, на python.

```console
°Ó`\ÚOnce upon a time, there was a big, red motor. It liked to run and play in the park. The motor was very slow, but it was a happy motor.
One day, the motor saw a little boy. The boy wanted to play with the motor, but it didn't move. The motor tried to explain, "The boy needs to walk, and try again." The boy was scared to walk, but the motor said, "It's okay, we can play together."
So the boy walked with the motor. They had fun running and playing in the park. But then, something unexpected happened. The motor started to slow down! The boy looked around and saw that the motor was not in a funny way anymore.
They were both scared, but then they saw a big, friendly bear. The bear surprised them and they laughed. The boy forgot he was scared of the motor now. From that day on, the boy, the motor, and the bear became best friends. They played together in the park every day, and the boy never thought the motor could be so much fun.
<s>
Once upon a time, there was a little boy named Timmy. He loved to play with his toy cars
```

Был ли более простой способ? Ну типа был. Можно было вызвать в фоне программу и получить ее output. Просто хотелось показать более менее реальный пример связки программы на си и python.

Спасибо за внимание. Меня можно найти тут [канал телеграм](https://t.me/larva_coder)
