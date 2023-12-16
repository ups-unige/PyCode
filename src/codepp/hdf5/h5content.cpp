#include "codepp/hdf5/h5utils.hpp"
#include <H5Opublic.h>
#include <codepp/hdf5/h5content.hpp>
#include <hdf5.h>
#include <prelude.hpp>

namespace CodePP::HDF5 {
H5Content::H5Content(hid_t file_id, hid_t base_group_id)
    : file_id(file_id), base_group_id(base_group_id) {}

auto H5Content::Open(string filename) -> optional<H5Content> {
  auto file_id = H5Fopen(filename.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
  if (file_id < 0)
    return {};
  else {
    auto base_group_id = H5Gopen(file_id, "Data/Recording_0", H5P_DEFAULT);
    if (base_group_id < 0)
      return {};
    else {
      H5Content ret(file_id, base_group_id);
             fmt::println("{}", base_group_id);
      H5Giterate(
          base_group_id, "AnalogStream", nullptr,
          [](hid_t group, const char *name, void *op_data) {
            (void)name;
            (void)op_data;
            auto tmp = H5Oopen(group, name, H5P_DEFAULT);
            auto analogs = static_cast<vector<H5Analog> *>(op_data);
            hid_t info_channel = H5Dopen(tmp, "InfoChannel", H5P_DEFAULT);
            hid_t channel_data = H5Dopen(tmp, "ChannelData", H5P_DEFAULT);
            analogs->emplace_back(
                H5Analog(tmp, name, info_channel, channel_data));
            H5Oclose(tmp);
            return 0;
          },
          static_cast<void *>(&ret.analogs));
      return ret;
    }
  }
}

H5Content::H5Content(H5Content &&moved) {
  file_id = moved.file_id;
  base_group_id = moved.base_group_id;
  moved.moved = true;
  fmt::println("H5Content Moving constructor {}", file_id);
}
auto H5Content::operator=(H5Content &&moved) -> H5Content {
  moved.moved = true;
  fmt::println("H5Content Moving assignment {}", moved.file_id);
  return {moved.file_id, moved.base_group_id};
}

H5Content::~H5Content() {
  fmt::println("H5Content Destructor {}", file_id);
  if (not moved)
    H5Fclose(file_id);
}

auto H5Content::get_tree() const -> string { return get_group_tree(file_id); }
} // namespace CodePP::HDF5
