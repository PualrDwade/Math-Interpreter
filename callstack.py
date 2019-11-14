from enum import Enum


class FrameType(Enum):
    PROGRAM = 'PROGRAM'
    PROCEDURE = 'PROCEDURE'


class Frame(object):
    def __init__(self, name: str, type: FrameType, nesting_level: int):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.enclosing_frame = None
        self.members = {}

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members[key]

    def get(self, key):
        return self.members.get(key)

    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type.value,
                name=self.name,
            )
        ]
        for name, val in self.members.items():
            lines.append(f'   {name:<20}: {val}')

        s = '\n'.join(lines)
        return s

    def __repr__(self):
        return self.__str__()


class CallStack(object):
    def __init__(self):
        self.__frames = []

    def push(self, frame: Frame):
        current_frame = self.peek()
        if current_frame is not None:
            frame.enclosing_frame = current_frame
            frame.nesting_level = current_frame.nesting_level + 1
        self.__frames.append(frame)

    def pop(self):
        self.__frames.pop()

    def peek(self):
        if len(self.__frames) is 0:
            return None
        return self.__frames[-1]

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self.__frames))
        s = f'CALL STACK\n{s}\n'
        return s

    def __repr__(self):
        return self.__str__()
