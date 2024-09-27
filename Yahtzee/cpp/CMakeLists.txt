cmake_minimum_required(VERSION 3.12)
project(Yahtzee)
enable_testing()

add_executable(yahtzee yahtzee.cpp yahtzee.hpp yahtzee.tests.cpp)
add_test(NAME yahtzee COMMAND yahtzee)
