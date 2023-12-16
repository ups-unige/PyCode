cmake_minimum_required(VERSION 3.20)

# c++ and build settings
set(CMAKE_CXX_STANDARD 20)
# set(CMAKE_BUILD_TYPE "Debug")

# project name
cmake_path(GET CMAKE_CURRENT_SOURCE_DIR FILENAME ProjectName)
string(REPLACE " " "_" PROJECT_NAME ${ProjectName})
project(
  ${PROJECT_NAME}
  VERSION 0.0.1
  LANGUAGES CXX)
include("cmake/compiler.cmake")
include("cmake/utils.cmake")

include(FetchContent)

FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG 10.1.1)

FetchContent_GetProperties(fmt)

if(NOT fmt_POPULATED)
  FetchContent_Populate(fmt)
  add_subdirectory(${fmt_SOURCE_DIR} ${fmt_BINARY_DIR})
endif()

FetchContent_MakeAvailable(fmt)

# ##############################################################################
# CodePP

set(SOURCES
    "src/codepp/hdf5/h5utils.cpp" "include/codepp/hdf5/h5utils.hpp"
    "src/codepp/hdf5/h5analog.cpp" "include/codepp/hdf5/h5analog.hpp"
    "src/codepp/hdf5/h5content.cpp" "include/codepp/hdf5/h5content.hpp")

# list(TRANSFORM SOURCES PREPEND "src/codepp/")

find_package(
  HDF5 CONFIG REQUIRED
  COMPONENTS CXX
  REQUIRED)
if(NOT HDF5_FOUND)
  message(FATAL_ERROR "HDF5 library is necessary to build CodePP")
else()

endif()

# find_package(
#   Python
#   COMPONENTS Interpreter
#   REQUIRED Development REQUIRED)
# if(NOT Python_FOUND)
#   message(FATAL_ERROR "Python library is necessary to build CodePP")
# endif()

add_library(${PROJECT_NAME}Lib ${SOURCES})

target_include_directories(
  ${PROJECT_NAME}Lib PRIVATE "${CMAKE_SOURCE_DIR}/include"
                             "${HDF5_INCLUDE_DIRS}" ${Python_INCLUDE_DIRS})

target_link_libraries(
  ${PROJECT_NAME}Lib PRIVATE all_warnings warnings_are_errors fmt::fmt
                             ${HDF5_LIBRARIES} ${Python_LIBRARIES})

# ##############################################################################
# GUI

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(GUI_SOURCES main.cpp)

list(TRANSFORM GUI_SOURCES PREPEND "src/")
find_package(
  QT
  REQUIRED
  HINTS
  $ENV{Qt6_ROOT}
  NAMES
  Qt6
  Qt5
  REQUIRED
  COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
  qt_add_executable(${PROJECT_NAME} MANUAL_FINALIZATION ${GUI_SOURCES})

  target_include_directories(${PROJECT_NAME}
                             PRIVATE "${CMAKE_SOURCE_DIR}/include")

  target_link_libraries(
    ${PROJECT_NAME} PRIVATE all_warnings warnings_are_errors fmt::fmt
                            ${PROJECT_NAME}Lib Qt${QT_VERSION_MAJOR}::Widgets)
else()
  message(FATAL_ERROR "Qt6 or greater version required")
endif()

set_target_properties(
  ${PROJECT_NAME}
  PROPERTIES MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
             MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
             MACOSX_BUNDLE_SHORT_VERSION_STRING
             ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
             MACOSX_BUNDLE TRUE
             # WIN32_EXECUTABLE TRUE
)

install(
  TARGETS ${PROJECT_NAME}
  BUNDLE DESTINATION .
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

if(QT_VERSION_MAJOR EQUAL 6)
  qt_finalize_executable(${PROJECT_NAME})
endif()
