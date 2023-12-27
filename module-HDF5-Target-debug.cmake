# Avoid multiple calls to find_package to append duplicated properties to the targets
include_guard()########### VARIABLES #######################################################################
#############################################################################################
set(hdf5_FRAMEWORKS_FOUND_DEBUG "") # Will be filled later
conan_find_apple_frameworks(hdf5_FRAMEWORKS_FOUND_DEBUG "${hdf5_FRAMEWORKS_DEBUG}" "${hdf5_FRAMEWORK_DIRS_DEBUG}")

set(hdf5_LIBRARIES_TARGETS "") # Will be filled later


######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
if(NOT TARGET hdf5_DEPS_TARGET)
    add_library(hdf5_DEPS_TARGET INTERFACE IMPORTED)
endif()

set_property(TARGET hdf5_DEPS_TARGET
             PROPERTY INTERFACE_LINK_LIBRARIES
             $<$<CONFIG:Debug>:${hdf5_FRAMEWORKS_FOUND_DEBUG}>
             $<$<CONFIG:Debug>:${hdf5_SYSTEM_LIBS_DEBUG}>
             $<$<CONFIG:Debug>:ZLIB::ZLIB;hdf5::hdf5;hdf5::hdf5_cpp;hdf5::hdf5_hl>
             APPEND)

####### Find the libraries declared in cpp_info.libs, create an IMPORTED target for each one and link the
####### hdf5_DEPS_TARGET to all of them
conan_package_library_targets("${hdf5_LIBS_DEBUG}"    # libraries
                              "${hdf5_LIB_DIRS_DEBUG}" # package_libdir
                              "${hdf5_BIN_DIRS_DEBUG}" # package_bindir
                              "${hdf5_LIBRARY_TYPE_DEBUG}"
                              "${hdf5_IS_HOST_WINDOWS_DEBUG}"
                              hdf5_DEPS_TARGET
                              hdf5_LIBRARIES_TARGETS  # out_libraries_targets
                              "_DEBUG"
                              "hdf5"    # package_name
                              "${hdf5_NO_SONAME_MODE_DEBUG}")  # soname

# FIXME: What is the result of this for multi-config? All configs adding themselves to path?
set(CMAKE_MODULE_PATH ${hdf5_BUILD_DIRS_DEBUG} ${CMAKE_MODULE_PATH})

