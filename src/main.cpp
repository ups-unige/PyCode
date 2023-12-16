#include <codepp/hdf5.hpp>
#include <prelude.hpp>

using namespace CodePP;
auto main([[__maybe_unused__]] int argc, [[__maybe_unused__]] char **argv)
    -> int {
  string filename =
      "E:/unige/raw data/03-10-2023/34341/hdf5/34341_DIV49_basal_0.h5";
  auto h5content = expect(HDF5::H5Content::Open(filename),
                          fmt::format("Error opening file {}", filename));
  return 0;
}
