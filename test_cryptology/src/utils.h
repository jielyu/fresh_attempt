/*

Providing tools for cryptology implementation

Author: Jie Lyu
Email: jiejielyu@outlook.com

*/

#ifndef __UTILS_H__
#define __UTILS_H__

#include <vector>
#include <string>
#include <bitset>

namespace crypt_impl{

#define CHECK_RAISE(cond, info) \
if (!(cond)) {throw std::runtime_error(info);}

typedef std::bitset<8> Byte;
typedef std::bitset<32> Word;

// convert string to bytes
std::vector<Byte> str2bytes(const std::string text);
// convert bytes to string
std::string bytes2str(const std::vector<Byte> & bytes);
// convert bytes to word
Word bytes2word(Byte b1, Byte b2, Byte b3, Byte b4);

}

#endif