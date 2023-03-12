import export_utils as eu
from export_utils import MinecraftFolder, DirectoryManager
import subprocess as sp

FORGE_INSTALL_LINK = "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.5-36.2.39/forge-1.16.5-36.2.39-installer.jar"
STARTUP_SCRIPT = """
#!/bin/bash
java -Xms8G -Xmx8G -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 -XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 -XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=50 -XX:+AlwaysPreTouch -jar forge-1.16.5-36.2.39.jar nogui
"""
SERVER_PROPERTIES = """
level-type=terraforged
white-list=true
"""
CLIENT_SIDE_MODS = [
    "NekosEnchantedBooks-1.16-1.7.0.jar",
]

server: MinecraftFolder = MinecraftFolder("server")
instance: MinecraftFolder = MinecraftFolder("instance")
directory: DirectoryManager = DirectoryManager(server.path)


def copy_mods() -> None:
    """Copy the mods folder from the server to the instance."""
    eu.soft_copy(instance.path + "/mods", server.path + "/mods")


def install_forge_server() -> None:
    print("Installing forge server...")
    eu.download_file(FORGE_INSTALL_LINK, server.path + "/forge-installer.jar")

    directory.execute(lambda: sp.call(
        ["java", "-jar", server.path + "/forge-installer.jar", "--installServer"]))

    print("Cleaning up...")
    directory.delete("forge-installer.jar")
    directory.delete("forge-installer.jar.log")

    print("Agreeing to EULA...")
    with open(server.path + "/eula.txt", "w") as eula_file:
        eula_file.write("eula=true")
    print("Finished agreeing to EULA.")

    print("Setting up server.properties...")
    with open(server.path + "/server.properties", "w") as server_properties_file:
        server_properties_file.write(SERVER_PROPERTIES)
    print("Finished setting up server.properties.")

    print("Creating startup script...")
    with open(server.path + "/start.sh", "w") as startup_file:
        startup_file.write(STARTUP_SCRIPT)
    print("Finished creating startup script.")

    print("Making startup script executable...")
    directory.execute(lambda: sp.call(
        ["chmod", "+x", server.path + "/start.sh"]))
    print("Finished making startup script executable.")

    print("Finished setting up forge server.")


def configuration_setup() -> None:
    print("Copying configuration files...")
    eu.hard_copy("config", server.path + "/config")
    eu.hard_copy("defaultconfigs", server.path + "/defaultconfigs")
    eu.hard_copy("kubejs", server.path + "/kubejs")
    print("Finished copying configuration files.")


def move_mods() -> None:
    """Move the mods folder from the instance to the server."""
    eu.soft_copy(instance.path + "/mods", server.path + "/mods")
    print("Removing client side mods...")
    for mod in CLIENT_SIDE_MODS:
        directory.delete("mods/" + mod)
    print("Finished removing client side mods.")


if __name__ == "__main__":
    print("Exporting to server...")
    install_forge_server()
    configuration_setup()
    move_mods()
