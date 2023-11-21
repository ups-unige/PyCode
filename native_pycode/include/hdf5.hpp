#pragma once

#include <H5Cpp.h>
#include <prelude.hpp>

namespace CodePP::HDF5 {

class H5Analog {
public:
  H5Analog(hid_t file_id, hid_t group_id, string name)
      : file_id(file_id), group(group_id), name(std::move(name)) {}

  [[nodiscard]] auto info() const -> string;

private:
  hid_t file_id;
  H5::Group group;
  string name;
};

class H5Content {
public:
  static auto build(const string &path) -> optional<unique_ptr<H5Content>>;
  ~H5Content();
  /// get_tree() -> string
  ///
  /// @returns a string with in each line a path in the tree
  [[nodiscard]] auto get_tree() -> string const;
  /// get_analogs -> vector<H5Analog>
  ///
  /// @returns a vector with all the analog streams contained in the file
  [[nodiscard]] auto get_analogs() const -> vector<H5Analog>;

private:
  H5Content(hid_t file_id);
  hid_t file_id;
};
} // namespace CodePP::HDF5
