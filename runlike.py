import subprocess

with open("containerIDs", "r") as file:
    IDs = file.read().split("\n")

IDs = [ID for ID in IDs if ID]

for ID in IDs:
    print(ID)

    with open(f"containerCommands/{ID}", "w") as file:
        subprocess.run(["runlike", ID], stdout=file)
