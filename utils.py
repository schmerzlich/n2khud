# utils.py
import os, shutil

def get_working_directory():
    return os.path.dirname(os.path.abspath(__file__))

def find_file_case_insensitive(start_dir, filename):
    target = filename.lower()
    for root, _, files in os.walk(start_dir):
        for f in files:
            if f.lower() == target:
                return os.path.join(root, f)
    return None

def backup_file(path):
    if not os.path.isfile(path):
        return None
    bak = path + ".bak"
    shutil.copy2(path, bak)
    return bak
