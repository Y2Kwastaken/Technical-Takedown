import export_utils as eu
from export_utils import DirectoryManager

if __name__ == "__main__":
    print("Packaging server...")    
    eu.get_system_paths()
    server: str = eu.SYSTEM_PATHS["server"]
    directory: DirectoryManager = DirectoryManager(server)
    directory.package("server.zip")
