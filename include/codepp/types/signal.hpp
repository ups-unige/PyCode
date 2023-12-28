#pragma once
#include <prelude.hpp>

namespace CodePP {
template <typename T> class Signal {
public:
  Signal() { sampling_frequency = 0; }
  Signal(const Signal &copied) = delete;
  auto operator=(const Signal &copied) = delete;
  Signal(Signal &&moved) {
    moved.moved = true;
    sampling_frequency = moved.sampling_frequency;
    data = std::move(moved.data);
  }
  auto operator=(Signal &&moved) -> Signal {
    moved.moved = true;
    Signal ret;
    ret.sampling_frequency = moved.sampling_frequency;
    ret.data = std::move(moved.data);
    return ret;
  }
  [[nodiscard]] auto copy() const -> Signal {
    Signal ret;
    ret.sampling_frequency = sampling_frequency;
    std::ranges::copy(data, begin(ret.data));
    return ret;
  }

  vector<T> data;
  float sampling_frequency;

private:
  bool moved = false;
};
}; // namespace CodePP
