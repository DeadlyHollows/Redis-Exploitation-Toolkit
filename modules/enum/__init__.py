from .acl import get_available_attacks as get_available_acl_attacks
from .auth import get_available_attacks as get_available_auth_attacks
from .keys import get_available_attacks as get_available_keys_attacks
from .misc import get_available_attacks as get_available_misc_attacks


AVAILABLE_ATTACKS = [
    { "auth": get_available_auth_attacks() },
    { "keys": get_available_keys_attacks() },
    { "acl": get_available_acl_attacks() },
    { "misc": get_available_misc_attacks() }
]



def acl_help():
    return "\nUnder this sub-module, we have the following ACL-related attacks currently available:\n\n" \
    "- retrieve_acl_entries: Retrieves the ACL entries from a connected Redis instance.\n\n" \
    "- crack_acl_password_hashes: Cracks the ACL password hashes retrieved from the ACL\nentries using JTR.\n\n" \
    "- retrieve_acl_logs: Retrieves the ACL logs. This information is valuable for both\n" \
    "Red- and Blue-teams! For instance, a Red-teamer can harvest usernames (helpful to\n" \
    "perform AUTH attacks) from these logs whereas a Blue teamer can find the bruteforce\n" \
    "attempts for a user from these logs.\n"



def auth_help():
    return "\nUnder this sub-module, we have the following AUTH-related attacks\ncurrently available:\n\n" \
    "- auth_existence_check: Checks if the Redis server requires authentication or\nis open for anyone to connect.\n\n" \
    "- crack_weak_auth: Performs a dictionary attack against the Redis server.\n" \



def keys_help():
    return "\nUnder this sub-module, we have the following KEYS-related attacks\ncurrently available:\n\n" \
    "- keys_enum: Performs key enumeration attack.\n\n" \
    "For the keys_enum attack, you can provide a KEYS_FILE file containing the\n" \
    "wordlist path for the parts of the keys. This file can be set in the\n" \
    "config/settings.py file as well.\n"



def misc_help():
    return "\nUnder this sub-module, we have the following miscellaneous attacks\ncurrently available:\n\n" \
    "- monitor_server_commands: This will run the MONITOR command and thus we\n" \
    "will get all the commands sent to the Redis server from the instance this\n" \
    "command is run.\n"