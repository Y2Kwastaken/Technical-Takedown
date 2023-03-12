import os
import shutil

SYSTEM_PATHS: dict[str, str] = {}
PATHS: str = "auto/paths.csv"


def get_system_paths() -> None:
    """Load the system paths from the specified file."""
    with open(PATHS, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                key, value = line.split(",")
                SYSTEM_PATHS[key] = value
                print(f"Loaded system path: {key} -> {value}")


class MinecraftFolder():

    def __init__(self, path: str) -> None:
        self.path = path
        self.kubejs_path = self.path + "/kubejs"
        self.configs_path = self.path + "/config"
        self.defaultconfigs_path = self.path + "/defaultconfigs"

    def __init__(self) -> None:
        if (SYSTEM_PATHS == {}):
            get_system_paths()
        self.path = SYSTEM_PATHS["instance"]
        self.kubejs_path = self.path + "/kubejs"
        self.configs_path = self.path + "/config"
        self.defaultconfigs_path = self.path + "/defaultconfigs"

    def __str__(self) -> str:
        return f"Instance path: {self.path}\nKubeJS path: {self.kubejs_path}\nConfigs path: {self.configs_path}"


def hard_copy(from_path: str, to_path: str) -> None:
    """Copy files from the from_path to the to_path, overwriting all files."""
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)
    print(f"Copying files from {from_path} to {to_path} (overwriting all files).")


def soft_copy(from_path: str, to_path: str) -> None:
    """Copy files from the from_path to the to_path, only overwriting files that exist in the from_path."""
    if (os.path.exists(to_path)):
        print(f"Copying files from {from_path} to {to_path}")
        shutil.copytree(from_path, to_path, dirs_exist_ok=True)
    else:
        print(f"Destination path {to_path} does not exist. Skipping copy.")


if __name__ == "__main__":
    print("This is a module, not a script.")
