import sys
import os

file_path = os.path.abspath(os.path.dirname(__file__))
dir_path = os.path.dirname(file_path)
src_path = os.path.join(dir_path, "src")

src_path = os.path.realpath(src_path)

sys.path.insert(0, src_path)
print(sys.path)
