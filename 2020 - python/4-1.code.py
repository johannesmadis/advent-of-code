import re


class PassportValidator:
    def __init__(self, line):

        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        self.cid = None

        items = re.split("\s+", line)
        self.length = len(items)
        for item in items:
            matches = re.match("(.+):(.+)", item)
            key = matches[1]
            value = matches[2]
            setattr(self, key, value)

        self.validate()
        self.print()

    def validate(self):
        self.validate_byr()
        self.validate_iyr()
        self.validate_eyr()
        self.validate_hgt()
        self.validate_hcl()
        self.validate_ecl()
        self.validate_pid()

        self.is_valid = self.is_valid_byr and self.is_valid_iyr and self.is_valid_eyr and self.is_valid_hgt and self.is_valid_hcl and self.is_valid_ecl and self.is_valid_pid

    def validate_byr(self):
        self.is_valid_byr = self.byr != None and len(self.byr) == 4 and int(
            self.byr) >= 1920 and int(self.byr) <= 2002

    def validate_iyr(self):

        self.is_valid_iyr = self.iyr != None and len(self.iyr) == 4 and int(
            self.iyr) >= 2010 and int(self.iyr) <= 2020

    def validate_eyr(self):
        self.is_valid_eyr = self.eyr != None and len(self.eyr) == 4 and int(
            self.eyr) >= 2020 and int(self.eyr) <= 2030

    def validate_hgt(self):
        self.is_valid_hgt = False

        if (self.hgt != None):
            matches = re.match(r"(\d+)(.+)", self.hgt)
            if (matches != None):
                height = int(matches[1])
                units = matches[2]
                if (units == "cm"):
                    self.is_valid_hgt = height >= 150 and height <= 193
                elif (units == "in"):
                    self.is_valid_hgt = height >= 59 and height <= 76

    def validate_hcl(self):
        self.is_valid_hcl = False
        if (self.hcl != None):
            match = re.match(r"#[0-9a-fA-F]{6}", self.hcl)
            self.is_valid_hcl = match != None and len(self.hcl) == 7

    def validate_ecl(self):
        self.is_valid_ecl = False
        for allowed in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
            if (self.ecl == allowed):
                self.is_valid_ecl = True
                return

    def validate_pid(self):
        self.is_valid_pid = False

        if (self.pid != None):
            match = re.match(r"\d{9}", self.pid)
            self.is_valid_pid = match != None and len(self.pid) == 9

    def print(self):
        if (self.is_valid):
            print(self.byr, self.iyr, self.eyr, self.hgt,
                  self.hcl, self.ecl, "\t")


with open("4-1.input.txt") as f:
    content = f.read()
    passports_inputs = content.split("\n\n")
    i = 0
    print("Total passports: " + str(len(passports_inputs)))
    for passport_input in passports_inputs:
        passport = PassportValidator(passport_input)
        if (passport.is_valid == True):
            i += 1

    print(i)
    # validator = PassportValidator()
