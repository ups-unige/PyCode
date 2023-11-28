cmake_minimum_required(VERSION 3.20)

# c++ and build settings
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_BUILD_TYPE "Debug")

# project name
cmake_path(GET CMAKE_CURRENT_SOURCE_DIR FILENAME ProjectName)   
string(REPLACE " " "_" PROJECT_NAME ${ProjectName})
project(${PROJECT_NAME} LANGUAGES CXX)
include("cmake/compiler.cmake")
include("cmake/utils.cmake")

include(FetchContent)

FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG        master
)

FetchContent_MakeAvailable(fmt)

set(SOURCES
  hdf5.cpp
  python.cpp
  main.cpp)
list(TRANSFORM SOURCES PREPEND "src/")

find_package(HDF5 REQUIRED COMPONENTS CXX REQUIRED)
find_package(Python COMPONENTS Interpreter REQUIRED Development REQUIRED)

add_executable(${PROJECT_NAME} ${SOURCES})
target_include_directories(${PROJECT_NAME} PRIVATE 
  "${CMAKE_SOURCE_DIR}/include" 
  ${HDF5_INCLUDE_DIRS}
  ${Python_INCLUDE_DIRS}
)
target_link_directories(${PROJECT_NAME} PRIVATE 
  ${HDF5_LIB_DIR}
)
target_link_libraries(${PROJECT_NAME} PRIVATE 
  all_warnings warnings_are_errors
  fmt::fmt
  ${HDF5_CXX_LIBRARY_NAMES}
  ${Python_LIBRARIES}
)
