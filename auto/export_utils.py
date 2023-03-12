import os
import tqdm
import shutil
import zipfile
import requests

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

    def __init__(self, system_var: str) -> None:
        if (SYSTEM_PATHS == {}):
            get_system_paths()
        self.path = SYSTEM_PATHS[system_var]
        if (self.path == ""):
            raise ValueError("System path not found.")

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
    print(
        f"Copying files from {from_path} to {to_path} (overwriting all files).")


def soft_copy(from_path: str, to_path: str) -> None:
    """Copy files from the from_path to the to_path, only overwriting files that exist in the from_path."""
    if not os.path.exists(to_path):
        print("Creating directory: " + to_path + " (does not exist).")
        os.mkdir(to_path)

    print(f"Copying files from {from_path} to {to_path}")
    shutil.copytree(from_path, to_path, dirs_exist_ok=True)


def download_file(url: str, download_location: str) -> None:
    """Downloads a file from the specified url while showing a progress bar."""
    # Uses tqdm and requests
    # https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    with open(download_location, 'wb') as file, tqdm.tqdm(
        total=total_size_in_bytes,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)


class DirectoryManager():

    def __init__(self, target_path: str):
        self.target_path = target_path
        self.current_path = os.getcwd()

    def change(self):
        os.chdir(self.target_path)

    def return_to_current(self):
        os.chdir(self.current_path)

    def execute(self, function):
        os.chdir(self.target_path)
        function()
        os.chdir(self.current_path)

    def delete(self, file_name: str) -> None:
        """Delete the specified file."""
        os.chdir(self.target_path)
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Deleted file: {file_name}")
        else:
            print(f"File not found: {file_name}")
        os.chdir(self.current_path)

    def package(self, file_name: str) -> None:
        """Zip the specified directory."""
        zf = zipfile.ZipFile(file_name, "w")
        for dirname, _, files in os.walk(self.target_path):
            print("Zipping directory: " + dirname)
            for filename in files:
                print("Zipping file: " + filename)
                zf.write(os.path.join(dirname, filename))
                print("Zipped file: " + filename)
            print("Zipped directory: " + dirname)
        zf.close()
        print("finished zipping")

if __name__ == "__main__":
    print("This is a module, not a script.")
