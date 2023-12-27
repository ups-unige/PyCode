#pragma once
#include <codepp/hdf5/h5utils.hpp>
#include <prelude.hpp>

namespace CodePP::HDF5 {

/// info_channel_struct
/// holds informations contained in the InfoChannel Dataset of an Analog Stream
///
/// With this information it is possible to convert the raw values of the ADC
/// stored in the DataChannel dataset and obtain an array of float values
/// representing the actual voltage recorded.
struct info_channel_struct {
  int channel_id;
  int row_index;
  int group_id;
  int electrode_group;
  char *label;
  char *raw_data_type;
  char *unit;
  int exponent;
  int ad_zero;
  long long int tick;
  long long int conversion_factor;
  int adc_bits;
  char *high_pass_filter_type;
  char *high_pass_filter_cutoff;
  int high_pass_filter_order;
  char *low_pass_filter_type;
  char *low_pass_filter_cutoff;
  int low_pass_filter_order;

  /// print()
  /// created for debugging pourpose. prints the value contained in the struct
  [[nodiscard]] auto info() -> string {
    string ret;
    ret += fmt::format("Channel ID:{}\n", channel_id);
    ret += fmt::format("Row Index:{}\n", row_index);
    ret += fmt::format("Group ID:{}\n", group_id);
    ret += fmt::format("Electrode Group:{}\n", electrode_group);
    if (label)
      ret += fmt::format("Label:{}\n", label);
    else
      ret += fmt::format("Label:\n");
    if (raw_data_type)
      ret += fmt::format("Raw data Type:{}\n", raw_data_type);
    else
      ret += fmt::format("Raw data Type:\n");
    if (unit)
      ret += fmt::format("Unit:{}\n", unit);
    else
      ret += fmt::format("Unit:\n");
    ret += fmt::format("Exponent:{}\n", exponent);
    ret += fmt::format("AD Zero:{}\n", ad_zero);
    ret += fmt::format("Tick:{}\n", tick);
    ret += fmt::format("Conversion factor:{}\n", conversion_factor);
    ret += fmt::format("ADC bits:{}\n", adc_bits);
    if (high_pass_filter_type)
      ret += fmt::format("HighPass Filter Type:{}\n", high_pass_filter_type);
    else
      ret += fmt::format("HighPass Filter Type:\n");
    if (high_pass_filter_cutoff)
      ret += fmt::format("HighPass Filter CutOff:{}\n", high_pass_filter_cutoff);
    else
      ret += fmt::format("HighPass Filter CutOff:\n");
    ret += fmt::format("HighPass Filter Order:{}\n", high_pass_filter_order);
    if (low_pass_filter_type)
      ret += fmt::format("LowPass Filter Type:{}\n", low_pass_filter_type);
    else
      ret += fmt::format("LowPass Filter Type:\n");
    if (low_pass_filter_cutoff)
      ret += fmt::format("LowPass Filter CutOff:{}\n", low_pass_filter_cutoff);
    else
      ret += fmt::format("LowPass Filter CutOff:\n");
    ret += fmt::format("LowPass Filter Order:{}\n", low_pass_filter_order);
    return ret;
  }
};

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
  H5Analog(hid_t group_id, string name, hid_t channel_data);
  ~H5Analog();
  H5Analog(H5Analog &&moved);
  auto operator=(H5Analog &&moved) -> H5Analog;

  H5Analog(const H5Analog &other) = delete;
  auto operator=(const H5Analog &other) = delete;

  [[nodiscard]] auto info() const -> string;
  [[nodiscard]] auto operator[](const string& label) -> Result<vector<float>>;

private:
  bool moved = false;

  hid_t group_id;
  string name;
  hid_t channel_data;
  unsigned long long n_channels;
  std::unordered_map<string, int> labels_dict;
  vector<info_channel_struct> info_channels;
};
} // namespace CodePP::HDF5
