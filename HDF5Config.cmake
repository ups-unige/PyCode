########## MACROS ###########################################################################
#############################################################################################

# Requires CMake > 3.15
if(${CMAKE_VERSION} VERSION_LESS "3.15")
    message(FATAL_ERROR "The 'CMakeDeps' generator only works with CMake >= 3.15")
endif()

if(HDF5_FIND_QUIETLY)
    set(HDF5_MESSAGE_MODE VERBOSE)
else()
    set(HDF5_MESSAGE_MODE STATUS)
endif()

include(${CMAKE_CURRENT_LIST_DIR}/cmakedeps_macros.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/HDF5Targets.cmake)
include(CMakeFindDependencyMacro)

check_build_type_defined()

foreach(_DEPENDENCY ${hdf5_FIND_DEPENDENCY_NAMES} )
    # Check that we have not already called a find_package with the transitive dependency
    if(NOT ${_DEPENDENCY}_FOUND)
        find_dependency(${_DEPENDENCY} REQUIRED ${${_DEPENDENCY}_FIND_MODE})
    endif()
endforeach()

set(HDF5_VERSION_STRING "1.14.3")
set(HDF5_INCLUDE_DIRS ${hdf5_INCLUDE_DIRS_DEBUG} )
set(HDF5_INCLUDE_DIR ${hdf5_INCLUDE_DIRS_DEBUG} )
set(HDF5_LIBRARIES ${hdf5_LIBRARIES_DEBUG} )
set(HDF5_DEFINITIONS ${hdf5_DEFINITIONS_DEBUG} )

# Only the first installed configuration is included to avoid the collision
foreach(_BUILD_MODULE ${hdf5_BUILD_MODULES_PATHS_DEBUG} )
    message(${HDF5_MESSAGE_MODE} "Conan: Including build module from '${_BUILD_MODULE}'")
    include(${_BUILD_MODULE})
endforeach()


