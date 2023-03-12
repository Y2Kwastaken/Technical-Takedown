import export_utils as eu
from export_utils import MinecraftFolder

instance: MinecraftFolder = MinecraftFolder()

if __name__ == "__main__":
    to_export: str = input("What to export [all, kubejs, config]: ")
    kubejs: bool = False
    config: bool = False
    
    if(to_export == "all"):
        kubejs = True
        config = True
    elif(to_export == "kubejs"):
        kubejs = True
    elif(to_export == "config"):
        config = True
    else:
        print("Invalid input. Exiting.")

    if(kubejs):
        eu.hard_copy("kubejs", instance.kubejs_path)
    if(config):
        eu.soft_copy("config", instance.configs_path)
        eu.soft_copy("defaultconfigs", instance.defaultconfigs_path)

