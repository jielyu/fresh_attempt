#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

json create_config()
{
    return {
        {"name", "Alice"},
        {"age", 30},
        {"active", true},
        {"scores", {95, 87, 92}}};
}

void print_json(const json &j)
{
    std::cout << j.dump(2) << std::endl;
}