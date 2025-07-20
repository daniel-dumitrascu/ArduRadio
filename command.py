class Command:
    def __init__(self, command: str, input: str):
        self.command = command
        self.fragments = self.split(command)
        self.input = input

    def split(self, command: str) -> list[str]:
        fragments = []
        start, end, last = None, None, 0
        pattern = "\\'"

        idx = command.find(pattern, 0)
        while idx != -1:
            if start is None:
                start = idx+2
                splits = command[last:idx].split()
                fragments += splits
            elif end is None:
                end = idx
                last = idx+2
                fragments.append(command[start:end])
                start, end = None, None
            idx = command.find(pattern, idx+2)

        # don't forget about the last fragments
        if last < len(command):
            fragments += command[last:len(command)].split()

        return fragments