#pragma once
#include <codepp/hdf5/h5utils.hpp>

namespace CodePP::HDF5 {

/// H5Analog
/// Class to access an analog signal stored in a MultiChannel HDF5 file
///
/// An instance of this class will handle the content of an analog stream
/// stored in an HDF5 file. A stream can hold more than on channel and for each
/// of them will contain two sets of information: on is an element of the
/// InfoChannel dataset inside the group that contains informations on how the
/// data should be interpreted, the other is a raw of the matrix DataChannels
/// and contains the actual data as integer values as recorded from the ADC.
/// This class will help accessing this data reading and converting them on
/// need when queried but will not hold the data itself. For this reason it
/// cannot be copied but only moved so that only one handle to the data can
/// exist.
class H5Analog {
public:
  H5Analog(hid_t group_id, string name, hid_t info_channel, hid_t channel_data);
  ~H5Analog();
  H5Analog(H5Analog &&moved);
  auto operator=(H5Analog &&moved) -> H5Analog;

  H5Analog(const H5Analog &other) = delete;
  auto operator=(const H5Analog &other) = delete;

  [[nodiscard]] auto info() const -> string;
  [[nodiscard]] auto operator[](unsigned int index) -> optional<vector<float>>;

private:
  bool moved = false;

  hid_t group_id;
  string name;
  hid_t info_channel, channel_data;
  unsigned long long n_channels;
};
} // namespace CodePP::HDF5
