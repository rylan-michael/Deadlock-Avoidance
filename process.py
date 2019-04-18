import operator


class Process:
    """Provides conveniences for operations on processes."""
    # Each process has 2 lists tracking the state of our resource-
    # allocation system. The 'Allocation' list tracks the number of
    # resources of each type currently allocated to the process.
    # The 'Max' list tracks the maximum demand of the process.
    def __init__(self, allocation, max_request):
        self.allocation = allocation
        self.max = max_request
        self.need = self.calculate_need()

    def calculate_need(self):
        return list(map(operator.sub, self.max, self.allocation))

    def __repr__(self):
        formatted_output = f"A:{self.allocation} M:{self.max} N:{self.need}\t" 
        return formatted_output


def le(list_a, list_b):
    return all(map(operator.le, list_a, list_b))

def add(list_a, list_b):
    return list(map(operator.add, list_a, list_b))

def sub(list_a, list_b):
    return list(map(operator.sub, list_a, list_b))
