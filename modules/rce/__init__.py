from .exec import get_available_attacks as get_available_exec_attacks
from .module_load import get_available_attacks as get_available_module_load_attacks



AVAILABLE_ATTACKS = [
    { "exec": get_available_exec_attacks() },
    { "module_load": get_available_module_load_attacks() }
]



def exec_help():
    return "\nUse this attack module to perform a variety of attacks resulting in\n" \
    "command execution. Currently available exec attack techniques are:\n\n" \
    "- webshell\n" \
    "- ssh\n" \
    "- crontab\n" \
    "\n[*] Preconditions:\n" \
    "Ability to run the following commands:\n" \
    "- CONFIG SET\n" \
    "- CONFIG GET (not mandatory but good to have)\n" \
    "- SAVE\n" \
    "- FLUSHALL/FLUSHDB (not mandatory but good to have)\n" \
    "- SET\n\n" \
    "You must also have the permissions to save the payload\n" \
    "to the .ssh/WEBROOT folder or the crontab file.\n" \
    "\nAll of the attack techniques leverage the RDB (dump) file\n" \
    "to implant the payload in the WEBROOT directory or\n" \
    ".ssh/authorized_keys file or the crontabs directory.\n" \
    "\n[NOTE] The crontab technique doesn't works in Debian machines!\n" \
    "\n[*] Outcome:\n" \
    "With this module, you can obtain a shell session on the\nRedis server machine.\n"



def module_load_help():
    return "\nUse this attack module to perform attack to load a malicious Redis module.\n" \
    "Currently this module contains one attack technique:\n\n" \
    "- load_malicious_module\n" \
    "\n[*] Preconditions:\n" \
    "1. You have a Redis module uploaded on the Redis server host.\n" \
    "2. The uploaded module has execute permissions.\n" \
    "3. Redis server (the privileges with which it is running) has\n" \
    "permissions to access the uploaded module.\n\n" \
    "[NOTE] If a module with the same name already exists on the\n" \
    "target Redis server, the current action is to unload that module\n" \
    "and load the supplied module. Only reason being that if you are\n" \
    "running this attack, then we assume that you wish to load the module\n" \
    "(and it is not currently loaded or is updated).\n" \
    "\n[*] Outcome:\n" \
    "With this module, you can load a malicious Redis module that supports\n" \
    "commands to run OS commands and to obtain reverse & bind shells.\n"