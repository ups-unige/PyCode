#include <prelude.hpp>
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#pragma once
namespace CodePP::Python {
template <bool x = false> struct PyRef {
  PyRef() : ref(nullptr) {}
  PyRef(PyObject *ref) : ref(ref) {}
  auto operator=(PyObject *ref) -> PyRef & {
    this->ref = ref;
    return *this;
  }
  ~PyRef() {
    if constexpr (x) {
      Py_XDECREF(ref);
    } else
      Py_DECREF(ref);
  }
  PyObject *ref;
};
} // namespace CodePP
