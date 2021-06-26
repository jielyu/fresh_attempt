/*

Interface of DES encrypt/decrypt algorithm

Author: Jie Lyu
Email: jiejielyu@outlook.com

*/

#ifndef __DES__H__
#define __DES__H__

#include <iostream>
#include <vector>
#include <bitset>
#include "utils.h"

namespace crypt_impl
{

// interface for des encrypt/decrypt algorithm
class DES{

#define DES_KEY_LEN 64
#define DES_PLAIN_LEN DES_KEY_LEN
#define DES_REAL_KEY_LEN 56
#define DES_HALF_KEY_LEN DES_REAL_KEY_LEN/2
#define DES_SUBKEY_LEN 48
#define DES_HALF_TEXT_LEN DES_KEY_LEN/2

public:

    static void print_args_shape();
    // number of bits of plain
    static int block_size() {return DES_KEY_LEN;}

    DES()=default;
    DES(std::string key_word) {this->set_key(key_word);}

    int set_key(std::string key_word);

    // with bytes format
    std::vector<Byte> encrypt(std::vector<Byte> & plain) {
        CHECK_RAISE(plain.size() == (DES_PLAIN_LEN/8), "plain size not match with PLAIN_LEN");
        auto bits = _bytes_to_bitset(plain);
        auto cipher = _des_core(bits);
        return _bitset_to_bytes(cipher);
    }
    
    // with bytes format
    std::vector<Byte> decrypt(std::vector<Byte> & cipher) {
        CHECK_RAISE(cipher.size() == (DES_KEY_LEN/8), "cipher size not match with DES_KEY_LEN");
        auto bits = _bytes_to_bitset(cipher);
        auto plain = _des_core(bits, true);
        return _bitset_to_bytes(plain);
    }

    // encrypt by aes algorithm
    std::bitset<DES_PLAIN_LEN> encrypt(std::string text) {
        CHECK_RAISE(text.size() == (DES_PLAIN_LEN/8), "plain text length not match with PLAIN_LEN");
        std::bitset<DES_PLAIN_LEN> plain = _chars_to_bitset(text.data());
        return _des_core(plain);
    }

    // decrypt aes cipher
    std::string decrypt(std::bitset<DES_PLAIN_LEN> cipher) {
        std::bitset<DES_PLAIN_LEN> plain = _des_core(cipher, true);
        return _bitset_to_str(plain);
    }

private:
    std::string _key_word;                  // text-format key
    std::bitset<DES_KEY_LEN> _key;                   // binary key
    std::vector<std::bitset<DES_SUBKEY_LEN>> _subkeys;  // round subkeys
    
    // convert bytes to bitset
    std::bitset<DES_KEY_LEN> _bytes_to_bitset(std::vector<Byte> & bytes);
    // convert bitset to bytes
    std::vector<Byte> _bitset_to_bytes(std::bitset<DES_KEY_LEN> bits);

    // convert char array to bitset
    std::bitset<DES_KEY_LEN> _chars_to_bitset(const char * word, const int WORD_LEN = 8);
    // convert bit array to string
    std::string _bitset_to_str(std::bitset<DES_PLAIN_LEN> plain);

    // left shift round operation used in generating subkeys
    std::bitset<DES_HALF_KEY_LEN> _left_shift_round(std::bitset<DES_HALF_KEY_LEN> key, int shift);
    // generate subkey for each round
    int _gen_subkeys(std::bitset<DES_KEY_LEN> key, int round);
    // F function for each round
    std::bitset<DES_HALF_TEXT_LEN> F(std::bitset<DES_HALF_TEXT_LEN> r, std::bitset<DES_SUBKEY_LEN> subkey);
    // AES cryptology core algorithm flow
    std::bitset<DES_PLAIN_LEN> _des_core(std::bitset<DES_PLAIN_LEN> text, bool reverse=false);
    
    // for encrypting plain text
    static const std::vector<int> _IP;     // initial permutation
    static const std::vector<int> _IP_inv; // inverse initial permutation
    static const std::vector<int> _E;      // expansion permutation
    static const std::vector<int> _P;      // permutation function
    static const std::vector<std::vector<std::vector<int>>> _Sbox; // Substitution box
    // for sub-key generation
    static const std::vector<int> _PC_1;   // permuted choice one
    static const std::vector<int> _PC_2;   // permuted choice two
    static const std::vector<int> _bit_shift; // table of rotate-left shift bits
    static const int _Round;               // number of rounds

};   
    
} // namespace crypt_impl



#endif