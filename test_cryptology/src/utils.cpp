#include "utils.h"

namespace crypt_impl
{
    

std::vector<Byte> str2bytes(const std::string text) {
    std::vector<Byte> bytes;
    for (int i = 0; i < text.size(); ++i) {
        bytes.push_back(Byte((unsigned int)text[i]));
    }
    return bytes;
}

std::string bytes2str(const std::vector<Byte> & bytes) {
    std::string text(bytes.size(), '\0');
    for (int i = 0; i < bytes.size(); ++i) {
        text[i] = (char)bytes[i].to_ulong();
    }
    return text;
}

Word bytes2word(Byte b1, Byte b2, Byte b3, Byte b4) {
    Word w(0), tmp;
    Byte bytes[4] = {b1, b2, b3, b4};
    for (int i = 1; i <= 4; ++i) {
        tmp = bytes[i-1].to_ulong();
        tmp <<= 32 - 8*i;
        w |= tmp;
    }
    return w;
}

} // namespace crypt_impl