########## COMPONENTS TARGET PROPERTIES Debug ########################################

    ########## COMPONENT hdf5::hdf5_hl_cpp #############

        set(hdf5_hdf5_hdf5_hl_cpp_FRAMEWORKS_FOUND_DEBUG "")
        conan_find_apple_frameworks(hdf5_hdf5_hdf5_hl_cpp_FRAMEWORKS_FOUND_DEBUG "${hdf5_hdf5_hdf5_hl_cpp_FRAMEWORKS_DEBUG}" "${hdf5_hdf5_hdf5_hl_cpp_FRAMEWORK_DIRS_DEBUG}")

        set(hdf5_hdf5_hdf5_hl_cpp_LIBRARIES_TARGETS "")

        ######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
        if(NOT TARGET hdf5_hdf5_hdf5_hl_cpp_DEPS_TARGET)
            add_library(hdf5_hdf5_hdf5_hl_cpp_DEPS_TARGET INTERFACE IMPORTED)
        endif()

        set_property(TARGET hdf5_hdf5_hdf5_hl_cpp_DEPS_TARGET
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_FRAMEWORKS_FOUND_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_SYSTEM_LIBS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_DEPENDENCIES_DEBUG}>
                     APPEND)

        ####### Find the libraries declared in cpp_info.component["xxx"].libs,
        ####### create an IMPORTED target for each one and link the 'hdf5_hdf5_hdf5_hl_cpp_DEPS_TARGET' to all of them
        conan_package_library_targets("${hdf5_hdf5_hdf5_hl_cpp_LIBS_DEBUG}"
                              "${hdf5_hdf5_hdf5_hl_cpp_LIB_DIRS_DEBUG}"
                              "${hdf5_hdf5_hdf5_hl_cpp_BIN_DIRS_DEBUG}" # package_bindir
                              "${hdf5_hdf5_hdf5_hl_cpp_LIBRARY_TYPE_DEBUG}"
                              "${hdf5_hdf5_hdf5_hl_cpp_IS_HOST_WINDOWS_DEBUG}"
                              hdf5_hdf5_hdf5_hl_cpp_DEPS_TARGET
                              hdf5_hdf5_hdf5_hl_cpp_LIBRARIES_TARGETS
                              "_DEBUG"
                              "hdf5_hdf5_hdf5_hl_cpp"
                              "${hdf5_hdf5_hdf5_hl_cpp_NO_SONAME_MODE_DEBUG}")


        ########## TARGET PROPERTIES #####################################
        set_property(TARGET hdf5::hdf5_hl_cpp
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_OBJECTS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_LIBRARIES_TARGETS}>
                     APPEND)

        if("${hdf5_hdf5_hdf5_hl_cpp_LIBS_DEBUG}" STREQUAL "")
            # If the component is not declaring any "cpp_info.components['foo'].libs" the system, frameworks etc are not
            # linked to the imported targets and we need to do it to the global target
            set_property(TARGET hdf5::hdf5_hl_cpp
                         PROPERTY INTERFACE_LINK_LIBRARIES
                         hdf5_hdf5_hdf5_hl_cpp_DEPS_TARGET
                         APPEND)
        endif()

        set_property(TARGET hdf5::hdf5_hl_cpp PROPERTY INTERFACE_LINK_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_LINKER_FLAGS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl_cpp PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_INCLUDE_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl_cpp PROPERTY INTERFACE_LINK_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_LIB_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl_cpp PROPERTY INTERFACE_COMPILE_DEFINITIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_COMPILE_DEFINITIONS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl_cpp PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_cpp_COMPILE_OPTIONS_DEBUG}> APPEND)

    ########## COMPONENT hdf5::hdf5_hl #############

        set(hdf5_hdf5_hdf5_hl_FRAMEWORKS_FOUND_DEBUG "")
        conan_find_apple_frameworks(hdf5_hdf5_hdf5_hl_FRAMEWORKS_FOUND_DEBUG "${hdf5_hdf5_hdf5_hl_FRAMEWORKS_DEBUG}" "${hdf5_hdf5_hdf5_hl_FRAMEWORK_DIRS_DEBUG}")

        set(hdf5_hdf5_hdf5_hl_LIBRARIES_TARGETS "")

        ######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
        if(NOT TARGET hdf5_hdf5_hdf5_hl_DEPS_TARGET)
            add_library(hdf5_hdf5_hdf5_hl_DEPS_TARGET INTERFACE IMPORTED)
        endif()

        set_property(TARGET hdf5_hdf5_hdf5_hl_DEPS_TARGET
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_FRAMEWORKS_FOUND_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_SYSTEM_LIBS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_DEPENDENCIES_DEBUG}>
                     APPEND)

        ####### Find the libraries declared in cpp_info.component["xxx"].libs,
        ####### create an IMPORTED target for each one and link the 'hdf5_hdf5_hdf5_hl_DEPS_TARGET' to all of them
        conan_package_library_targets("${hdf5_hdf5_hdf5_hl_LIBS_DEBUG}"
                              "${hdf5_hdf5_hdf5_hl_LIB_DIRS_DEBUG}"
                              "${hdf5_hdf5_hdf5_hl_BIN_DIRS_DEBUG}" # package_bindir
                              "${hdf5_hdf5_hdf5_hl_LIBRARY_TYPE_DEBUG}"
                              "${hdf5_hdf5_hdf5_hl_IS_HOST_WINDOWS_DEBUG}"
                              hdf5_hdf5_hdf5_hl_DEPS_TARGET
                              hdf5_hdf5_hdf5_hl_LIBRARIES_TARGETS
                              "_DEBUG"
                              "hdf5_hdf5_hdf5_hl"
                              "${hdf5_hdf5_hdf5_hl_NO_SONAME_MODE_DEBUG}")


        ########## TARGET PROPERTIES #####################################
        set_property(TARGET hdf5::hdf5_hl
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_OBJECTS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_LIBRARIES_TARGETS}>
                     APPEND)

        if("${hdf5_hdf5_hdf5_hl_LIBS_DEBUG}" STREQUAL "")
            # If the component is not declaring any "cpp_info.components['foo'].libs" the system, frameworks etc are not
            # linked to the imported targets and we need to do it to the global target
            set_property(TARGET hdf5::hdf5_hl
                         PROPERTY INTERFACE_LINK_LIBRARIES
                         hdf5_hdf5_hdf5_hl_DEPS_TARGET
                         APPEND)
        endif()

        set_property(TARGET hdf5::hdf5_hl PROPERTY INTERFACE_LINK_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_LINKER_FLAGS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_INCLUDE_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl PROPERTY INTERFACE_LINK_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_LIB_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl PROPERTY INTERFACE_COMPILE_DEFINITIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_COMPILE_DEFINITIONS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_hl PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_hl_COMPILE_OPTIONS_DEBUG}> APPEND)

    ########## COMPONENT hdf5::hdf5_cpp #############

        set(hdf5_hdf5_hdf5_cpp_FRAMEWORKS_FOUND_DEBUG "")
        conan_find_apple_frameworks(hdf5_hdf5_hdf5_cpp_FRAMEWORKS_FOUND_DEBUG "${hdf5_hdf5_hdf5_cpp_FRAMEWORKS_DEBUG}" "${hdf5_hdf5_hdf5_cpp_FRAMEWORK_DIRS_DEBUG}")

        set(hdf5_hdf5_hdf5_cpp_LIBRARIES_TARGETS "")

        ######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
        if(NOT TARGET hdf5_hdf5_hdf5_cpp_DEPS_TARGET)
            add_library(hdf5_hdf5_hdf5_cpp_DEPS_TARGET INTERFACE IMPORTED)
        endif()

        set_property(TARGET hdf5_hdf5_hdf5_cpp_DEPS_TARGET
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_FRAMEWORKS_FOUND_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_SYSTEM_LIBS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_DEPENDENCIES_DEBUG}>
                     APPEND)

        ####### Find the libraries declared in cpp_info.component["xxx"].libs,
        ####### create an IMPORTED target for each one and link the 'hdf5_hdf5_hdf5_cpp_DEPS_TARGET' to all of them
        conan_package_library_targets("${hdf5_hdf5_hdf5_cpp_LIBS_DEBUG}"
                              "${hdf5_hdf5_hdf5_cpp_LIB_DIRS_DEBUG}"
                              "${hdf5_hdf5_hdf5_cpp_BIN_DIRS_DEBUG}" # package_bindir
                              "${hdf5_hdf5_hdf5_cpp_LIBRARY_TYPE_DEBUG}"
                              "${hdf5_hdf5_hdf5_cpp_IS_HOST_WINDOWS_DEBUG}"
                              hdf5_hdf5_hdf5_cpp_DEPS_TARGET
                              hdf5_hdf5_hdf5_cpp_LIBRARIES_TARGETS
                              "_DEBUG"
                              "hdf5_hdf5_hdf5_cpp"
                              "${hdf5_hdf5_hdf5_cpp_NO_SONAME_MODE_DEBUG}")


        ########## TARGET PROPERTIES #####################################
        set_property(TARGET hdf5::hdf5_cpp
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_OBJECTS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_LIBRARIES_TARGETS}>
                     APPEND)

        if("${hdf5_hdf5_hdf5_cpp_LIBS_DEBUG}" STREQUAL "")
            # If the component is not declaring any "cpp_info.components['foo'].libs" the system, frameworks etc are not
            # linked to the imported targets and we need to do it to the global target
            set_property(TARGET hdf5::hdf5_cpp
                         PROPERTY INTERFACE_LINK_LIBRARIES
                         hdf5_hdf5_hdf5_cpp_DEPS_TARGET
                         APPEND)
        endif()

        set_property(TARGET hdf5::hdf5_cpp PROPERTY INTERFACE_LINK_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_LINKER_FLAGS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_cpp PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_INCLUDE_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_cpp PROPERTY INTERFACE_LINK_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_LIB_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_cpp PROPERTY INTERFACE_COMPILE_DEFINITIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_COMPILE_DEFINITIONS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5_cpp PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_cpp_COMPILE_OPTIONS_DEBUG}> APPEND)

    ########## COMPONENT hdf5::hdf5 #############

        set(hdf5_hdf5_hdf5_FRAMEWORKS_FOUND_DEBUG "")
        conan_find_apple_frameworks(hdf5_hdf5_hdf5_FRAMEWORKS_FOUND_DEBUG "${hdf5_hdf5_hdf5_FRAMEWORKS_DEBUG}" "${hdf5_hdf5_hdf5_FRAMEWORK_DIRS_DEBUG}")

        set(hdf5_hdf5_hdf5_LIBRARIES_TARGETS "")

        ######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
        if(NOT TARGET hdf5_hdf5_hdf5_DEPS_TARGET)
            add_library(hdf5_hdf5_hdf5_DEPS_TARGET INTERFACE IMPORTED)
        endif()

        set_property(TARGET hdf5_hdf5_hdf5_DEPS_TARGET
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_FRAMEWORKS_FOUND_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_SYSTEM_LIBS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_DEPENDENCIES_DEBUG}>
                     APPEND)

        ####### Find the libraries declared in cpp_info.component["xxx"].libs,
        ####### create an IMPORTED target for each one and link the 'hdf5_hdf5_hdf5_DEPS_TARGET' to all of them
        conan_package_library_targets("${hdf5_hdf5_hdf5_LIBS_DEBUG}"
                              "${hdf5_hdf5_hdf5_LIB_DIRS_DEBUG}"
                              "${hdf5_hdf5_hdf5_BIN_DIRS_DEBUG}" # package_bindir
                              "${hdf5_hdf5_hdf5_LIBRARY_TYPE_DEBUG}"
                              "${hdf5_hdf5_hdf5_IS_HOST_WINDOWS_DEBUG}"
                              hdf5_hdf5_hdf5_DEPS_TARGET
                              hdf5_hdf5_hdf5_LIBRARIES_TARGETS
                              "_DEBUG"
                              "hdf5_hdf5_hdf5"
                              "${hdf5_hdf5_hdf5_NO_SONAME_MODE_DEBUG}")


        ########## TARGET PROPERTIES #####################################
        set_property(TARGET hdf5::hdf5
                     PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_OBJECTS_DEBUG}>
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_LIBRARIES_TARGETS}>
                     APPEND)

        if("${hdf5_hdf5_hdf5_LIBS_DEBUG}" STREQUAL "")
            # If the component is not declaring any "cpp_info.components['foo'].libs" the system, frameworks etc are not
            # linked to the imported targets and we need to do it to the global target
            set_property(TARGET hdf5::hdf5
                         PROPERTY INTERFACE_LINK_LIBRARIES
                         hdf5_hdf5_hdf5_DEPS_TARGET
                         APPEND)
        endif()

        set_property(TARGET hdf5::hdf5 PROPERTY INTERFACE_LINK_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_LINKER_FLAGS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5 PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_INCLUDE_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5 PROPERTY INTERFACE_LINK_DIRECTORIES
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_LIB_DIRS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5 PROPERTY INTERFACE_COMPILE_DEFINITIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_COMPILE_DEFINITIONS_DEBUG}> APPEND)
        set_property(TARGET hdf5::hdf5 PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Debug>:${hdf5_hdf5_hdf5_COMPILE_OPTIONS_DEBUG}> APPEND)

    ########## AGGREGATED GLOBAL TARGET WITH THE COMPONENTS #####################
    set_property(TARGET HDF5::HDF5 PROPERTY INTERFACE_LINK_LIBRARIES hdf5::hdf5_hl_cpp APPEND)
    set_property(TARGET HDF5::HDF5 PROPERTY INTERFACE_LINK_LIBRARIES hdf5::hdf5_hl APPEND)
    set_property(TARGET HDF5::HDF5 PROPERTY INTERFACE_LINK_LIBRARIES hdf5::hdf5_cpp APPEND)
    set_property(TARGET HDF5::HDF5 PROPERTY INTERFACE_LINK_LIBRARIES hdf5::hdf5 APPEND)

########## For the modules (FindXXX)
set(hdf5_LIBRARIES_DEBUG HDF5::HDF5)
