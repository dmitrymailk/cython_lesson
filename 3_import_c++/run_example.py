from rectangle_cpy import PyRectangle

if __name__ == "__main__":
    # https://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html
    rectangle = PyRectangle(1, 20, 3, 43)
    rectangle.print()
    print("Setting y1")
    rectangle.y1 = 12
    rectangle.print()
    rectangle.move(1, 4)
    rectangle.print()
