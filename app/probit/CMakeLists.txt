cmake_minimum_required(VERSION 3.22)
project(probit LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optimized build
add_compile_options(-O3)

# Header-only library
add_library(icn INTERFACE)
target_include_directories(icn INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src)

# API binary for web backend
add_executable(probit_api src/probit_api.cpp)
target_link_libraries(probit_api PRIVATE icn)
target_compile_definitions(probit_api PRIVATE ICN_ENABLE_HALLEY_REFINEMENT)
