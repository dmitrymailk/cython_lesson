cmake_minimum_required(VERSION 3.8)

project(example)

# pip install "pybind11[global]"
# python -c "import pybind11; print(pybind11.__path__)"
set(pybind11 "/home/user-name-goes-here/.local/lib/python3.11/site-packages/pybind11/share/cmake/pybind11/")
find_package(pybind11 REQUIRED)

add_executable(example main.cpp)
target_link_libraries(example PRIVATE pybind11::embed)

add_custom_target(
    copy_file_after_build
    ALL
    COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/calc.py
        ${CMAKE_BINARY_DIR}/
    DEPENDS ${CMAKE_SOURCE_DIR}/calc.py  # Depend on the source file
)
