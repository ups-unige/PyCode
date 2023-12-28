// #include "codepp/hdf5/type_inspector.hpp"
#include "codepp/hdf5/h5utils.hpp"
#include "prelude.hpp"
#include <H5Ppublic.h>
#include <H5Tpublic.h>
#include <codepp/hdf5/h5analog.hpp>
#include <hdf5/hdf5.h>

////////////////////////////////////////////////////////////////////////////////
///
///                               H5ANALOG
///
////////////////////////////////////////////////////////////////////////////////

namespace CodePP::HDF5 {

/// InfoChannelMemoryType
/// utitity for reading the values of the InfoChannel dataset
///
/// this class create and stores a value adapt to be used in the H5Dread
/// function for reading the InfoChannel dataset from the physical storage and
/// copy into an info_channel_struct into memory
class InfoChannelMemoryType {
public:
  InfoChannelMemoryType() {
    strtype = H5Tcopy(H5T_C_S1);
    H5Tset_size(strtype, H5T_VARIABLE);
    H5Tset_strpad(strtype, H5T_STR_NULLPAD);
    H5Tset_cset(strtype, H5T_CSET_ASCII);
    id = H5Tcreate(H5T_COMPOUND, sizeof(struct info_channel_struct));
    H5Tinsert(id, "ChannelID", HOFFSET(struct info_channel_struct, channel_id),
              H5T_NATIVE_INT);
    H5Tinsert(id, "RowIndex", HOFFSET(struct info_channel_struct, row_index),
              H5T_NATIVE_INT);
    H5Tinsert(id, "GroupID", HOFFSET(struct info_channel_struct, group_id),
              H5T_NATIVE_INT);
    H5Tinsert(id, "ElectrodeGroup",
              HOFFSET(struct info_channel_struct, electrode_group),
              H5T_NATIVE_INT);
    H5Tinsert(id, "Label", HOFFSET(struct info_channel_struct, label), strtype);
    H5Tinsert(id, "RawDataType",
              HOFFSET(struct info_channel_struct, raw_data_type), strtype);
    H5Tinsert(id, "Unit", HOFFSET(struct info_channel_struct, unit), strtype);
    H5Tinsert(id, "Exponent", HOFFSET(struct info_channel_struct, exponent),
              H5T_NATIVE_INT);
    H5Tinsert(id, "AdZero", HOFFSET(struct info_channel_struct, ad_zero),
              H5T_NATIVE_INT);
    H5Tinsert(id, "Tick", HOFFSET(struct info_channel_struct, tick),
              H5T_NATIVE_LLONG);
    H5Tinsert(id, "ConversionFactor",
              HOFFSET(struct info_channel_struct, conversion_factor),
              H5T_NATIVE_LLONG);
    H5Tinsert(id, "ADCBits", HOFFSET(struct info_channel_struct, adc_bits),
              H5T_NATIVE_INT);
    H5Tinsert(id, "HighPassFilterType",
              HOFFSET(struct info_channel_struct, high_pass_filter_type),
              strtype);
    H5Tinsert(id, "HighPassFilterCutOff",
              HOFFSET(struct info_channel_struct, high_pass_filter_cutoff),
              strtype);
    H5Tinsert(id, "HighPassFilterOrder",
              HOFFSET(struct info_channel_struct, high_pass_filter_order),
              H5T_NATIVE_INT);
    H5Tinsert(id, "LowPassFilterType",
              HOFFSET(struct info_channel_struct, low_pass_filter_type),
              strtype);
    H5Tinsert(id, "LowPassFilterCutOff",
              HOFFSET(struct info_channel_struct, low_pass_filter_cutoff),
              strtype);
    H5Tinsert(id, "LowPassFilterOrder",
              HOFFSET(struct info_channel_struct, low_pass_filter_order),
              H5T_NATIVE_INT);
  }
  InfoChannelMemoryType(const InfoChannelMemoryType &copied) = delete;
  auto operator=(const InfoChannelMemoryType &copied) = delete;

  ~InfoChannelMemoryType() {
    H5Tclose(strtype);
    H5Tclose(id);
  }

