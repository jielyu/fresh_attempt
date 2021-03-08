aux_source_directory(. MY_STR_SRC)
message(STATUS, "my_str_src: ${MY_STR_SRC}")
add_library(my_str ${MY_STR_SRC})