#pragma once
#include <prelude.hpp>
namespace CodePP::HDF5 {

using hid_t = long long;
auto get_group_tree(const hid_t file_id) -> string;
auto get_object_path(hid_t object, string &&path) -> optional<string>;
[[nodiscard]] auto get_group_objects(hid_t group_id) -> string;
[[nodiscard]] auto get_type_name(hid_t type_id) -> string;

} // namespace CodePP::HDF5
