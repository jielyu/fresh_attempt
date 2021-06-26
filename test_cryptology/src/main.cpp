#include <iostream>

#include "des.h"
#include "aes.h"
#include "operation_mode.hpp"

using namespace std;
using namespace crypt_impl;

void demo_des() {
    std::cout << "------------- DES Encrypt/Decrypt Demo --------------" << std::endl;
    //DES::print_args_shape();
    DES des("12345678");
    std::vector<std::string> testcase = {
        "abcdefgh", "bbcdefgh", "accdefgh", "abddefgh", "abceefgh",
        "abcdffgh", "abcdeggh", "abcdefhh", "abcdefga", "abcdefbh"};
    std::cout << "bitset format:" << std::endl;
    for (auto & plain : testcase) {
        auto cipher = des.encrypt(plain);
        auto plain_text = des.decrypt(cipher);
        std::cout << "plain:" << plain << ",cipher:" << cipher << ",decrypt:" << plain_text << std::endl; 
    }
    std::cout << "bytes format:" << std::endl;
    for (auto & text : testcase) {
        auto plain = str2bytes(text);
        auto cipher = des.encrypt(plain);
        auto decode = des.decrypt(cipher);
        std::cout << "plain:" << text << ", decode:" << bytes2str(decode) << std::endl;
    }
}

// a demo for aes encrypt and decrypt functions
void demo_aes() {
    std::cout << "------------- AES Encrypt/Decrypt Demo --------------" << std::endl;
    AES aes("1234567890123456");

    std::vector<std::string> testcases = {
        "bbcdefghijklmnop", "accdefghijklmnop", "abddefghijklmnop", "abceefghijklmnop",
        "abcdffghijklmnop", "abcdegghijklmnop", "abcdefhhijklmnop", "abcdefgiijklmnop",
        "abcdefghjjklmnop", "abcdefghikklmnop", "abcdefghijllmnop", "abcdefghijkmmnop",
        "abcdefghijklnnop", "abcdefghijklmoop", "abcdefghijklmnpp", "abcdefghijklmnoq"};
    for (auto & text : testcases) {
        std::cout << "text:" << text << ";";
        auto cipher = aes.encrypt(text);
        std::cout << "cipher ";
        for (int i = 0; i < cipher.size(); ++i) {
            std::cout << "[" << i << "]:" << cipher[i] << ",";
        }
        auto plain = aes.decrypt_text(cipher);
        std::cout << "plain:" << plain<< std::endl;
    }
}

void demo_ecb_des() {
    std::cout << "------------- ECB DES Encrypt/Decrypt Demo --------------" << std::endl;
    ECB<DES> op_mode("12345678");
    std::string text = "hello world, here is china";
    auto plain = str2bytes(text);
    auto cipher = op_mode.encrypt(plain);
    auto decode = op_mode.decrypt(cipher);
    auto str = bytes2str(decode);
    std::cout << "DES, text:" << text << ", str:" << str << std::endl;
}

void demo_ofb_des() {
    std::cout << "------------- OFB DES Encrypt/Decrypt Demo --------------" << std::endl;
    OFB<DES> op_mode("12345678");
    std::string text = "hello world, here is china";
    auto plain = str2bytes(text);
    auto cipher = op_mode.encrypt(plain);
    auto decode = op_mode.decrypt(cipher);
    auto str = bytes2str(decode);
    std::cout << "DES, text:" << text << ", str:" << str << std::endl;
}

void demo_cbc_des() {
    std::cout << "------------- CBC DES Encrypt/Decrypt Demo --------------" << std::endl;
    CBC<DES> op_mode("12345678");
    std::string text = "hello world, here is china";
    auto plain = str2bytes(text);
    auto cipher = op_mode.encrypt(plain);
    auto decode = op_mode.decrypt(cipher);
    auto str = bytes2str(decode);
    std::cout << "DES, text:" << text << ", str:" << str << std::endl;
}

void demo_ecb_aes() {
    std::cout << "------------- ECB AES Encrypt/Decrypt Demo --------------" << std::endl;
    ECB<AES> op_mode("1234567890123456");
    std::string text = "hello world, here is china";
    auto plain = str2bytes(text);
    auto cipher = op_mode.encrypt(plain);
    auto decode = op_mode.decrypt(cipher);
    auto str = bytes2str(decode);
    std::cout << "AES, text:" << text << ", str:" << str << std::endl;
}

void demo_ofb_aes() {
    std::cout << "------------- OFB AES Encrypt/Decrypt Demo --------------" << std::endl;
    OFB<AES> op_mode("1234567890123456");
    std::string text = "hello world, here is china";
    auto plain = str2bytes(text);
    auto cipher = op_mode.encrypt(plain);
    auto decode = op_mode.decrypt(cipher);
    auto str = bytes2str(decode);
    std::cout << "AES, text:" << text << ", str:" << str << std::endl;
}

void demo_cbc_aes() {
    std::cout << "------------- CBC AES Encrypt/Decrypt Demo --------------" << std::endl;
    CBC<AES> op_mode("1234567890123456");
    std::string text = "hello world, here is china";
    auto plain = str2bytes(text);
    auto cipher = op_mode.encrypt(plain);
    auto decode = op_mode.decrypt(cipher);
    auto str = bytes2str(decode);
    std::cout << "AES, text:" << text << ", str:" << str << std::endl;
}


int main() {
    cout << "Cryptology Homework" << endl;

    demo_des();
    demo_aes();
    demo_ecb_des();
    demo_ecb_aes();
    demo_ofb_des();
    demo_ofb_aes();
    demo_cbc_des();
    demo_cbc_aes();

    return 0;
}
