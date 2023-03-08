import os
import shutil
import filecmp

SYSTEM_PATHS: dict[str, str] = {}
PATHS: str = "auto/paths.csv"


def load_system_paths(file: str) -> None:
    """Load the system paths from the specified file."""
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                key, value = line.split(",")
                SYSTEM_PATHS[key] = value
                print(f"Loaded system path: {key} -> {value}")


def copy_and_overwrite(from_path, to_path):
    """Copy files from the from_path to the to_path, overwriting any existing files."""
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)
    
def verify_and_clean(from_path, to_path):
    """Verifies the FROM_PATH and TO_PATH are the same, and warns if they are not"""
    if not os.path.exists(from_path):
        print(f"ERROR: FROM_PATH {from_path} does not exist!")
        return
    if not os.path.exists(to_path):
        print(f"ERROR: TO_PATH {to_path} does not exist!")
        return
    for root, _, files in os.walk(from_path):
        for file in files:
            from_file = os.path.join(root, file)
            to_file = os.path.join(to_path, from_file[len(from_path)+1:])
            if not os.path.exists(to_file):
                print(f"ERROR: TO_FILE {to_file} does not exist! (FROM_FILE: {from_file})")
                continue
            if not filecmp.cmp(from_file, to_file):
                print(f"ERROR: TO_FILE {to_file} is not the same as FROM_FILE {from_file}!")
                continue
            print(f"Verified: {to_file}")
            


if __name__ == "__main__":
    print("Loading system paths...")
    load_system_paths(PATHS)
    kubejs_path = SYSTEM_PATHS["instance"]+"kubejs"
    print(f"KubeJS path: {kubejs_path}")
    copy_and_overwrite("kubejs", kubejs_path)
    verify_and_clean(kubejs_path, "kubejs")
