from typing import List


class Input:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.content = None
        self.lines = None

    def read(self) -> str:
        with open(self.file_name) as f:
            self.content = f.read()
        return self.content

    def read_lines(self) -> List[str]:
        if (self.content is None):
            self.read()

        if (self.lines is None):
            self.lines = self.content.split("\n")
        return self.lines
