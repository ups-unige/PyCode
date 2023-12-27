#pragma once
#include "codepp/hdf5/h5analog.hpp"
#include <codepp/hdf5/h5utils.hpp>
#include <prelude.hpp>

namespace CodePP::HDF5 {
/// H5Content
/// Class to access the content of a HDF5 file with MultiChannel Systems data
///
/// An instance of this class will handle the access to the data stored in a
/// HDF5 file created via MultiChannel Data Manager after the conversion from
/// the recorded data. The instance will open the file and lazy load data when
/// required and close the file after going out of scope. For this reason is
/// not possible to copy an instance but only move it, so that the file will
/// not be closed ahead of schedule. Moreover an instance of this class is not
/// directly constructable but to access a file a call to the static method
/// Open is needed and also a check on its return type that could be an
/// instance of H5Content or a nullopt if an error occurred.
/// In an HDF5 file MultiChannel's software could have stored a number of data
/// not all of which are already managed. The actual goal is to access the raw
/// signals stored in it that could represent the recording of an electrode or
/// some sort of sync signal for analize a stimulation; those values can be
/// found in the H5Analog elements of the analogs vector attribute of this
/// class. The order of the storage of this data (first the stimulation signal,
/// then the raw recording) is not guaranteed.
class H5Content {
public:
  static auto Open(string filename) -> Result<H5Content>;
  ~H5Content();
  H5Content(H5Content &&moved);
  auto operator=(H5Content &&moved) -> H5Content;

  H5Content(const H5Content &other) = delete;
  auto operator=(const H5Content &other) -> H5Content & = delete;

  [[nodiscard]] auto get_tree() const -> string;

  vector<H5Analog> analogs;
private:
  H5Content(hid_t file_id, hid_t base_group_id);
  bool moved = false;

  hid_t file_id;
  hid_t base_group_id;
};
} // namespace CodePP::HDF5
