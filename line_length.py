import argparse
import glob


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def terminal_size():
    import fcntl
    import termios
    import struct
    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0, 0)))
    return tw, th


def getArgs():
    parser = argparse.ArgumentParser(description='Files to parse.')
    parser.add_argument('strings', metavar='str', type=str, nargs='+',
                        help='regex to parse.')
    args = parser.parse_args()
    return args.strings


def getFiles(strings):
    accum = []
    for string in strings:
        accum += glob.iglob(string)
    return accum


def readFile(file):
    t = []
    with open(file, 'r') as fp:
        counter = 0
        for line in fp:
            counter += 1
            if len(line) > 80:
                t.append((counter, len(line)))
    return t


def readFiles(files):
    t = []
    for file in files:
        t.append((file, readFile(file)))
    return t


def printErrors(t):
    print(chr(27) + "[2J")
    width, height = terminal_size()
    padding = 18
    prints_per_line = width // padding
    if t:
        for (file, errors) in t:
            if errors:
                print(bcolors.FAIL + f'\n------{file}------' + bcolors.ENDC)
            else:
                print(bcolors.OKBLUE + f'No errors in {file}' + bcolors.ENDC)
            accum = ''
            for count, (line, length) in enumerate(errors):
                accum += f'line:{line} is {length}'.ljust(padding, ' ')
                if (count + 1) % prints_per_line == 0:
                    accum += '\n'
            if accum:
                print(accum + '\n')
    else:
        print(bcolors.FAIL + f'No files matched' + bcolors.ENDC)


def main():
    files = getFiles(getArgs())
    printErrors(readFiles(files))


if __name__ == '__main__':
    main()
