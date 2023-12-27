#include <H5Tpublic.h>
#include <codepp/hdf5/h5utils.hpp>
#include <hdf5/hdf5.h>

namespace CodePP::HDF5 {

////////////////////////////////////////////////////////////////////////////////
///
///                               UTILITIES
///
////////////////////////////////////////////////////////////////////////////////

/// get_tree (const hid_t file_id) -> string
/// get the tree content of the file at *filepath*
///
/// @param [in] file_id
/// @returns a string with the tree
///
/// This function open the file at the path in read only mode and visit each
/// node inside it storing the name of the node in an common string that is
/// the return value of the function.
auto get_group_tree(const hid_t file_id) -> string {

  auto ret = string{""};

  H5Ovisit2(
      file_id, H5_INDEX_NAME, H5_ITER_INC,
      []([[__maybe_unused__]] hid_t obj, [[__maybe_unused__]] const char *name,
         [[__maybe_unused__]] const H5O_info1_t *info,
         [[__maybe_unused__]] void *op_data) {
        auto &aret = *static_cast<string *>(op_data);
        aret += name;
        aret += '\n';
        return 0;
      },
      &ret, H5O_INFO_BASIC);
  return ret;
}

/// get_object_path(hid_t object, string&& path) -> optional<string>
/// get the path of an object
///
/// @param [in] object: the hid_t of the object
/// @param [in] path: a reference to the string where to store the path
/// @returns a string with the path of the object, if succeded, nullopt
///          otherwise
auto get_object_path(hid_t object, string &&path) -> optional<string> {
  if (path.length() == 0)
    path.resize(64);
  auto res = H5Iget_name(object, path.data(), path.length());
  if (res <= 0)
    return {};
  else if (res == static_cast<long long>(path.length())) {
    path.resize(path.length() * 2);
    return CodePP::HDF5::get_object_path(object, std::move(path));
  } else {
    return {path};
  }
}

/// get_group_objects(hid_t group_id) -> string
/// get a list of the objects linked to a group
///
/// @param [in] group_id
/// @returns a string with a list of the names of the linked objects
[[nodiscard]] auto get_group_objects(hid_t group_id) -> string {
  string ret;

  H5Literate(
      group_id, H5_INDEX_NAME, H5_ITER_INC, nullptr,
      []([[maybe_unused]] hid_t group, [[maybe_unused]] const char *name,
         [[maybe_unused]] const H5L_info2_t *info,
         [[maybe_unused]] void *op_data) {
        auto ret = reinterpret_cast<string *>(op_data);
        *ret += string(name) + '\n';
        return 0;
      },
      &ret);

  return ret;
}

/// get_type_name(hid_t type_id) -> string
/// get the name of an hdf5 type from its id
///
/// @param [in] type_id
/// @returns a string with the type name
auto get_type_name(hid_t type_id) -> string {
  switch (H5Tget_class(type_id)) {
  case H5T_FLOAT:
    return "Float";
  case H5T_INTEGER:
    return "Integer";
  case H5T_ARRAY:
    return "Array";
  case H5T_STRING:
    return "String";
  case H5T_COMPOUND:
    return "Compound";
  default:
    return "Unkown";
  }
}

} // namespace CodePP::HDF5
