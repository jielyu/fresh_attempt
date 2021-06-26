#ifndef __OPERATION_MODE_H__
#define __OPERATION_MODE_H__

#include <vector>
#include <string>
#include "utils.h"
#include "des.h"
#include "aes.h"

namespace crypt_impl
{

template<typename T_cipher>
class OperationMode {
protected:
    
public:
    T_cipher _crypto;

    int block_size() {return _crypto.block_size();}

    void fill_bytes(std::vector<Byte> & bytes) {
        CHECK_RAISE(bytes.size() > 0, "not allow to process empty data");
        int block_bytes = block_size() / 8;
        if (bytes.size() % block_bytes != 0) {
            int num_comp = block_bytes - (bytes.size() % block_bytes);
            for (int i = 0; i < num_comp; ++i) {bytes.push_back(Byte(0));}
        }
    }

    std::vector<Byte> get_IV() {
        static std::vector<Byte> iv = {
            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 
            0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
            0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x15, 0x17,
            0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f};
        int num_bytes = OperationMode<T_cipher>::block_size() / 8;
        CHECK_RAISE(iv.size() >= num_bytes, "iv is too short");
        return std::vector<Byte>(iv.begin(), iv.begin() + num_bytes);
    }
};

template<typename T_cipher>
class ECB : public OperationMode<T_cipher> {

public:

    ECB()=default;
    ECB(std::string key_word) {OperationMode<T_cipher>::_crypto.set_key(key_word);}

    std::vector<Byte> encrypt(std::vector<Byte> & plain) {
        int block_bytes = OperationMode<T_cipher>::block_size() / 8;
        OperationMode<T_cipher>::fill_bytes(plain);
        int num_block = plain.size() / block_bytes;
        std::vector<Byte> cipher;
        cipher.reserve(plain.size());
        for (int i = 0; i < num_block; ++i) {
            std::vector<Byte> bytes(plain.begin() + i*block_bytes, plain.begin() + (i+1)*block_bytes);
            auto cipher_block = OperationMode<T_cipher>::_crypto.encrypt(bytes);
            cipher.insert(cipher.end(), cipher_block.begin(), cipher_block.end());
        }
        return cipher;
    }

    std::vector<Byte> decrypt(std::vector<Byte> & cipher) {
        int block_bytes = OperationMode<T_cipher>::block_size() / 8;
        CHECK_RAISE((cipher.size()) % block_bytes == 0, "cipher size not match with KEY_LEN");
        std::vector<Byte> plain;
        plain.reserve(cipher.size());
        int num_block = cipher.size() / block_bytes;
        for (int i = 0; i < num_block; ++i) {
            std::vector<Byte> bytes(cipher.begin() + i*block_bytes, cipher.begin() + (i+1)*block_bytes);
            auto plain_block = OperationMode<T_cipher>::_crypto.decrypt(bytes);
            plain.insert(plain.end(), plain_block.begin(), plain_block.end());
        }
        return plain;
    }
};


template<typename T_cipher>
class OFB : public OperationMode<T_cipher> {

public:
    OFB()=default;
    OFB(std::string key_word) {OperationMode<T_cipher>::_crypto.set_key(key_word);}

    std::vector<Byte> encrypt(std::vector<Byte> & plain) {
        // fill bytes to ensure byte alignment
        int block_bytes = OperationMode<T_cipher>::block_size() / 8;
        OperationMode<T_cipher>::fill_bytes(plain);
        // OFB operation mode
        int num_block = plain.size() / block_bytes;
        auto iv = OperationMode<T_cipher>::get_IV();
        std::vector<Byte> cipher;
        cipher.reserve(plain.size());
        for (int i = 0; i < num_block; ++i) {
            // encrypt iv
            iv = OperationMode<T_cipher>::_crypto.encrypt(iv);
            for (int j = 0; j < block_bytes; ++j) {
                plain[i*block_bytes+j] ^= iv[j];
            }
        }
        return plain;
    }

    std:: vector<Byte> decrypt(std::vector<Byte> & cipher) {
        int block_bytes = OperationMode<T_cipher>::block_size() / 8;
        CHECK_RAISE((cipher.size()) % block_bytes == 0, "cipher size not match with KEY_LEN");
        int num_block = cipher.size() / block_bytes;
        auto iv = OperationMode<T_cipher>::get_IV();
        for (int i = 0; i < num_block; ++i) {
            iv = OperationMode<T_cipher>::_crypto.encrypt(iv);
            for (int j = 0; j < block_bytes; ++j) {
                cipher[i*block_bytes+j] ^= iv[j];
            }
        }
        return cipher;
    }
};


template<typename T_cipher>
class CBC : public OperationMode<T_cipher> {

public:
    CBC()=default;
    CBC(std::string key_word) {OperationMode<T_cipher>::_crypto.set_key(key_word);}

    std::vector<Byte> encrypt(std::vector<Byte> & plain) {
        // fill bytes to ensure byte alignment
        int block_bytes = OperationMode<T_cipher>::block_size() / 8;
        OperationMode<T_cipher>::fill_bytes(plain);
        // OFB operation mode
        int num_block = plain.size() / block_bytes;
        auto iv = OperationMode<T_cipher>::get_IV();
        std::vector<Byte> cipher;
        cipher.reserve(plain.size());
        for (int i = 0; i < num_block; ++i) {
            for (int j = 0; j < block_bytes; ++j) {plain[i*block_bytes+j] ^= iv[j];}
            std::vector<Byte> bytes(plain.begin() + i*block_bytes, plain.begin() + (i+1)*block_bytes);
            iv = OperationMode<T_cipher>::_crypto.encrypt(bytes);
            cipher.insert(cipher.end(), iv.begin(), iv.end());
        }
        return cipher;
    }

    std:: vector<Byte> decrypt(std::vector<Byte> & cipher) {
        int block_bytes = OperationMode<T_cipher>::block_size() / 8;
        CHECK_RAISE((cipher.size()) % block_bytes == 0, "cipher size not match with KEY_LEN");
        int num_block = cipher.size() / block_bytes;
        auto iv = OperationMode<T_cipher>::get_IV();
        std::vector<Byte> plain;
        plain.reserve(cipher.size());
        for (int i = 0; i < num_block; ++i) {
            std::vector<Byte> bytes(cipher.begin() + i*block_bytes, cipher.begin() + (i+1)*block_bytes);
            auto plain_block = OperationMode<T_cipher>::_crypto.decrypt(bytes);
            for (int j = 0; j < block_bytes; ++j) {plain_block[j] ^= iv[j];}
            plain.insert(plain.end(), plain_block.begin(), plain_block.end());
            iv = std::vector<Byte>(cipher.begin() + i*block_bytes, cipher.begin() + (i+1)*block_bytes);
        }
        return plain;
    }
};
    
} // namespace crypt_impl

#endif
