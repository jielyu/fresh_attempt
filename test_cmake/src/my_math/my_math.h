#ifndef __MY_MATH_H__
#define __MY_MATH_H__

#ifdef BUILD_XXX_DLL 
#define IO_XXX_DLL __declspec(dllexport) 
#else 
#define IO_XXX_DLL __declspec(dllimport) 
#endif

int IO_XXX_DLL my_add(int a, int b);

#endif
