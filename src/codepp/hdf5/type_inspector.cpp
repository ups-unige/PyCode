#include "codepp/hdf5/h5utils.hpp"
#include <H5Dpublic.h>
#include <H5Spublic.h>
#include <codepp/hdf5/type_inspector.hpp>
#include <hdf5.h>

namespace CodePP::HDF5 {

auto DatasetInspector::type_name(Type type) -> string {
  switch (type) {
  case INTEGER:
    return "INTEGER";
  case FLOAT:
    return "FLOAT";
    break;
  case STRING:
    return "STRING";
    break;
  case BITFIELD:
    return "BITFIELD";
    break;
  case OPAQUE:
    return "OPAQUE";
    break;
  case COMPOUND:
    return "COMPOUND";
    break;
  case REFERENCE:
    return "REFERENCE";
    break;
  case ENUM:
    return "ENUM";
    break;
  case VLEN:
    return "VLEN";
    break;
  case ARRAY:
    return "ARRAY";
    break;
  default:
    return fmt::format("UNKNOWN: {}", static_cast<unsigned int>(type));
  }
}

inline auto DatasetInspector::Field::byte_order() const -> string {
  auto value = H5Tget_order(field_id);
  switch (value) {
  case H5T_ORDER_ERROR:
    return "Error";
  case H5T_ORDER_LE:
    return "Little Endian";
  case H5T_ORDER_BE:
    return "Big Endian";
  case H5T_ORDER_VAX:
    return "Vax";
  case H5T_ORDER_MIXED:
    return "Mixed";
  case H5T_ORDER_NONE:
    return "None";
  default:
    return "Unknown";
  }
}

inline auto DatasetInspector::Field::sign() const -> string {
  auto value = H5Tget_sign(field_id);
  switch (value) {
  case H5T_SGN_ERROR:
    return "Error";
  case H5T_SGN_NONE:
    return "No sign";
  case H5T_SGN_2:
    return "With sign";
  case H5T_NSGN:
    return "Nsgn";
  default:
    return "Unknown";
  }
}

inline auto DatasetInspector::Field::cset() const -> string {
  auto value = H5Tget_cset(field_id);
  switch (value) {
  case H5T_CSET_ERROR:
    return "Error";
  case H5T_CSET_ASCII:
    return "ASCII";
  case H5T_CSET_UTF8:
    return "UTF-8";
  default:
    return "Unknown";
  }
}

inline auto DatasetInspector::Field::strpad() const -> string {
  auto value = H5Tget_strpad(field_id);
  switch (value) {
  case -1:
    return "Error";
  case 0:
    return "C-style NULL terminated";
  case 1:
    return "Pad with zeros";
  case 2:
    return "Pad with spaces";
  default:
    return "Unknown";
  }
}

inline auto DatasetInspector::Field::strvlen() const -> string {
  auto value = H5Tis_variable_str(field_id);
  switch (value) {
  case -1:
    return "Error";
  case 0:
    return "False";
  case 1:
    return "True";
  default:
    return "Unknown";
  }
}

inline auto H5TypeToInspectorType(H5T_class_t value) -> DatasetInspector::Type {
  using Type = DatasetInspector::Type;
  switch (value) {
  case H5T_NO_CLASS:
    return Type::NOT_IMPLEMENTED;
  case H5T_INTEGER:
    return Type::INTEGER;
  case H5T_FLOAT:
    return Type::FLOAT;
  case H5T_TIME:
    return Type::TIME;
  case H5T_STRING:
    return Type::STRING;
  case H5T_BITFIELD:
    return Type::BITFIELD;
  case H5T_OPAQUE:
    return Type::OPAQUE;
  case H5T_COMPOUND:
    return Type::COMPOUND;
  case H5T_REFERENCE:
    return Type::REFERENCE;
  case H5T_ENUM:
    return Type::ENUM;
  case H5T_VLEN:
    return Type::VLEN;
  case H5T_ARRAY:
    return Type::VLEN;
  case H5T_NCLASSES:
    return Type::NOT_IMPLEMENTED;
  default:
    return Type::NOT_IMPLEMENTED;
  }
}

auto DatasetInspector::build(hid_t dataset_id) -> Result<DatasetInspector> {
  DatasetInspector ret;
  ret.datatype_id = H5Dget_type(dataset_id);
  if (not(H5Tget_class(ret.datatype_id) == H5T_COMPOUND)) {
    return Error{"DatasetInspector Open called with a non compound type"};
  }

  // getting informations from the compound datatype
  size_t current_offset = 0;

  auto type_nmembers = H5Tget_nmembers(ret.datatype_id);
  for (auto i = 0; i < type_nmembers; ++i) {
    auto member_type_id = H5Tget_member_type(ret.datatype_id, i);
    auto member_size = H5Tget_size(member_type_id);
    auto member_name = H5Tget_member_name(ret.datatype_id, i);
    ret.fields.push_back(
        Field{member_name, current_offset, member_size, member_type_id,
              H5TypeToInspectorType(H5Tget_class(member_type_id))});
    H5free_memory(member_name);
    current_offset += member_size;
  }

  // getting informations about the dataspace
  ret.dataspace_id = H5Dget_space(dataset_id);
  ret.dimensions.resize(H5Sget_simple_extent_ndims(ret.dataspace_id));
  H5Sget_simple_extent_dims(ret.dataspace_id, ret.dimensions.data(), nullptr);

  return ret;
}

auto DatasetInspector::selection_info(hid_t selection) -> Result<string> {
  string ret;
  ret += "-------------------------------------\n";
  ret += fmt::format("{}", selection);
  ret += "-------------------------------------\n";
  return ret;
}

DatasetInspector::DatasetInspector(DatasetInspector &&moved) {
  moved.moved = true;
  memory_type = moved.memory_type;
  fields = std::move(moved.fields);
  dimensions = std::move(moved.dimensions);
}

auto DatasetInspector::operator=(DatasetInspector &&moved) -> DatasetInspector {
  moved.moved = true;
  DatasetInspector ret;
  ret.memory_type = moved.memory_type;
  ret.fields = std::move(moved.fields);
  ret.dimensions = std::move(moved.dimensions);
  return ret;
}

DatasetInspector::~DatasetInspector() {
  if (not moved) {
    H5Tclose(datatype_id);
    H5Sclose(dataspace_id);
    // H5Tclose(memory_type);
  }
}

auto DatasetInspector::type_structure(const Field &field) const -> string {
  string ret;
  ret += fmt::format("Name: {}\n"
                     "Offset: {}\n"
                     "Size: {}\n"
                     "Type: {}\n"
                     "Byte order: {}\n",
                     field.name, field.offset, field.size,
                     type_name(field.type), field.byte_order());
  switch (field.type) {
  case INTEGER:
    ret += fmt::format("Sign: {}\n", field.sign());
    break;
  case STRING:;
    ret += fmt::format("Is variable length: {}\n"
                       "Padding: {}\n"
                       "Char Set: {}\n",
                       field.strvlen(), field.strpad(), field.cset());
    break;
  default:;
  }
  ret += "-------------------------------------\n";
  return ret;
}

auto DatasetInspector::structure() const -> Result<string> {
  string ret;
  ret += "-------------------------------------\n";
  for (auto const &field : fields) {
    ret += type_structure(field);
  }

  ret += fmt::format("Simple dataspace: {}\n", H5Sis_simple(dataspace_id));
  ret += fmt::format("Dataspace rank: {}\nDimensions: [ ", dimensions.size());
  for (auto &dim : dimensions) {
    ret += fmt::format("{} ", dim);
  }
  ret += "]\n-------------------------------------\n";

  return ret;
}
} // namespace CodePP::HDF5
