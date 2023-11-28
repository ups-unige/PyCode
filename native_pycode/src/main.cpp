#include <fmt/format.h>
#include <hdf5.hpp>
#include <prelude.hpp>
#include <python.hpp>

using CodePP::Python::PyRef;

auto main([[__maybe_unused__]] int argc, [[__maybe_unused__]] char **argv)
    -> int {
  // const string filepath =
  //     "e:/unige/raw data/03-10-2023/34341/hdf5/34341_DIV49_stim_4_60.h5";

  //  auto file_opt = CodePP::HDF5::H5Content::build(filepath);
  //  if (not file_opt.has_value()) {
  //    cout << "Error opening file " << filepath << endl;
  //  }
  //
  //  auto file = std::move(file_opt.value());
  //  // cout << file->get_tree() << endl;
  //  for (auto &analog : file->get_analogs()) {
  //    cout << analog.info() << endl;
  //  }
  //
  //

  if (argc > 0) {
    CodePP::Python::Python interpreter(argv[0]);
    interpreter.f();
  }
  return 0;
}
