#include <codepp/hdf5.hpp>
#include <prelude.hpp>

using namespace CodePP;
auto main([[__maybe_unused__]] int argc, [[__maybe_unused__]] char **argv)
    -> int {
  string filename =
      "E:/unige/raw data/03-10-2023/34341/hdf5/34341_DIV49_basal_0.h5";
  auto h5content = unwrap(HDF5::H5Content::Open(filename));
  auto x = unwrap(h5content.analogs[2]["46"]);
  for (auto v: x.data) cout << v << endl;
  return 0;
}
