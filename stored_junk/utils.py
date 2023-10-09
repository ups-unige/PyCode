
# keeped for some time but consider delete it
# def mea_60_electrode_index_to_number(index: int) -> int:
#     """
#     Return the corresponding electrode number (in the range 12-87) from an
#     index (in the range 1-60). The electrode are supposed to be indexed from
#     top to bottom and from left to right. Their labelling pattern is:
#
#                1  2  3  4  5  6               12 13 14 15 16 17
#             7  8  9 10 11 12 13 14         21 22 23 24 25 26 27 28
#            15 16 17 18 19 20 21 22         31 32 33 34 35 36 37 38
#            23 24 25 26 27 28 29 30  <----> 41 42 43 44 45 46 47 48
#            31 32 33 34 35 36 37 38         51 52 53 54 55 56 57 58
#            39 40 41 42 43 44 45 46         61 62 63 64 65 66 67 68
#            47 48 49 50 51 52 53 54         71 72 73 74 75 76 77 78
#               55 56 57 58 59 60               82 83 84 85 86 87
#     """
#     if not (index > 0 and index < 61):
#         raise Exception("Error: INDEX should be in range [1-60]")
#     if index <= 6:
#         return 11 + index
#     elif index <= 54:
#         index = index - 6
#         return 20 + index // 8 * 10 + index % 8
#     else:
#         index = index - 54
#         return 81 + index


# keeped for some time but consider delete it
# def mea_60_electrode_number_to_index(number: int) -> int:
#     """
#     Return the corresponding index (in the range 1-60) from an electrode
#     number (in the range 12-87).
#
#               12 13 14 15 16 17                 1  2  3  4  5  6
#            21 22 23 24 25 26 27 28           7  8  9 10 11 12 13 14
#            31 32 33 34 35 36 37 38          15 16 17 18 19 20 21 22
#            41 42 43 44 45 46 47 48  <---->  23 24 25 26 27 28 29 30
#            51 52 53 54 55 56 57 58          31 32 33 34 35 36 37 38
#            61 62 63 64 65 66 67 68          39 40 41 42 43 44 45 46
#            71 72 73 74 75 76 77 78          47 48 49 50 51 52 53 54
#               82 83 84 85 86 87                55 56 57 58 59 60
#     """
#     if number not in full_mea_60:
#         raise Exception("Error: NUMBER should be a valide electrode number")
#
#     if number <= 17:
#         return number-11
#     elif number <= 78:
#         return 6 + (number // 10 - 2) * 8 + number % 10
#     else:
#         return 54 + number-81
