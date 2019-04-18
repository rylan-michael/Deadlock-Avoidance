import pandas as pd
import operator
import random


def read_file(filename):
    """Parses txt file and extracts process information.
    Returns:
        df: DataFrame of the process request matrix.
        available_resources: a single list of available resources.
    """
    data_set = {"Allocation": [], "Max": []}
    available_resources = []
    f = open(filename, "r")
    header = ""
    for x in f:
        x = x.rstrip()
        if ("Process" not in x) and (not x[0].isdigit()):
            header = x

        if x is not header:
            if header == "Allocation":
                # Remove 'Process #: ' from string
                resources = x[11:].split()
                process = [int(x) for x in resources]
                data_set["Allocation"].append(process)
            elif header == "Max":
                resources = x[11:].split()
                process = [int(x) for x in resources]
                data_set["Max"].append(process)
            elif header == "Available":
                resources = x.split()
                process = [int(x) for x in resources]
                available_resources = process

    df = pd.DataFrame(data=data_set)
    return df, available_resources


def is_safe(process_request_matrix, available_resources):
    """Determines whether the system can safely grant resources to processes.
    Params:
        process_request_matrix: DataFrame of all process resources.
        available_resources: Array of the system's available reosuorces.
    """
    df, available = process_request_matrix, available_resources
    need = []
    # Additional unpacking generalizations --
    # https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-448
    for i in range(len(df)):
        try:
            allocation = df["Allocation"][i]
            max_resources = df["Max"][i]
            # Check if the process is trying to request too many resources.
            if any(map(operator.gt, allocation, max_resources)):
                raise Exception("Process is requesting more resources"
                                + " than can be provided by the system.")
            else:
                need.append(list(map(operator.sub, df["Max"][i],
                                     df["Allocation"][i])))
        except Exception:
            print("Process is requesting more resources"
                  + " than can be provided by the system.")
            return False

    work = available
    finish = [False for i in range(len(df))]

    iterations = 0
    while False in finish:
        for i in range(len(finish)):
            if not finish[i] and all(map(operator.le, need[i], work)):
                work = list(map(operator.add, work, df["Allocation"][i]))
                finish[i] = True
            else:
                if False not in finish:
                    return True
            iterations += 1
        if iterations > 1000:
            work = available
            terminated = []
            for i in range(1, len(finish)):
                need = list(map(operator.sub, df["Max"][0], df["Allocation"][0]))
                if all(map(operator.le, need, work)):
                    print(f"Processes {terminated} should be terminated to grant the requested resources.")
                else:
                    terminated.append(i)
                    work = list(map(operator.add, work, df["Allocation"][i]))
            print("There are no amount of process you could kill that would"
                  + " grant the resources your process requires.")
            return False


def display_header(filename):
    """Provides better user experience in the header prompts."""
    colors = ["\x1b[0;30;44m", "\x1b[0;30;47m", "\x1b[0;30;43m",
              "\x1b[0;30;46m"]
    filename_disp = random.choice(colors) + filename + "\x1b[0m"
    print("================================================================\n")
    print("Processing the Request maxtrix file: ", filename_disp)
    print("\n================================================================")


def takeUserInput(filename):
    display_header(filename)
    process_request_matrix, available_resources = read_file(filename)
    s_state = is_safe(process_request_matrix, available_resources)
    print("State after reading the file is: "
          + ("Safe" if s_state else "Not Safe"))
    print("If you'd like to exit reading input for this file at"
          + " anytime, enter 'c'.")
    if s_state:
        while True:
            try:
                process = input("Please enter a request vector: ")
                # Handle 'exit' user input
                if process == "c":
                    return
                parsed_request = [int(i) for i in process.split()]
                if len(parsed_request) != len(available_resources):
                    raise IOError

                # Add user request to Process 0.
                process_zero = process_request_matrix["Max"][0]
                print(process_zero)
                process_request_matrix["Max"][0] = [
                    *map(operator.add, process_zero, parsed_request)]
                is_s_safe = is_safe(process_request_matrix,
                                    available_resources)
                if is_s_safe:
                    print("Safe")
                else:
                    process_request_matrix["Max"][0] = process_zero
                    print("Not Granted, Max for Process 0 has been"
                          + " reverted.")
            except ValueError:
                print("\t ERROR: Please enter a request without trailing"
                      + " spaces.")
            except IOError:
                print("\t ERROR: Please enter a request with proper length.")
    else:
        print("Unable to take user requests because the input file has left"
              + " the system in an unsafe state.")


takeUserInput("sys_config.txt")
# takeUserInput("sys_config 2.txt")
# takeUserInput("sys_config_task3.txt")
