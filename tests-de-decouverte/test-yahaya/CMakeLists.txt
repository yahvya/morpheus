cmake_minimum_required(VERSION 3.26)
project(test_opencv)

set(CMAKE_CXX_STANDARD 23)
set(DST_DIR "cmake-build-debug-visual-studio")
set(MODEL_LIST "frontal-face.xml" "profile-face.xml" "smile.xml")

find_package(OpenCV REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME}
        ${OpenCV_LIBRARIES}
)

# ligne de copie que je ne sais pas trop pourquoi cause un soucis de version
#file(COPY_FILE "model.xml" "${DST_DIR}/model.xml")

foreach (file ${MODEL_LIST})
    file(COPY_FILE "${file}" "${DST_DIR}/${file}")
endforeach ()