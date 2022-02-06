from .common import get_attack_help_message, proceed_with_cached_connection


AVAILABLE_ATTACKS = [
    "load_malicious_module"
]



def module_load_help():
    return "\nUse this sub-module to load a malicious\n" \
    "Redis module on the target server. The Redis module\n" \
    "must be present on the server and must have execute\n"\
    "permissions.\n"



def perform_module_load_attack(attack_name, redis):

    if attack_name not in AVAILABLE_ATTACKS:
        print("\n[-]Invalid attack name specified!\n")
        return False

    # getattr(import_module(f".{attack_name}", "modules.module_load"), attack_name)()
    return getattr(locals[attack_name])(redis)



def load_malicious_module_help():
    return get_attack_help_message("load_malicious_module")

def load_malicious_module(redis):
    from .load_malicious_module import load_malicious_module
    return load_malicious_module(redis)



def get_available_attacks():
    return AVAILABLE_ATTACKS



if __name__ == "__main__":
    redis = proceed_with_cached_connection()
    perform_module_load_attack(attack_name = "load_malicious_module")