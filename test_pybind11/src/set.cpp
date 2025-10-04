#include <set>
#include <pybind11/pybind11.h>
// 在 PYBIND11_MODULE 外或内定义
namespace pybind11
{
    namespace detail
    {
        template <typename T>
        struct type_caster<std::set<T>>
        {
            using value_conv = make_caster<T>;

            bool load(handle src, bool convert)
            {
                if (!isinstance<sequence>(src))
                    return false;
                auto s = reinterpret_borrow<sequence>(src);
                value.clear();
                for (auto it : s)
                {
                    value_conv conv;
                    if (!conv.load(it, convert))
                        return false;
                    value.insert(cast_op<T>(conv));
                }
                return true;
            }

            static handle cast(const std::set<T> &src, return_value_policy, handle)
            {
                list l;
                for (const T &x : src)
                {
                    l.append(cast<T>(x));
                }
                return l.release();
            }

            PYBIND11_TYPE_CASTER(std::set<T>, _("Set[") + value_conv::name + _("]"));
        };
    }
} // namespace pybind11::detail

// 现在可以绑定接收 std::set 的函数
std::string describe_set(const std::set<int> &s)
{
    std::string result = "{";
    for (auto it = s.begin(); it != s.end(); ++it)
    {
        if (it != s.begin())
            result += ", ";
        result += std::to_string(*it);
    }
    result += "}";
    return result;
}