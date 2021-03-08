aux_source_directory(. MY_MATH_SRC)
message(STATUS, "my_math_src: ${MY_MATH_SRC}")
add_library(my_math SHARED ${MY_MATH_SRC})