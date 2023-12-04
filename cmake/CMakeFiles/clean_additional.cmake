# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\PyCode_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\PyCode_autogen.dir\\ParseCache.txt"
  "PyCode_autogen"
  )
endif()
