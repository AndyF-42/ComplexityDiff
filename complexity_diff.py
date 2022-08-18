# Author: Andy Fleischer
# Date: 8/17/2022
# Summary: Takes in two complexity text files and returns a summary of the differences.
# Usage: "python complexity_diff.py {old file} {new file} {output file (optional)}"


import sys


def main(args):
    # Get lines from the files
    old_file = open(args[0], 'r')
    new_file = open(args[1], 'r')
    files = [old_file.readlines(), new_file.readlines()]
    old_file.close()
    new_file.close()

    complexities = {}

    for arg, _file in enumerate(files):
        # Find starting line for scores
        start = ([pos + 1 for pos, line in enumerate(_file) if line[0:5] == "Score"] + [-1])[0]
        if start == -1:
            quit(f"Failed to find \"Score\" in {args[arg]}")
        
        # Map all the complexities and their changes
        for line in _file[start:-1]:
            line = line.strip().split()
            line[3] = line[3].split("(")[0]
            if (line[3], line[4]) in complexities:
                old_complexity = complexities[(line[3], line[4])][0]
                complexities[(line[3], line[4])] = (old_complexity, int(line[0]), "increased" if int(line[0]) - old_complexity > 0 else "decreased")
            else:
                if arg == 1:
                    complexities[(line[3], line[4])] = (-1, int(line[0]), "new")
                else:
                    complexities[(line[3], line[4])] = (int(line[0]), -1, "old")
    
    # Sorting
    sorted_complexities = sorted(complexities.items(), key=lambda kv: kv[1][1], reverse=True)

    # Compiling output
    padding = max([len(line[0][0] + " " + line[0][1]) for line in sorted_complexities])
    
    output = ""
    for func in sorted_complexities:
        if func[1][2] == "new" or func[1][2] == "old":
            output += f"{func[0][0]} {func[0][1]} {'.' * (padding - len(func[0][0] + func[0][1]))} Only present in {func[1][2]}, complexity {max(func[1][0], func[1][1])}\n"
        elif func[1][0] == func[1][1]:
            output += f"{func[0][0]} {func[0][1]} {'.' * (padding - len(func[0][0] + func[0][1]))} Complexity unchanged at {func[1][0]}\n"
        else:
            output += f"{func[0][0]} {func[0][1]} {'.' * (padding - len(func[0][0] + func[0][1]))} Complexity {func[1][2]} from {func[1][0]} to {func[1][1]}\n"

    # Printing and writing to file
    print(output.strip())
    if len(args) == 3:
        with open(args[2], 'w') as out:
            out.write(output)


if __name__ == "__main__":
    if len(sys.argv) > 4:
        quit("Too many arguments")
    main(sys.argv[1::])