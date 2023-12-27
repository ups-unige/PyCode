#pragma once
#include <codepp/hdf5/h5utils.hpp>
#include <prelude.hpp>

namespace CodePP::HDF5 {
class DatasetInspector {
public:
  enum Type {
    INTEGER,
    FLOAT,
    TIME,
    STRING,
    BITFIELD,
    OPAQUE,
    COMPOUND,
    REFERENCE,
    ENUM,
    VLEN,
    ARRAY,
    NOT_IMPLEMENTED,
  };
  struct Field {
    string name;
    size_t offset, size;
    hid_t field_id;
    Type type;

    [[nodiscard]] auto byte_order() const -> string;
    [[nodiscard]] auto cset() const -> string;
    [[nodiscard]] auto strvlen() const -> string;
    [[nodiscard]] auto strpad() const -> string;
    [[nodiscard]] auto sign() const -> string;
  };

  static auto build(hid_t dataset_id) -> Result<DatasetInspector>;
  DatasetInspector(const DatasetInspector &copied) = delete;
  auto operator=(const DatasetInspector &copied) = delete;
  DatasetInspector(DatasetInspector &&moved);
  auto operator=(DatasetInspector &&moved) -> DatasetInspector;
  ~DatasetInspector();

  [[nodiscard]] auto structure() const -> Result<string>;
  static auto selection_info(hid_t selection) -> Result<string>;

private:
  DatasetInspector() = default;
  static auto type_name(Type t) -> string;
  [[nodiscard]] auto type_structure(const Field& field) const -> string;

  hid_t datatype_id;
  hid_t dataspace_id;
  hid_t memory_type;
  bool moved = false;
  vector<Field> fields;
  vector<size_t> dimensions;
};
} // namespace CodePP::HDF5
