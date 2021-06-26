/*

Implementation of AES encrypt/decrypt algorithm

Author: Jie Lyu
Email: jiejielyu@outlook.com

*/

#include "aes.h"

#include <iostream>

using namespace std;

namespace crypt_impl{

const std::vector<std::vector<int>> AES::_Sbox = {
	{0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
	 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76},
	{0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 
	 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0},
	{0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 
	 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15},
	{0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 
	 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75},
	{0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 
	 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84},
	{0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 
	 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF},
	{0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 
	 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8},
	{0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 
	 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2},
	{0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 
	 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73},
	{0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 
	 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB},
	{0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 
	 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79},
	{0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 
	 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08},
	{0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 
	 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A},
	{0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 
	 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E},
	{0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 
	 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF},
	{0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 
	 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16}
};

const std::vector<std::vector<int>> AES::_Sbox_inv = {
	{0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 
	 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB},
	{0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 
	 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB},
	{0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 
	 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E},
	{0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 
	 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25},
	{0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 
	 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92},
	{0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 
	 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84},
	{0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 
	 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06},
	{0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 
	 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B},
	{0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 
	 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73},
	{0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 
	 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E},
	{0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 
	 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B},
	{0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 
	 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4},
	{0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 
	 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F},
	{0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 
	 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF},
	{0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 
	 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61},
	{0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 
	 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D}
};

const std::vector<unsigned int> AES::_Rcon = {
    0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 
	0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000};

void AES::print_args_shape() {
    cout << "Sbox.shape=(" << _Sbox.size() << "," << _Sbox[0].size() << ")" << endl;
    cout << "Rcon.shape=(" << _Rcon.size() << ")" << endl;
}

// set key for aes algorithm
void AES::set_key(std::string key_word) {
    CHECK_RAISE(key_word.size() == AES_KEY_LEN/8, "key word not match with AES_KEY_LEN");
    this->_key_word = key_word;
    this->_key = str2bytes(key_word);
    this->_subkeys = _expand_key(this->_key);
}

// encrypt binary data
std::vector<Byte> AES::encrypt(std::vector<Byte> & plain) {
    CHECK_RAISE(plain.size() == AES_KEY_LEN/8, "plain size not match with AES_KEY_LEN");
    _add_round_key(plain, this->_subkeys[0]);
    int num_rounds = this->_subkeys.size() - 1;
    for (int i = 1; i < num_rounds; ++i) {
        _sbox_bytes(plain);
        _shift_row(plain);
        _mix_cols(plain);
        _add_round_key(plain, this->_subkeys[i]);
    }
    _sbox_bytes(plain);
    _shift_row(plain);
    _add_round_key(plain, this->_subkeys[num_rounds]);
    return plain;
}

// decrypt to obtain binary plain data
std::vector<Byte> AES::decrypt(std::vector<Byte> & cipher) {
    CHECK_RAISE(cipher.size() == AES_KEY_LEN/8, "cipher size not match with AES_KEY_LEN");
    int num_rounds = this->_subkeys.size() - 1;
    _add_round_key(cipher, this->_subkeys[num_rounds]);
    for (int i = num_rounds-1; i > 0; --i) {
        _shift_row(cipher, true);
        _sbox_bytes(cipher, true);
        _add_round_key(cipher, this->_subkeys[i]);
        _mix_cols_inv(cipher);
    }
    _shift_row(cipher, true);
    _sbox_bytes(cipher, true);
    _add_round_key(cipher, this->_subkeys[0]);
    return cipher;
}

Word AES::_word_sbox(Word w) {
    Word sw;
    for (int i = 0; i < AES_WORD_BYTE_LEN; ++i) {
        int row = w[i*8+7]*8 + w[i*8+6]*4 + w[i*8+5]*2 + w[i*8+4];
        int col = w[i*8+3]*8 + w[i*8+2]*4 + w[i*8+1]*2 + w[i*8];
        Byte s_val = this->_Sbox[row][col];
        for (int j = 0; j < 8; ++j) {sw[i*8+j] = s_val[j];}
    }
    return sw;
}

Word AES::g(Word w, int round) {
    return _word_sbox(_word_rotate(w)) ^ Word(this->_Rcon[round]);
}

std::vector<std::vector<Word>> AES::_expand_key(const std::vector<Byte> & key) {
    // copy the original key as first key 
    int num_word = key.size() / 4;
    std::vector<Word> origin_keys;
    for (int i = 0; i < num_word; ++i) {
        origin_keys.push_back(bytes2word(key[i*4], key[i*4+1], key[i*4+2], key[i*4+3]));
    }
    int num_round = this->_Rcon.size();
    std::vector<std::vector<Word>> exp_keys;
    exp_keys.reserve(num_round+1);
    exp_keys.push_back(origin_keys);
    // generate key for each round
    for (int i = 0; i < num_round; ++i) {
        std::vector<Word> subkey;
        subkey.push_back(exp_keys[i][0] ^ g(exp_keys[i][3], i));
        for (int j = 1; j < 4; ++j) {
            subkey.push_back(exp_keys[i][j]^exp_keys[i][j-1]);
        }
        exp_keys.push_back(subkey);
    }
    return exp_keys;
}

std::vector<Byte> AES::_sbox_bytes(std::vector<Byte> & bytes, bool reverse) {
    for (int i = 0; i < bytes.size(); ++i) {
        int row = bytes[i][7]*8 + bytes[i][6]*4 + bytes[i][5]*2 + bytes[i][4]; 
        int col = bytes[i][3]*8 + bytes[i][2]*4 + bytes[i][1]*2 + bytes[i][0];
        bytes[i] = reverse ? this->_Sbox_inv[row][col] :this->_Sbox[row][col];
    }
    return bytes;
}

std::vector<Byte> AES::_shift_row(std::vector<Byte> & bytes, bool reverse) {
    CHECK_RAISE(bytes.size() == AES_KEY_LEN/8, "bytes size not match with AES_KEY_LEN");
    int num_rows = bytes.size() / AES_WORD_BYTE_LEN;
    for (int i = 1; i < num_rows; ++i) {
        int idx = i*AES_WORD_BYTE_LEN;
        Byte ori_bytes[AES_WORD_BYTE_LEN] = {bytes[idx], bytes[idx+1], bytes[idx+2], bytes[idx+3]};
        for (int j = 0; j < AES_WORD_BYTE_LEN; ++j) {
            int factor = reverse ? -1 : 1; // shift right or left 
            int ori_idx = (j - factor * i + i*AES_WORD_BYTE_LEN) % AES_WORD_BYTE_LEN;
            bytes[idx+j] = ori_bytes[ori_idx];
        }
    }
    return bytes;
}

Byte AES::_GF2_8(Byte b1, Byte b2) {
    Byte p = 0, h_bit;
    for (int i = 0; i < 8; ++i) {
        if ((b2 & Byte(0x01)) != 0) {p ^= b1;}
        h_bit = b1 & (Byte)0x80;
        b1 <<= 1;
        if (h_bit != 0) {b1 ^= 0x1b;}
        b2 >>= 1;
    }
    return p;
}

std::vector<Byte> AES::_mix_cols(std::vector<Byte> & bytes) {
    CHECK_RAISE(bytes.size() == AES_KEY_LEN/8, "bytes size not match with AES_KEY_LEN");
    Byte ori_bytes[AES_WORD_BYTE_LEN];
    int num_rows = bytes.size()/AES_WORD_BYTE_LEN;
    for (int c = 0; c < AES_WORD_BYTE_LEN; ++c) {
        for (int r = 0; r < num_rows; ++r) {
            ori_bytes[r] = bytes[r*AES_WORD_BYTE_LEN + c];
        }
        for (int r = 0; r < num_rows; ++r) {
            int hit_2 = r % AES_WORD_BYTE_LEN;
            int hit_3 = (r+1) % AES_WORD_BYTE_LEN;
            bytes[r*AES_WORD_BYTE_LEN + c] = 0;
            for (int k = 0; k < AES_WORD_BYTE_LEN; ++k) {
                Byte cur = ori_bytes[k];
                if (k == hit_2) {cur = _GF2_8(0x02, cur);}
                if (k == hit_3) {cur = _GF2_8(0x03, cur);}
                if (0 == k) {
                    bytes[r*AES_WORD_BYTE_LEN + c] |= cur;
                } else {
                    bytes[r*AES_WORD_BYTE_LEN + c] ^= cur;
                }
            }
        }
    }
    return bytes;
}

std::vector<Byte> AES::_mix_cols_inv(std::vector<Byte> & bytes) {
    CHECK_RAISE(bytes.size() == AES_KEY_LEN/8, "bytes size not match with AES_KEY_LEN");
    Byte ori_bytes[AES_WORD_BYTE_LEN];
    int num_rows = bytes.size()/AES_WORD_BYTE_LEN;
    Byte gf_const[AES_WORD_BYTE_LEN] = {0x0e, 0x0b, 0x0d, 0x09};
    for (int c = 0; c < AES_WORD_BYTE_LEN; ++c) {
        for (int r = 0; r < num_rows; ++r) {
            ori_bytes[r] = bytes[r*AES_WORD_BYTE_LEN + c];
        }
        for (int r = 0; r < num_rows; ++r) {
            bytes[r*AES_WORD_BYTE_LEN + c] = 0;
            for (int k = 0; k < AES_WORD_BYTE_LEN; ++k) {
                Byte cur = ori_bytes[k];
                int hit_idx = (k - r + r*AES_WORD_BYTE_LEN) % AES_WORD_BYTE_LEN;
                cur = _GF2_8(gf_const[hit_idx], cur);
                if (0 == k) {
                    bytes[r*AES_WORD_BYTE_LEN + c] |= cur;
                } else {
                    bytes[r*AES_WORD_BYTE_LEN + c] ^= cur;
                }
            }
        }
    }
    return bytes;
}

std::vector<Byte> AES::_add_round_key(std::vector<Byte> & bytes, const std::vector<Word> & key) {
    CHECK_RAISE(bytes.size() == AES_KEY_LEN/8, "bytes size not match with AES_KEY_LEN");
    CHECK_RAISE(key.size() == AES_WORD_BYTE_LEN, "key size not match with AES_WORD_BYTE_LEN");
    int num_rows = bytes.size() / AES_WORD_BYTE_LEN;
    for (int c = 0; c < AES_WORD_BYTE_LEN; ++c) {
        Word k[AES_WORD_BYTE_LEN] = {
            key[c] >> 24, (key[c] << 8) >> 24, (key[c] << 16) >> 24, (key[c] << 24) >> 24};
        for (int r = 0; r < num_rows; ++r) {
            bytes[r*AES_WORD_BYTE_LEN + c] ^= Byte(k[r].to_ulong());
        }
    }
    return bytes;
}

}