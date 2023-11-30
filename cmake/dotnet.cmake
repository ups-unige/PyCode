# template of a CLR project with cmake

cmake_minimum_required(VERSION 3.20)
project(clr_test LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(${PROJECT_NAME}
  "src/main.cpp"
)

# Set project /clr flags
target_compile_options(${PROJECT_NAME} PRIVATE /clr)
target_compile_options(${PROJECT_NAME} PRIVATE /fp:precise)

# Define the metadata directories as variables
set(MetadataDir1 "${CMAKE_SOURCE_DIR}/lib")
# Add the metadata directories to the compiler search path
target_compile_options(${PROJECT_NAME} PRIVATE
                       $<$<BOOL:${MSVC}>:/AI${MetadataDir1}>)

set_property(TARGET ${PROJECT_NAME} PROPERTY VS_GLOBAL_ROOTNAMESPACE ${PROJECT_NAME})
set_property(TARGET ${PROJECT_NAME} PROPERTY VS_GLOBAL_KEYWORD "ManagedCProj")
set_property(TARGET ${PROJECT_NAME} PROPERTY VS_GLOBAL_CLRSupport "true")
set_property(TARGET ${PROJECT_NAME} PROPERTY VS_DOTNET_TARGET_FRAMEWORK_VERSION "v4.7")
set_property(TARGET ${PROJECT_NAME} PROPERTY VS_DOTNET_REFERENCES "System" "System.Data")

# Note: Modification of compiler flags is required for CLR compatibility now that we are using .resx files.
string(REPLACE "/EHsc" "" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
string(REPLACE "/RTC1" "" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
