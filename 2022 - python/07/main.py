from __future__ import annotations
import math

class File:
    def __init__(self, size: int, parent: File | None, name: str, is_dir = False):
        self.size = size
        self.name = name
        self.parent = parent
        self.total_size = 0
        self.path = (self.parent.path if self.parent is not None else "") + name
        self.children = []
        if self.parent is not None:
            self.parent.children.append(self)
        self.is_dir = is_dir

    def get_size(self) -> int:
        self.total_size = self.size + sum([c.get_size() for c in self.children])
        return self.total_size

class Parser:
    cmd = "$ "
    cmd_cd = "cd"
    cmd_list = "ls"

    cd_back = ".."
    cd_root = "/"
    
    ls_dir = "dir"


    def __init__(self):
        self.current_path: list[str] = ["/"]
        self.files = {"/": File(0,None, "/", True)}

    def parse(self, output):
        # split by cmd
        # split first line by space, get command and arguments
        # rest are outputs
        chunks = output.split(Parser.cmd)
        chunks = [x.strip() for x in chunks if x]

        for chunk in chunks:
            lines = [line.strip() for line in chunk.split("\n")]
            cmd_line = lines.pop(0)
            cmd = cmd_line.split(" ")
            if cmd[0] == Parser.cmd_cd:
                self.cd(cmd[1])
            elif cmd[0] == Parser.cmd_list:
                self.ls(lines)
    
    def cd(self, argument: str):
        if argument == Parser.cd_back:
            self.current_path.pop()
        elif argument == Parser.cd_root:
            self.current_path = ["/"]
        else:
            self.current_path.append(argument.strip() + "/")


    def ls(self, lines):
        for line in lines:
            root_path = "".join(self.current_path)

            [size, filename] = line.split(" ")

            file_name = filename + "/"
            
            path = root_path + file_name
            is_dir = False
            if size == Parser.ls_dir:
                is_dir = True
                size = 0
            self.files.setdefault(path, File(int(size), self.files[root_path] if root_path in self.files else None, file_name, is_dir))
        

with open("C:\\Users\\kasutaja7yh\\Desktop\\aoc-2022\\07\\input.txt") as input:
    parser = Parser()
    parser.parse(input.read())

    for file_name in parser.files:
        file = parser.files[file_name]
        file.get_size()


    sum_dir = 0
    for file_name in parser.files:
        file = parser.files[file_name]
          
        if file.is_dir and file.total_size <= 100000:
            sum_dir += file.total_size

    print(sum_dir)

    # part 2
    total_size = 70000000
    required_size = 30000000
    used_size = parser.files["/"].total_size

    free_space = total_size - used_size
    delta = required_size - free_space

    closest_size = math.inf
    for file_name in parser.files:
        file = parser.files[file_name]
          
        if file.is_dir and file.total_size >= delta and file.total_size < closest_size:
            closest_size = file.total_size
    
    print("closest", closest_size)
