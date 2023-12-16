#include "codepp/hdf5/h5utils.hpp"
#include <H5public.h>
#include <codepp/hdf5/h5analog.hpp>
#include <hdf5/hdf5.h>

////////////////////////////////////////////////////////////////////////////////
///
///                               H5ANALOG
///
////////////////////////////////////////////////////////////////////////////////

namespace CodePP::HDF5 {

H5Analog::H5Analog(hid_t group_id, string name, hid_t info_channel,
                   hid_t channel_data)
    : group_id(group_id), name(std::move(name)), info_channel(info_channel),
      channel_data(channel_data) {

  // here the number of channels in an analog stream is retrieved from the 
  // dimension of the InfoChannel dataset and it's stored in n_channels
  auto info_dataspace = H5Dget_space(info_channel);
  H5Sget_simple_extent_dims(info_dataspace, &n_channels, nullptr);
  fmt::println("Dataspace of InfoChannel: {}", n_channels);
  H5Sclose(info_dataspace);
}

H5Analog::H5Analog(H5Analog &&moved) {
  group_id = moved.group_id;
  name = std::move(moved.name);
  info_channel = moved.info_channel;
  channel_data = moved.channel_data;
  moved.moved = true;
  fmt::println("H5Analog Moving constructor {}", group_id);
}

auto H5Analog::operator=(H5Analog &&moved) -> H5Analog {
  moved.moved = true;
  fmt::println("H5Analog Moving assignment {}", moved.group_id);
  return {group_id, name, info_channel, channel_data};
}

H5Analog::~H5Analog() {
  if (not moved) {
    H5Dclose(info_channel);
    H5Dclose(channel_data);
  }
  fmt::println("H5Analog Destructor {}", group_id);
}

auto H5Analog::operator[](unsigned int index) -> optional<vector<float>> {
  (void)index;
  return {};
}

auto H5Analog::info() const -> string {
  string ret;
  //--------------------------    Name     ---------------------------------
  ret += "path: " + name + "\n";
  //-------------------------- InfoChannel ---------------------------------
  auto info_channel_dataset =
      H5Oopen(group_id, (name + "/InfoChannel").c_str(), H5P_DEFAULT);
  auto dataspace_id = H5Dget_space(info_channel_dataset);
  auto ndims = H5Sget_simple_extent_ndims(dataspace_id);
  auto npoints = H5Sget_simple_extent_npoints(dataspace_id);
  //-------------------------- ChannelData ---------------------------------
  auto channel_data_dataset =
      H5Oopen(group_id, (name + "/ChannelData").c_str(), H5P_DEFAULT);
  auto channel_dataspace_id = H5Dget_space(channel_data_dataset);
  auto channel_ndims = H5Sget_simple_extent_ndims(channel_dataspace_id);
  vector<hsize_t> channel_dims(channel_ndims);
  H5Sget_simple_extent_dims(channel_dataspace_id, channel_dims.data(), nullptr);
  auto channel_npoints = H5Sget_simple_extent_npoints(channel_dataspace_id);

  //------------------------- InfoChannel 1 --------------------------------
  auto datatype_id = H5Dget_type(info_channel_dataset);

  fmt::println("{}", datatype_id);

  ret += "-----------------------------------------------------\n";
  ret += "InfoChannel\n";
  ret += std::to_string(ndims) + ", " + std::to_string(npoints) + "\n";
  ret += "-----------------------------------------------------\n";
  ret += "ChannelData\n(";
  for (auto dim : channel_dims)
    ret += fmt::to_string(dim) + " ";
  ret += "), " + std::to_string(channel_npoints) + "\n";
  ret += "-----------------------------------------------------\n";
  return ret;
}
} // namespace CodePP::HDF5
