from typing import Dict, List

from attrs import define


@define
class Directory:
    subdirs: Dict[str, 'Directory']
    files: Dict[str, int]
    _size: int = -1

    def get_rec_subdir(self, path_list: List[str]) -> 'Directory':
        if not path_list:
            return self
        else:
            return self.subdirs[path_list[0]].get_rec_subdir(path_list[1:])

    def extend_with(self, subdirnames: List[str], files: Dict[str, int]):
        self.files = files
        self.subdirs = {name: Directory({}, {}) for name in subdirnames}

    def size(self):
        if self._size == -1:
            self._size = sum((subdir.size() for subdir in self.subdirs.values())) + sum(self.files.values())
        return self._size

    def dir_iter(self):
        for subdir in self.subdirs.values():
            yield from subdir.dir_iter()
        yield self


@define
class IntermediateTerminalState:
    line_idx: int
    working_dir: List[str]

    def read_command(self, terminal_lines: List[str], root_dir: Directory):
        cmd = terminal_lines[self.line_idx].strip()
        assert(cmd[0] == '$')
        if cmd[2:4] == 'cd':
            the_dir = cmd[5:]
            if the_dir == '/':
                self.working_dir = []
            elif the_dir == '..':
                self.working_dir = self.working_dir[:-1]
            else:
                self.working_dir.append(the_dir)
            self.line_idx += 1
        elif cmd[2:4] == 'ls':
            self.line_idx += 1
            sub_dirs = []
            files = dict()
            while (self.line_idx < len(terminal_lines) and
                   terminal_lines[self.line_idx].strip() and
                   terminal_lines[self.line_idx][0] != '$'):
                output_line = terminal_lines[self.line_idx].strip()
                if output_line.startswith('dir'):
                    sub_dirs.append(output_line[4:])
                else:
                    size, name = tuple(output_line.split(' '))
                    files[name] = int(size)
                self.line_idx += 1
            cur_dir = root_dir.get_rec_subdir(self.working_dir)
            cur_dir.extend_with(sub_dirs, files)
        else:
            print(cmd[2:4])


def parse_terminal(root_dir: Directory, terminal: str):
    lines = terminal.split('\n')[:-1]
    state = IntermediateTerminalState(0, [])
    while state.line_idx < len(lines):
        state.read_command(lines, root_dir)


def main():
    with open('input/day07_input.txt') as f:
        terminal = ''.join(f.readlines())
    root_dir = Directory({}, {})
    parse_terminal(root_dir, terminal)

    print(sum((subdir.size() for subdir in root_dir.dir_iter() if subdir.size() < 100000)))
    total_space = 70000000
    required_space = 30000000
    taken_space = root_dir.size()
    unused_space = total_space - taken_space
    delete_at_least = required_space - unused_space
    print(min((subdir.size() for subdir in root_dir.dir_iter() if subdir.size() >= delete_at_least)))


if __name__ == '__main__':
    main()