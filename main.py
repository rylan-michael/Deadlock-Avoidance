import argparse
from process import Process, le, add, sub


def parse_file(filename):
    """Parses text file and extracts system process information.
    Params:
        filename: name of the text file inluding the extension.
    Returns:
        process_list: list of process objects.
        available: list of available resource-type intances.
    """
    raw_data_set = {"Allocation": [], "Max": []}
    available_resources = []
    process_list = []

    f = open(filename, "r")
    header = ""
    for line in f:
        line = line.rstrip()
        if ("Process" not in line) and (not line[0].isdigit()):
            header = line
        if line is not header:
            # Classify process lists into the following categories.
            if header == "Allocation":
                # Strip 'Process #: ' from string.
                isolated_resources = line[11:].split()
                resource_instance_count = [int(r) for r in isolated_resources]
                raw_data_set["Allocation"].append(resource_instance_count)
            elif header == "Max":
                isolated_resources = line[11:].split()
                resource_instance_count = [int(r) for r in isolated_resources]
                raw_data_set["Max"].append(resource_instance_count)
            elif header == "Available":
                isolated_resources = line.split()
                available_resources = [int(r) for r in isolated_resources]
    process_list = [p for p in map(Process, raw_data_set["Allocation"],
                                   raw_data_set["Max"])]
    return process_list, available_resources


def is_safe(process_list, available_resources):
    """Implements the safety portion of the Banker's algorithmn.

    The Banker's algorithm for deadlock-avoidance (pg.331). Determines whether
    the system ends up in a safe-state given a list of processes and the sys-
    tem's available resources.
    Returns:
        is_safe: boolean specifying whether system is safe.
    """
    work = available_resources
    finish = [False for i in range(len(process_list))]

    # Worst-case performance m*n^2 operations. *n = len(finish)*
    for _ in range(len(work) * (len(finish)**2)):
        for i in range(len(process_list)):
            process = process_list[i]
            if not finish[i] and le(process.need, work):
                work = add(work, process.allocation)
                finish[i] = True
            elif False not in finish:
                return True
    return False


def request_resource(process_list, available, request):
    """Determines whether request can safely be granted."""
    process = process_list[0]  # Assuming request for P0.
    if not le(request, process.need):
        print("Process has exceeded its maximum claim.")
        return False
    if le(request, available):
        available = sub(available, request)
        process.allocation = add(process.allocation, request)
        process.need = sub(process.need, request)
        process_list[0] = process
        if is_safe(process_list, available):
            return True
    return False


def take_user_input(process_list, available):
    print("If you'd like to exit reading input for this file at"
          + " anytime, enter 'c'.")
    while True:
        try:
            p_input = input("Please enter a request vector (e.g. 1 0 0): ")
            if p_input == "c":
                return
            parsed_request = [int(r) for r in p_input.split()]
            if len(parsed_request) != len(available):
                raise IOError

            if request_resource(process_list, available, parsed_request):
                print("GRANTED")
            else:
                print("NOT GRANTED")
        except ValueError:
            print("ERROR: Please enter a request without trailing"
                      + " spaces.")
        except IOError:
            print("ERROR: Please enter a request with proper length.")

def main():
    # Setup user-friendly interface for command-line arguments.
    parser = argparse.ArgumentParser(description="Processes the request " +
                                     "vector from a specified text file.")
    parser.add_argument("filename", type=str, help="include extension")
    args = parser.parse_args()
    process_list, available_resources = parse_file(args.filename)

    if is_safe(process_list, available_resources):
        print("SAFE")
    else:
        print("NOT SAFE")

    take_user_input(process_list, available_resources)


main()
