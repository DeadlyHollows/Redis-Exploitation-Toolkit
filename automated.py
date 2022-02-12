import json
from time import sleep

from common import get_launch_attack_sequence, launch_exploit
from config.settings import VERBOSE, INTER_ATTACK_DELAY, \
        ATTACK_DEPENDENCY_FILE

from helper.utils import nostdout, read_file
from modules import get_automated_attack_sequence


# A mapping of the attack sequence executed
EXECUTED_ATTACK_SEQUENCES = set()



def attack_sequence_not_executed(attack_sequence):

    if attack_sequence in EXECUTED_ATTACK_SEQUENCES:
        # Attack sequence was already executed.
        return False

    return True



def mark_attack_sequence_executed(attack_sequence):

    global EXECUTED_ATTACK_SEQUENCES
    EXECUTED_ATTACK_SEQUENCES.add(attack_sequence)



def display_attack_sequence(attack_sequence, tab_count = 0):

    for attack in attack_sequence:

        if isinstance(attack, str):
            print("    " * tab_count + "-> " + attack)
            if isinstance(attack_sequence, dict):
                display_attack_sequence(attack_sequence[attack], tab_count + 1)
                print()

        else:
            display_attack_sequence(attack, tab_count)



def execute_attack_sequence(attack_module_path, available_attacks):

    for attack in available_attacks:

        if isinstance(attack, str):
            if isinstance(available_attacks, dict):
                execute_attack_sequence(attack_module_path + [attack],
                        available_attacks[attack])

            else:
                attack_function_path = attack_module_path + [attack]

                sleep(INTER_ATTACK_DELAY)

                dependency_sequence = json.loads(read_file(ATTACK_DEPENDENCY_FILE))
                launch_attack_sequence = get_launch_attack_sequence(
                        attack_function_path, dependency_sequence)

                for attack_sequence in launch_attack_sequence:

                    # If attack is not executed, we execute the attack,
                    # keeping it's stdout intact.
                    # Otherwise, we set a dummy studout to avoid any output
                    # traces of the precondition attack - to prevent any noise
                    # TODO?: Since connections would be cached, we can keep the
                    # re-execution to a minimum by executing until we get both
                    # true and false possibilities
                    # That way, we can prevent execution of certain attack paths.
                    if not VERBOSE and not attack_sequence_not_executed(attack_sequence):
                        # Nothing sent to stdout
                        with nostdout():
                            execution_success_status = launch_exploit(attack_sequence.split("/"))

                    else:
                        execution_success_status = launch_exploit(attack_sequence.split("/"))

                    if str(execution_success_status) == launch_attack_sequence[attack_sequence] \
                            or launch_attack_sequence[attack_sequence].upper() == "ANY":
                        # Mark the sequence as executed
                        mark_attack_sequence_executed(attack_sequence)

                    else:
                        # If the status differs, we won't execute any further attacks!
                        break

                print("[", "=" * 75 , "]\n")

        else:
            execute_attack_sequence(attack_module_path, attack)



def launch_in_automated_mode():

    # It's the JSON specified in config.settings
    # The attack sequence file is stored in 'AUTOMATED_ATTACK_SEQUENCE'
    attack_sequence = get_automated_attack_sequence()

    print("\n[*] Attack Sequence")
    display_attack_sequence(attack_sequence)

    sleep(1)

    print("\n[INFO] Press CTRL+C to skip an attack.")
    print("[INFO] Press CTRL+D to stop the tool.\n")

    for attack_module in attack_sequence:
        execute_attack_sequence([attack_module], attack_sequence[attack_module])



if __name__ == "__main__":
    launch_in_automated_mode()