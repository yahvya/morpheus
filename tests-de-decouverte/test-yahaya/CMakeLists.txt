cmake_minimum_required(VERSION 3.26)
project(test_opencv)

set(CMAKE_CXX_STANDARD 23)

find_package(OpenCV REQUIRED)

add_executable(${PROJECT_NAME} main.cpp
        OpenCvHelper.cpp
        OpenCvHelper.hpp
        CameraDistanceCalculator.cpp
        CameraDistanceCalculator.hpp
        Neuron.cpp
        Neuron.hpp
)

target_link_libraries(${PROJECT_NAME}
        ${OpenCV_LIBRARIES}
)

add_custom_command(
        TARGET ${PROJECT_NAME}
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/resources
        ${CMAKE_BINARY_DIR}/resources
)