#pragma once

#include <array>
using std::array;

#include <vector>
using std::vector;

#include <utility>
using std::declval;
using std::pair;
using std::tuple;

#include <string>
using std::string;

#include <iostream>
using std::cerr;
using std::cin;
using std::cout;
using std::endl;

#include <functional>
using std::function;

#include <memory>
using std::move;
using std::shared_ptr;
using std::unique_ptr;
using std::weak_ptr;

#if __cplusplus >= 202002L
#include <ranges>
using namespace std::ranges;

#include <optional>
using std::optional, std::nullopt;

#include <variant>
using std::variant;
#endif

#include <fmt/format.h>

template <typename T>
[[nodiscard]] auto expect(optional<T> opt, const string &message) -> T && {
  if (opt.has_value())
    return std::move(opt.value());
  else {
    fmt::println("{}", message);
    exit(1);
  }
}
