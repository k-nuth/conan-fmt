cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

# include(conanbuildinfo.cmake)
# conan_basic_setup()

message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")
message( STATUS "****************************************")

# Conan infrastructure.
#==============================================================================

message( STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
message( STATUS "CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}")

if(EXISTS ${CMAKE_SOURCE_DIR}/ci_utils/cmake/knuthbuildinfo.cmake)
    include(${CMAKE_SOURCE_DIR}/ci_utils/cmake/knuthbuildinfo.cmake)
else()
    message( STATUS "knuthbuildinfo does not exists")
endif()


add_subdirectory("source_subfolder")
