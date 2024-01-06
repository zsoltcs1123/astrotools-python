import pathlib
import sys


# src has to be added to PATH so pytest can run

this_file_path = pathlib.Path(__file__)
src_core_dir_path_str = str(this_file_path.parent.joinpath("src"))
sys.path.insert(0, src_core_dir_path_str)
