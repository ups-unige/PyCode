from pycode.io import load_phase_from_hdf5

filepath = "e:/unige/raw data/03-10-2023/34341/hdf5/34341_DIV49_basal_0.h5"

if __name__ == "__main__":
    phase = load_phase_from_hdf5(filepath)
