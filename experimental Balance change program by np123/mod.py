import copy
import json
import os

def install():

    with open("config.json", "r") as f:
        config = json.load(f)


    backup = []

    if os.path.isfile("uninstall.json"):
        with open("uninstall.json", "r") as f:
            try:
                uninstall = json.load(f)
            except json.JSONDecodeError:
                uninstall = []
    else:
        uninstall = []

    print(uninstall)

    with open("uninstall.json", "w") as f:
        with open(os.path.join(os.path.dirname(os.getcwd()), "Stronghold_Crusader_Extreme.exe"), "r+b") as shc:
            for cfg in config:
                shc.seek(0)
                shc.seek(int(cfg["address"], 16))
                if cfg["description"] not in [x["description"] for x in uninstall if type(x) == dict and "description" in x.keys()]:
                    uninstall.append(copy.deepcopy(cfg))
                    uninstall[-1]["value"] = hex(int.from_bytes(shc.read(cfg["size"]), byteorder='little'))
                    print(hex(int.from_bytes(shc.read(cfg["size"]), byteorder='little')))

            f.write(json.dumps(uninstall, indent=4))
                


            for cfg in config:
                shc.seek(0)
                shc.seek(int(cfg["address"], 16))
                shc.write(int(cfg["value"]).to_bytes(int(cfg["size"]), byteorder='little'))


def uninstall():
    if os.path.isfile("uninstall.json"):
        with open("uninstall.json", "r") as f:
            try:
                uninstall = json.load(f)
            except json.JSONDecodeError:
                return
            
            with open(os.path.join(os.path.dirname(os.getcwd()), "Stronghold_Crusader_Extreme.exe"), "r+b") as shc:
                for cfg in uninstall:
                    shc.seek(0)
                    shc.seek(int(cfg["address"], 16))
                    shc.write(int(cfg["value"], 16).to_bytes(int(cfg["size"]), byteorder='little'))

    os.remove("uninstall.json")




if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall()
    else:
        install()
