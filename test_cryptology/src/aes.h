/*

Interface of AES encrypt/decrypt algorithm

Author: Jie Lyu
Email: jiejielyu@outlook.com

*/

#ifndef __AES_H__
#define __AES_H__

#include <iostream>
#include <vector>
#include <bitset>

#include "utils.h"

namespace crypt_impl
{

class AES {

#define AES_KEY_LEN 128
#define AES_WORD_BYTE_LEN 4       // 1 word consists of 4 bytes
#define AES_WORD_BIT_LEN 32

public:

    AES()=default;
    AES(std::string key_word) {set_key(key_word);}
    
    // print shape of args for aes algorithm
    static void print_args_shape();
    // number of bits of plain 
    static int block_size() {return AES_KEY_LEN;}

    // set key for aes algorithm
    void set_key(std::string key_word);
    
    // encrypt binary data
    std::vector<Byte> encrypt(std::vector<Byte> & plain);

    // decrypt to obtain binary plain data
    std::vector<Byte> decrypt(std::vector<Byte> & cipher);
    
    // encrypt text data
    std::vector<Byte> encrypt(std::string text) {
        auto plain = str2bytes(text);
        return encrypt(plain);
    }

    // decrypt to obtain text data
    std::string decrypt_text(std::vector<Byte> & cipher) {
        decrypt(cipher);
        return bytes2str(cipher);
    }

private:

    std::string _key_word;                    // text key word
    std::vector<Byte> _key;                   // binary key
    std::vector<std::vector<Word>> _subkeys;  // subkeys for each round
    
    // left shift word in loop
    Word _word_rotate(Word w) {return (w<<8) | (w>>24);}
    // word sbox substitution
    Word _word_sbox(Word w);
    // g fucntion for subkeys generation
    Word g(Word w, int round);
    // generate subkeys for each round
    std::vector<std::vector<Word>> _expand_key(const std::vector<Byte> & key);
    // bytes sbox substitution
    std::vector<Byte> _sbox_bytes(std::vector<Byte> & bytes, bool reverse=false);
    // shift in rows for bytes
    std::vector<Byte> _shift_row(std::vector<Byte> & bytes, bool reverse=false);
    // GF(2^8)
    Byte _GF2_8(Byte b1, Byte b2);
    // mix in cols
    std::vector<Byte> _mix_cols(std::vector<Byte> & bytes);
    // mix in cols for decrypt process
    std::vector<Byte> _mix_cols_inv(std::vector<Byte> & bytes);
    // xor operation using subkey in round
    std::vector<Byte> _add_round_key(std::vector<Byte> & bytes, const std::vector<Word> & key);

    // parameters of AES algorithm
    static const std::vector<std::vector<int>> _Sbox;     // Substitution boxes
    static const std::vector<std::vector<int>> _Sbox_inv; // inverse substitution
    static const std::vector<unsigned int> _Rcon;         // round constant

};
    
} // namespace crypt_impl


#endif
