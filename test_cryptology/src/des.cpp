/*

Implementation of DES encrypt/decrypt algorithm

Author: Jie Lyu
Email: jiejielyu@outlook.com

*/

#include "des.h"
#include <iostream>
#include "utils.h"

using namespace std;

namespace crypt_impl
{

const std::vector<int> DES::_IP = {
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7};

const std::vector<int> DES::_IP_inv = {
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25};

const std::vector<int> DES::_E = {
    32,  1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1};

const std::vector<int> DES::_P = {
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25 };

const std::vector<std::vector<std::vector<int>>> DES::_Sbox = {
	{  
		{14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7},  
		{0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8},  
		{4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0}, 
		{15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13} 
	},
	{  
		{15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10},  
		{3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5}, 
		{0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15},  
		{13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9}  
	}, 
	{  
		{10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8},  
		{13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1},  
		{13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7},  
		{1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12}  
	}, 
	{  
		{7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15},  
		{13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9},  
		{10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4},  
		{3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14}  
	},
	{  
		{2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9},  
		{14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6},  
		{4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14},  
		{11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3}  
	},
	{  
		{12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11},  
		{10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8},  
		{9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6},  
		{4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13}  
	}, 
	{  
		{4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1},  
		{13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6},  
		{1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2},  
		{6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12}  
	}, 
	{  
		{13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7},  
		{1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2},  
		{7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8},  
		{2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11}  
	} 
};

const std::vector<int> DES::_PC_1 = {
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4};

const std::vector<int> DES::_PC_2 = {
    14, 17, 11, 24,  1,  5,
    3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32}; 

const std::vector<int> DES::_bit_shift = {
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};

const int DES::_Round = 16;

void DES::print_args_shape() {
    cout << "IP.shape=(" << _IP.size() << ")" << endl;
    cout << "IP_inv.shape=(" << _IP_inv.size() << ")" << endl;
    cout << "E.shape=(" << _E.size() << ")" << endl;
    cout << "P.shape=(" << _P.size() << ")" << endl;
    cout << "Sbox.shape=(" << _Sbox.size() 
        << "," << _Sbox[0].size() << "," << _Sbox[0][0].size() << ")" << endl;
    cout << "PC_1.shape=(" << _PC_1.size() << ")" << endl;
    cout << "PC_2.shape=(" << _PC_2.size() << ")" << endl;
    cout << "bit_shift.shape=(" << _bit_shift.size() << ")" << endl;
}

int DES::set_key(std::string key_word) {
    this->_key_word = key_word;
    this->_key = _chars_to_bitset(this->_key_word.c_str());
    _gen_subkeys(this->_key, this->_Round);
    return 0;
}

std::bitset<DES_KEY_LEN> DES::_bytes_to_bitset(std::vector<Byte> & bytes) {
    CHECK_RAISE(bytes.size() == DES_KEY_LEN/8, "word length not equal to DES_KEY_LEN");
    std::bitset<DES_KEY_LEN> bits;
    for (int i = 0; i < bytes.size(); ++i) {
        for (int j = 0; j < 8; ++j) {
            bits[i*8+j] = bytes[i][j];
        }
    }
    return bits;
}

std::vector<Byte> DES::_bitset_to_bytes(std::bitset<DES_KEY_LEN> bits) {
    std::vector<Byte> bytes;
    int num_bytes = DES_KEY_LEN / 8;
    for (int i = 0; i < num_bytes; ++i) {
        Byte b;
        for (int j = 0; j < 8; ++j) {
            b[j] = bits[i*8+j];
        }
        bytes.push_back(b);
    }
    return bytes;
}

std::bitset<DES_KEY_LEN> DES::_chars_to_bitset(const char * word, const int WORD_LEN) {
    const int NUM_BIT = 8;
    CHECK_RAISE(strlen(word) == WORD_LEN, "word length not equal to WORD_LEN");
    std::bitset<DES_KEY_LEN> bits;
    for (int i = 0; i < WORD_LEN; ++i) {
        for (int j = 0; j < NUM_BIT; ++j) {
            bits[i * NUM_BIT + j] = (word[i] >> j) & 0x01;
        }
    }
    return bits;
}

std::string DES::_bitset_to_str(std::bitset<DES_PLAIN_LEN> plain) {
    int num_chars = DES_PLAIN_LEN / 8;
    std::string text(num_chars, '\0');
    for (int i = 0; i < num_chars; ++i) {
        for (int j = 0; j < 8; ++j) {
            text[i] = plain[i*8+j] ? text[i] | (0x01 << j) : text[i] & (~(0x01 << j));
        }
    }
    return text;
}

std::bitset<DES_HALF_KEY_LEN> DES::_left_shift_round(std::bitset<DES_HALF_KEY_LEN> key, int shift) {
    std::bitset<DES_HALF_KEY_LEN> bak = key;
    for (int i = 0; i < DES_HALF_KEY_LEN; ++i) {
        if (i + shift >= DES_HALF_KEY_LEN) {
            key[i] = bak[i + shift - DES_HALF_KEY_LEN];
        } else {
            key[i] = bak[i+shift];
        }
    }
    return key;
}

int DES::_gen_subkeys(std::bitset<DES_KEY_LEN> key, int round) {
    // permutation
    CHECK_RAISE(this->_PC_1.size() == DES_REAL_KEY_LEN, "PC_1 not match REAL_KEY_LEN");
    std::bitset<DES_REAL_KEY_LEN> real_key;
    for (int i = 0; i < DES_REAL_KEY_LEN; ++i) {
        real_key[DES_REAL_KEY_LEN-1-i] = key[DES_KEY_LEN - this->_PC_1[i]];
    }
    // generate subkey for each round
    this->_subkeys.clear();
    std::bitset<DES_HALF_KEY_LEN> left, right;
    std::bitset<DES_SUBKEY_LEN> subkey;
    CHECK_RAISE(this->_PC_2.size() == DES_SUBKEY_LEN, "PC_2 not match DES_SUBKEY_LEN");
    for (int i = 0; i < round; ++i) {
        // split left and right parts
        for (int j = 0; j < DES_HALF_KEY_LEN; ++j) {
            right[j] = real_key[j];
            left[j] = real_key[j + DES_HALF_KEY_LEN];
        }
        // left shift
        left = _left_shift_round(left, this->_bit_shift[i]);
        right = _left_shift_round(right, this->_bit_shift[i]);
        // concat to generate new key
        for (int j = 0; j < DES_HALF_KEY_LEN; ++j) {
            real_key[j] = right[j];
            real_key[j + DES_HALF_KEY_LEN] = left[j];
        }
        // permutation
        for (int j = 0; j < DES_SUBKEY_LEN; ++j) {
            subkey[j] = real_key[DES_REAL_KEY_LEN - this->_PC_2[DES_SUBKEY_LEN-1 - j]];
        }
        this->_subkeys.push_back(subkey);
    }
    return 0;
}

std::bitset<DES_HALF_TEXT_LEN> DES::F(std::bitset<DES_HALF_TEXT_LEN> r, std::bitset<DES_SUBKEY_LEN> subkey) {
    // expand plain text
    std::bitset<DES_SUBKEY_LEN> ext_r;
    for (int i = 0; i < DES_SUBKEY_LEN; ++i) {
        ext_r[i] = r[DES_HALF_TEXT_LEN - this->_E[DES_SUBKEY_LEN - 1 - i]];
    }
    ext_r ^= subkey;
    // sbox subsititution
    std::bitset<DES_HALF_TEXT_LEN> sbox_r;
    for (int i = 0; i < DES_SUBKEY_LEN; i += 6) {
        int idx = DES_SUBKEY_LEN - 1 - i;
        int row = ext_r[idx] * 2 + ext_r[idx-5];
        int col = ext_r[idx-1]*8 + ext_r[idx-2]*4 + ext_r[idx-3]*2 + ext_r[idx-4];
        std::bitset<4> sbox_val(this->_Sbox[i/6][row][col]);
        int r_idx = (i/6) * 4;
        for (int j = 0; j < 4; ++j) {sbox_r[r_idx + j] = sbox_val[j];}
    }
    // permutation
    std::bitset<DES_HALF_TEXT_LEN> cipher;
    for (int i = 0; i < DES_HALF_TEXT_LEN; ++i) {
        cipher[DES_HALF_TEXT_LEN-1-i] = sbox_r[DES_HALF_TEXT_LEN - this->_P[i]];
    }
    return cipher;
}

std::bitset<DES_PLAIN_LEN> DES::_des_core(std::bitset<DES_PLAIN_LEN> text, bool reverse) {
    // initial permutation
    std::bitset<DES_PLAIN_LEN> ip_text;
    for (int i = 0; i < DES_PLAIN_LEN; ++i) {
        ip_text[DES_PLAIN_LEN - 1 - i] = text[DES_PLAIN_LEN - this->_IP[i]];
    }
    // split plain text into left and right parts
    std::bitset<DES_HALF_TEXT_LEN> left, right, left_bak;
    for (int i = 0; i < DES_HALF_TEXT_LEN; ++i) {
        left[i] = ip_text[i + DES_HALF_TEXT_LEN];
        right[i] = ip_text[i];
    }
    // encrypt plain text in rounds
    CHECK_RAISE(this->_subkeys.size() == this->_Round, "please set key at first")
    for (int i = 0; i < this->_Round; ++i) {
        left_bak = right;
        int subkey_idx = reverse ? this->_Round - 1 - i : i;
        auto f = F(right, this->_subkeys[subkey_idx]);
        right = left ^ f;
        left = left_bak;
    }
    // concat [right, left] after the last round 
    std::bitset<DES_PLAIN_LEN> cipher;
    for (int i = 0; i < DES_HALF_TEXT_LEN; ++i) {
        cipher[i] = left[i];
        cipher[i + DES_HALF_TEXT_LEN] = right[i];
    }
    // inverse initial permutation
    std::bitset<DES_PLAIN_LEN> cipher_bak = cipher;
    for (int i = 0; i < DES_PLAIN_LEN; ++i) {
        cipher[DES_PLAIN_LEN-1-i] = cipher_bak[DES_PLAIN_LEN-this->_IP_inv[i]];
    }
    return cipher;
}

} // namespace crypt_impl
