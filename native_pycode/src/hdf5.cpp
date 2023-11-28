#include <cstring>
#include <hdf5.hpp>

using namespace H5;

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
auto get_file_tree(const hid_t file_id) -> string {

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

////////////////////////////////////////////////////////////////////////////////
///
///                               H5NANALOG
///
////////////////////////////////////////////////////////////////////////////////

H5Analog::H5Analog(hid_t file_id, hid_t group_id, string name)
    : file_id(file_id), group(group_id), name(std::move(name)) {
}

auto H5Analog::info() const -> string {
  string ret;
  ret += "path: " + name + "\n";
  auto info_channel_dataset =
      H5Oopen(group.getId(), (name + "/InfoChannel").c_str(), H5P_DEFAULT);
  auto dataspace_id = H5Dget_space(info_channel_dataset);
  auto ndims = H5Sget_simple_extent_ndims(dataspace_id);
  auto npoints = H5Sget_simple_extent_npoints(dataspace_id);
  ret += std::to_string(ndims) + ", " + std::to_string(npoints) + "\n";
  ret += "-----------------------------------------------------\n";
  return ret;
}

////////////////////////////////////////////////////////////////////////////////
///
///                                  H5CONTENT
///
////////////////////////////////////////////////////////////////////////////////

auto H5Content::build(const string &path) -> optional<unique_ptr<H5Content>> {
  auto file_id = H5Fopen(path.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
  if (file_id > 0) {
    auto ret = new H5Content(file_id);
    return optional{unique_ptr<H5Content>(ret)};
  }
  return {};
}

auto H5Content::get_tree() -> string const { return get_file_tree(file_id); }

H5Content::H5Content(hid_t file_id) : file_id(file_id) {
  cout << file_id << endl;
}

H5Content::~H5Content() { H5Fclose(file_id); }

auto H5Content::get_analogs() const -> vector<H5Analog> {
  vector<H5Analog> ret;
  auto analog_group = H5::Group(
      H5Oopen(file_id, "/Data/Recording_0/AnalogStream", H5P_DEFAULT));
  auto analog_group_id = analog_group.getId();
  if (analog_group_id > 0) {
    for (unsigned int i = 0; i < analog_group.getNumObjs(); ++i) {
      string obj_name = string("/Data/Recording_0/AnalogStream") + "/Stream_" +
                        std::to_string(i);
      hid_t obj_id = H5Oopen(analog_group_id, obj_name.c_str(), H5P_DEFAULT);
      if (obj_id > 0)
        ret.emplace_back(file_id, obj_id, obj_name);
      else {
        cout << "ERROR finding the Stream_" + std::to_string(i) + " group"
             << endl;
      }
    }
  }
  return ret;
}
} // namespace CodePP::HDF5
