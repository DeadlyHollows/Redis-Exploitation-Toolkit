import contextlib
import io
import sys
import subprocess
from config import settings



def execute_command(command):

    print(f"\n[*] Executing `{' '.join(command)}`\n")

    command = ["timeout", str(settings.EXEC_TIMEOUT)] + command

    process = subprocess.Popen(command, stdout = subprocess.PIPE)

    try:
        for line in iter(process.stdout.readline, ""):
            if not line:
                break
            print(line.decode("utf-8"), end = "")

    except KeyboardInterrupt as e:
        # Stop this command!
        process.kill()



def execute_command_with_output(command):

    try:
        return subprocess.check_output(command, shell = True)
    except subprocess.CalledProcessError as e:
        return b""



def execute_redis_command(*command):

    from .connection import get_cached_db_connection

    redis = get_cached_db_connection()
    return redis.execute_command(*command)



def read_file(fname, strip = True):

    fp = open(fname, "r")
    data = fp.read()
    fp.close()

    if strip:
        data = data.strip()

    return data



def write_file(fname, data):

    fp = open(fname, "w")
    fp.write(data.strip())
    fp.close()



def print_kv_pairs(kv_pairs, label = "", tab_count = 0):

    if label:
        print(f"\n[*] {label}\n")
        label = ""

    for key in kv_pairs:

        tabs = tab_count * "\t"

        if isinstance(kv_pairs[key], dict):
            print(f"{tabs}{key}:")
            print_kv_pairs(kv_pairs[key], tab_count = 1)
            print("")

        else:
            print(f"{tabs}{key} => {kv_pairs[key]}")



def decode_bytes_kv_pair(bytes_kv_pair):

    str_kv_pair = {}

    for key in bytes_kv_pair.keys():

        _key = key
        _value = bytes_kv_pair.get(key)

        if isinstance(key, bytes):
            _key = _key.decode("ascii")

        if isinstance(_value, bytes):
            _value = _value.decode("ascii")

        str_kv_pair[_key] = _value

    return str_kv_pair



def get_tool_banner():

    from config.settings import TOOL_BANNER_FILE
    return read_file(TOOL_BANNER_FILE, strip = False)



def strip_quotes_from_entries(entries):

    modified_entries = []

    for entry in entries:
        modified_entries.append(entry.replace("'", "")
                        .replace('"', ""))

    return modified_entries



def get_assume_defaults_value():

    from config.settings import ASSUME_DEFAULTS
    return ASSUME_DEFAULTS



@contextlib.contextmanager
def nostdout():

    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout