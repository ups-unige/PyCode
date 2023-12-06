#pragma once
#include <prelude.hpp>

namespace CodePP {
namespace HDF5 {
enum HChannelType {
  AnalogStream,
  TimeEventStamp,
};
template <HChannelType type> class HDataset {
  public:
  HChannelType channel_type = type;
};
class HStream {};
class H5Data {};
} // namespace HDF5
namespace Python {
class Python {
public:
  Python(string argv0);
  ~Python();

  void f() const;

private:
  wchar_t *program;
};
} // namespace Python
} // namespace CodePP
