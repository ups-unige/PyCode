#include <fmt/format.h>
#include <fmt/xchar.h>
#include <python.hpp>

namespace CodePP::Python {

Python::Python(string argv0) {
  program = Py_DecodeLocale(argv0.c_str(), nullptr);
  if (program == nullptr) {
    cerr << "Fatal error: cannot decode argv[0]" << endl;
    exit(1);
  }
  Py_SetProgramName(program);
  Py_Initialize();
}

Python::~Python() {
  if (Py_FinalizeEx() < 0) {
    exit(120);
  };
  PyMem_RawFree(program);
}

void Python::f() const {
  string name = "multiply";
  string func = "multiply";
  vector<string> args = {"3", "2"};

  PyRef pModule;
  {
    PyRef pName = PyUnicode_DecodeFSDefault(name.c_str());
    pModule = PyImport_Import(pName.ref);
  }

  if (pModule.ref != nullptr) {
    PyRef pFunc = PyObject_GetAttrString(pModule.ref, func.c_str());
    if (pFunc.ref and PyCallable_Check(pFunc.ref)) {
      PyRef pArgs = PyTuple_New(args.size());
      auto i = 0;
      for (auto &arg : args) {
        PyRef<true> pValue = PyLong_FromLong(std::stol(arg));
        if (!pValue.ref) {
          fmt::print("Cannot convert argument {}", arg);
        }
        PyTuple_SetItem(pArgs.ref, i++, pValue.ref);
      }
      PyRef pValue = PyObject_CallObject(pFunc.ref, pArgs.ref);
      if (pValue.ref != nullptr) {
        fmt::print("Result of the call: {}\n", PyLong_AsLong(pValue.ref));
      } else {
        PyErr_Print();
        fmt::print("Call failed\n");
      }
    } else {
      PyErr_Print();
      fmt::print("Cannot find function \"{}\"\n", func);
    }
  } else {
    PyErr_Print();
    fmt::print("Falied to load \"{}\"\n", name);
  }
}
} // namespace CodePP::Python
