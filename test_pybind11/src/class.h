#pragma once
#include <string>

class Pet
{
public:
    std::string nick_name;
    int age = 0;
    Pet(const std::string &name) : name_(name) {}
    void setName(const std::string &name) { name_ = name; }
    const std::string &getName() const { return name_; }

private:
    std::string name_;
};