  auto get_id() { return id; }

private:
  hid_t strtype, id;
};

H5Analog::H5Analog(hid_t group_id, string name, hid_t channel_data)
    : group_id(group_id), name(std::move(name)), channel_data(channel_data) {

  // here the number of channels in an analog stream is retrieved from the
  // dimension of the InfoChannel dataset and it's stored in n_channels
  auto info_channel = H5Dopen(group_id, "InfoChannel", H5P_DEFAULT);
  auto info_dataspace = H5Dget_space(info_channel);
  H5Sget_simple_extent_dims(info_dataspace, &n_channels, nullptr);

  // then the space for the info_channel datas is allocated
  info_channels.resize(n_channels);

  // the datatype and the dataspace for both storage and memory are crated.
  // this because the hdf5 library needs to know how the data in the filesystem
  // and in the memory must be interpreted

  // auto storage_dataspace = H5Dget_space(info_channel);
  // auto storage_datatype = H5Dget_type(info_channel);
  InfoChannelMemoryType memory_datatype;
  // vector<size_t> memory_dimenstions{n_channels};
  // auto memory_dataspace =
  //     H5Screate_simple(1, memory_dimenstions.data(), nullptr);
  H5Dread(info_channel, memory_datatype.get_id(), H5S_ALL, H5S_ALL, H5P_DEFAULT,
          info_channels.data());

  // storing the map from label to indices for a quicker access later on
  for (unsigned int i = 0; i < n_channels; ++i) {
    labels_dict.insert_or_assign(info_channels[i].label, i);
  }

  // finally all the objects no more needed are closed
  H5Sclose(info_dataspace);
  H5Dclose(info_channel);
}

H5Analog::H5Analog(H5Analog &&moved) {
  group_id = moved.group_id;
  name = std::move(moved.name);
  channel_data = moved.channel_data;
  n_channels = moved.n_channels;
  labels_dict = std::move(moved.labels_dict);
  info_channels = std::move(moved.info_channels);
  moved.moved = true;
}

auto H5Analog::operator=(H5Analog &&moved) -> H5Analog {
  moved.moved = true;
  auto ret = H5Analog(group_id, name, channel_data);
  ret.n_channels = moved.n_channels;
  ret.labels_dict = std::move(moved.labels_dict);
  ret.info_channels = std::move(moved.info_channels);
  return ret;
}

H5Analog::~H5Analog() {
  if (not moved) {
    H5Dclose(channel_data);
    H5Gclose(group_id);
  }
}

auto H5Analog::operator[](const string &label) -> Result<Signal<float>> {
  if (not labels_dict.contains(label))
    return Error{
        fmt::format("H5Analog Operator[]: not a valid label {}", label)};
  else {
    // retrieve the info_channel of the choosen label
    auto index = labels_dict[label];

    auto channel_data_index =
        info_channels[index]
            .row_index; // index of the data in the ChannelData dataset

    // getting the conversion parameters
    auto ad_zero = info_channels[index].ad_zero;
    auto conversion_factor = info_channels[index].conversion_factor;
    auto exponent = info_channels[index].exponent;
    float conversion_factorf = static_cast<float>(conversion_factor) *
                               static_cast<float>(std::pow(10, exponent));

    // get the DataChannel dataspace and its dimensions
    //
    auto data_channel_dataspace_id = H5Dget_space(channel_data);
    auto n_dims = H5Sget_simple_extent_ndims(data_channel_dataspace_id);
    vector<size_t> dims(n_dims);
    H5Sget_simple_extent_dims(data_channel_dataspace_id, dims.data(), nullptr);

    if (dims.size() != 2 and dims[0] != n_channels)
      return Error{fmt::format(
          "H5Analog operator[] error in querying {} label data", label)};

    // get the selection of the dataspace for the choosen label
    array<size_t, 1> memory_size_array{dims[1]};
    [[maybe_unused]] auto memory_dataspace =
        H5Screate_simple(1, memory_size_array.data(), nullptr);

    array<size_t, 2> storage_slab_start{static_cast<size_t>(channel_data_index),
                                        0};
    array<size_t, 2> storage_slab_count{1, dims[1]};
    H5Sselect_hyperslab(data_channel_dataspace_id, H5S_SELECT_SET,
                        storage_slab_start.data(), nullptr,
                        storage_slab_count.data(), nullptr);
    vector<int> data(dims[1]);
    // read its value
    H5Dread(channel_data, H5T_NATIVE_INT, memory_dataspace,
            data_channel_dataspace_id, H5P_DEFAULT, data.data());

    // build the return value
    Signal<float> ret;
    ret.data.resize(dims[1]);

    // subtract the offset and multiply the data for the conversion factor
    for (size_t i = 0; i < dims[1]; ++i) {
      ret.data[i] = (data[i] - ad_zero) * conversion_factorf;
    }

    // compute the sampling frequency
    ret.sampling_frequency = 1e6 / info_channels[index].tick;
    return ret;
  }
}

auto H5Analog::info() const -> string {
  string ret;
  //--------------------------    Name     ---------------------------------
  ret += "path: " + name + "\n";
  ret += "-----------------------------------------------------\n";
  return ret;
}
} // namespace CodePP::HDF5
