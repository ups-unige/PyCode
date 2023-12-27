########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

list(APPEND hdf5_COMPONENT_NAMES hdf5::hdf5 hdf5::hdf5_cpp hdf5::hdf5_hl hdf5::hdf5_hl_cpp)
list(REMOVE_DUPLICATES hdf5_COMPONENT_NAMES)
list(APPEND hdf5_FIND_DEPENDENCY_NAMES ZLIB)
list(REMOVE_DUPLICATES hdf5_FIND_DEPENDENCY_NAMES)
set(ZLIB_FIND_MODE "NO_MODULE")

########### VARIABLES #######################################################################
#############################################################################################
set(hdf5_PACKAGE_FOLDER_DEBUG "C:/Users/leonardo/.conan2/p/b/hdf5e9175353bee83/p")
set(hdf5_BUILD_MODULES_PATHS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/lib/cmake/conan-official-hdf5-variables.cmake")


set(hdf5_INCLUDE_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/include"
			"${hdf5_PACKAGE_FOLDER_DEBUG}/include/hdf5")
set(hdf5_RES_DIRS_DEBUG )
set(hdf5_DEFINITIONS_DEBUG )
set(hdf5_SHARED_LINK_FLAGS_DEBUG )
set(hdf5_EXE_LINK_FLAGS_DEBUG )
set(hdf5_OBJECTS_DEBUG )
set(hdf5_COMPILE_DEFINITIONS_DEBUG )
set(hdf5_COMPILE_OPTIONS_C_DEBUG )
set(hdf5_COMPILE_OPTIONS_CXX_DEBUG )
set(hdf5_LIB_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/lib")
set(hdf5_BIN_DIRS_DEBUG )
set(hdf5_LIBRARY_TYPE_DEBUG STATIC)
set(hdf5_IS_HOST_WINDOWS_DEBUG 1)
set(hdf5_LIBS_DEBUG hdf5_hl_cpp_D hdf5_hl_D hdf5_cpp_D hdf5_D)
set(hdf5_SYSTEM_LIBS_DEBUG Shlwapi)
set(hdf5_FRAMEWORK_DIRS_DEBUG )
set(hdf5_FRAMEWORKS_DEBUG )
set(hdf5_BUILD_DIRS_DEBUG )
set(hdf5_NO_SONAME_MODE_DEBUG FALSE)


# COMPOUND VARIABLES
set(hdf5_COMPILE_OPTIONS_DEBUG
    "$<$<COMPILE_LANGUAGE:CXX>:${hdf5_COMPILE_OPTIONS_CXX_DEBUG}>"
    "$<$<COMPILE_LANGUAGE:C>:${hdf5_COMPILE_OPTIONS_C_DEBUG}>")
set(hdf5_LINKER_FLAGS_DEBUG
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${hdf5_SHARED_LINK_FLAGS_DEBUG}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${hdf5_SHARED_LINK_FLAGS_DEBUG}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${hdf5_EXE_LINK_FLAGS_DEBUG}>")


set(hdf5_COMPONENTS_DEBUG hdf5::hdf5 hdf5::hdf5_cpp hdf5::hdf5_hl hdf5::hdf5_hl_cpp)
########### COMPONENT hdf5::hdf5_hl_cpp VARIABLES ############################################

set(hdf5_hdf5_hdf5_hl_cpp_INCLUDE_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/include"
			"${hdf5_PACKAGE_FOLDER_DEBUG}/include/hdf5")
set(hdf5_hdf5_hdf5_hl_cpp_LIB_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/lib")
set(hdf5_hdf5_hdf5_hl_cpp_BIN_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_LIBRARY_TYPE_DEBUG STATIC)
set(hdf5_hdf5_hdf5_hl_cpp_IS_HOST_WINDOWS_DEBUG 1)
set(hdf5_hdf5_hdf5_hl_cpp_RES_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_OBJECTS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_COMPILE_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_COMPILE_OPTIONS_C_DEBUG "")
set(hdf5_hdf5_hdf5_hl_cpp_COMPILE_OPTIONS_CXX_DEBUG "")
set(hdf5_hdf5_hdf5_hl_cpp_LIBS_DEBUG hdf5_hl_cpp_D)
set(hdf5_hdf5_hdf5_hl_cpp_SYSTEM_LIBS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_FRAMEWORK_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_FRAMEWORKS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_DEPENDENCIES_DEBUG hdf5::hdf5 hdf5::hdf5_cpp hdf5::hdf5_hl)
set(hdf5_hdf5_hdf5_hl_cpp_SHARED_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_EXE_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_hl_cpp_NO_SONAME_MODE_DEBUG FALSE)

# COMPOUND VARIABLES
set(hdf5_hdf5_hdf5_hl_cpp_LINKER_FLAGS_DEBUG
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${hdf5_hdf5_hdf5_hl_cpp_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${hdf5_hdf5_hdf5_hl_cpp_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${hdf5_hdf5_hdf5_hl_cpp_EXE_LINK_FLAGS_DEBUG}>
)
set(hdf5_hdf5_hdf5_hl_cpp_COMPILE_OPTIONS_DEBUG
    "$<$<COMPILE_LANGUAGE:CXX>:${hdf5_hdf5_hdf5_hl_cpp_COMPILE_OPTIONS_CXX_DEBUG}>"
    "$<$<COMPILE_LANGUAGE:C>:${hdf5_hdf5_hdf5_hl_cpp_COMPILE_OPTIONS_C_DEBUG}>")
########### COMPONENT hdf5::hdf5_hl VARIABLES ############################################

set(hdf5_hdf5_hdf5_hl_INCLUDE_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/include"
			"${hdf5_PACKAGE_FOLDER_DEBUG}/include/hdf5")
set(hdf5_hdf5_hdf5_hl_LIB_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/lib")
set(hdf5_hdf5_hdf5_hl_BIN_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_hl_LIBRARY_TYPE_DEBUG STATIC)
set(hdf5_hdf5_hdf5_hl_IS_HOST_WINDOWS_DEBUG 1)
set(hdf5_hdf5_hdf5_hl_RES_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_hl_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_hl_OBJECTS_DEBUG )
set(hdf5_hdf5_hdf5_hl_COMPILE_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_hl_COMPILE_OPTIONS_C_DEBUG "")
set(hdf5_hdf5_hdf5_hl_COMPILE_OPTIONS_CXX_DEBUG "")
set(hdf5_hdf5_hdf5_hl_LIBS_DEBUG hdf5_hl_D)
set(hdf5_hdf5_hdf5_hl_SYSTEM_LIBS_DEBUG )
set(hdf5_hdf5_hdf5_hl_FRAMEWORK_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_hl_FRAMEWORKS_DEBUG )
set(hdf5_hdf5_hdf5_hl_DEPENDENCIES_DEBUG hdf5::hdf5)
set(hdf5_hdf5_hdf5_hl_SHARED_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_hl_EXE_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_hl_NO_SONAME_MODE_DEBUG FALSE)

# COMPOUND VARIABLES
set(hdf5_hdf5_hdf5_hl_LINKER_FLAGS_DEBUG
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${hdf5_hdf5_hdf5_hl_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${hdf5_hdf5_hdf5_hl_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${hdf5_hdf5_hdf5_hl_EXE_LINK_FLAGS_DEBUG}>
)
set(hdf5_hdf5_hdf5_hl_COMPILE_OPTIONS_DEBUG
    "$<$<COMPILE_LANGUAGE:CXX>:${hdf5_hdf5_hdf5_hl_COMPILE_OPTIONS_CXX_DEBUG}>"
    "$<$<COMPILE_LANGUAGE:C>:${hdf5_hdf5_hdf5_hl_COMPILE_OPTIONS_C_DEBUG}>")
########### COMPONENT hdf5::hdf5_cpp VARIABLES ############################################

set(hdf5_hdf5_hdf5_cpp_INCLUDE_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/include"
			"${hdf5_PACKAGE_FOLDER_DEBUG}/include/hdf5")
set(hdf5_hdf5_hdf5_cpp_LIB_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/lib")
set(hdf5_hdf5_hdf5_cpp_BIN_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_LIBRARY_TYPE_DEBUG STATIC)
set(hdf5_hdf5_hdf5_cpp_IS_HOST_WINDOWS_DEBUG 1)
set(hdf5_hdf5_hdf5_cpp_RES_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_OBJECTS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_COMPILE_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_COMPILE_OPTIONS_C_DEBUG "")
set(hdf5_hdf5_hdf5_cpp_COMPILE_OPTIONS_CXX_DEBUG "")
set(hdf5_hdf5_hdf5_cpp_LIBS_DEBUG hdf5_cpp_D)
set(hdf5_hdf5_hdf5_cpp_SYSTEM_LIBS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_FRAMEWORK_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_FRAMEWORKS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_DEPENDENCIES_DEBUG hdf5::hdf5)
set(hdf5_hdf5_hdf5_cpp_SHARED_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_EXE_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_cpp_NO_SONAME_MODE_DEBUG FALSE)

# COMPOUND VARIABLES
set(hdf5_hdf5_hdf5_cpp_LINKER_FLAGS_DEBUG
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${hdf5_hdf5_hdf5_cpp_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${hdf5_hdf5_hdf5_cpp_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${hdf5_hdf5_hdf5_cpp_EXE_LINK_FLAGS_DEBUG}>
)
set(hdf5_hdf5_hdf5_cpp_COMPILE_OPTIONS_DEBUG
    "$<$<COMPILE_LANGUAGE:CXX>:${hdf5_hdf5_hdf5_cpp_COMPILE_OPTIONS_CXX_DEBUG}>"
    "$<$<COMPILE_LANGUAGE:C>:${hdf5_hdf5_hdf5_cpp_COMPILE_OPTIONS_C_DEBUG}>")
########### COMPONENT hdf5::hdf5 VARIABLES ############################################

set(hdf5_hdf5_hdf5_INCLUDE_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/include"
			"${hdf5_PACKAGE_FOLDER_DEBUG}/include/hdf5"
			"${hdf5_PACKAGE_FOLDER_DEBUG}/include/hdf5")
set(hdf5_hdf5_hdf5_LIB_DIRS_DEBUG "${hdf5_PACKAGE_FOLDER_DEBUG}/lib")
set(hdf5_hdf5_hdf5_BIN_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_LIBRARY_TYPE_DEBUG STATIC)
set(hdf5_hdf5_hdf5_IS_HOST_WINDOWS_DEBUG 1)
set(hdf5_hdf5_hdf5_RES_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_OBJECTS_DEBUG )
set(hdf5_hdf5_hdf5_COMPILE_DEFINITIONS_DEBUG )
set(hdf5_hdf5_hdf5_COMPILE_OPTIONS_C_DEBUG "")
set(hdf5_hdf5_hdf5_COMPILE_OPTIONS_CXX_DEBUG "")
set(hdf5_hdf5_hdf5_LIBS_DEBUG hdf5_D)
set(hdf5_hdf5_hdf5_SYSTEM_LIBS_DEBUG Shlwapi)
set(hdf5_hdf5_hdf5_FRAMEWORK_DIRS_DEBUG )
set(hdf5_hdf5_hdf5_FRAMEWORKS_DEBUG )
set(hdf5_hdf5_hdf5_DEPENDENCIES_DEBUG ZLIB::ZLIB)
set(hdf5_hdf5_hdf5_SHARED_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_EXE_LINK_FLAGS_DEBUG )
set(hdf5_hdf5_hdf5_NO_SONAME_MODE_DEBUG FALSE)

# COMPOUND VARIABLES
set(hdf5_hdf5_hdf5_LINKER_FLAGS_DEBUG
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${hdf5_hdf5_hdf5_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${hdf5_hdf5_hdf5_SHARED_LINK_FLAGS_DEBUG}>
        $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${hdf5_hdf5_hdf5_EXE_LINK_FLAGS_DEBUG}>
)
set(hdf5_hdf5_hdf5_COMPILE_OPTIONS_DEBUG
    "$<$<COMPILE_LANGUAGE:CXX>:${hdf5_hdf5_hdf5_COMPILE_OPTIONS_CXX_DEBUG}>"
    "$<$<COMPILE_LANGUAGE:C>:${hdf5_hdf5_hdf5_COMPILE_OPTIONS_C_DEBUG}>")