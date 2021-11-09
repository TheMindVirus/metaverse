#Metaverse Search Protocol
import os, sys, random

filename = None
filelist = []
pathlist = dict()

commands = \
[
    "search", "search-nonstrict", "search-strict",
    "reload", "cross", "help"
]

def search(term, datum, _ = None):
    return term.lower() in datum.lower()

def search2(term, datum, strict = False):
    score = 0
    longer = term if len(term) > len(datum) else datum
    for c in longer:
        if c.lower() in longer.lower():
            score += 1
    return score > strict

def help2():
    sys.stdout.write("Commands: " + ", ".join(i for i in commands) + "\n")

def reload():
    global filename, filelist, pathlist
    filename = os.path.basename(__file__)
    filelist = []
    pathlist = dict()
    for root, directories, files in os.walk(os.getcwd()):
        for file in files:
            if file != filename:
                name, ext = os.path.splitext(file)
                if ext.lower() == ".png":
                    rel = os.path.relpath(root)
                    filelist.append(name)
                    pathlist[name] = os.path.join(rel, name)

reload()

first_run = True

while True:
    sys.stdout.write("Metaverse Search Protocol\n")
    if first_run:
        help2()
        first_run = False
    sys.stderr.write(">>> ")
    args = input().split()
    command = args[0].lower()
    term = " ".join(args[1:])
    if command == "search":
        for file in filelist:
            if search(term, file):
                spaces = (" " * (24 - len(file))) + "\t"
                sys.stderr.write(file + spaces + pathlist[file] + "\n")
        sys.stderr.write("\n")
    elif command == "search-nonstrict":
        for file in filelist:
            if search2(term, file, False):
                spaces = (" " * (24 - len(file))) + "\t"
                sys.stderr.write(file + spaces + pathlist[file] + "\n")
        sys.stderr.write("\n")
    elif command == "search-strict":
        for file in filelist:
            if search2(term, file, True):
                spaces = (" " * (24 - len(file))) + "\t"
                sys.stderr.write(file + spaces + pathlist[file] + "\n")
        sys.stderr.write("\n")
    elif command == "reload":
        sys.stderr.write("Reloading...\n")
        reload()
    elif command == "cross":
        a = random.randrange(0, len(filelist))
        b = random.randrange(0, len(filelist))
        sys.stderr.write(filelist[a] + " x " + filelist[b] + "\n")
    elif command == "help":
        help2()
    else:
        sys.stderr.write("Unknown Command\n")
        help2()

"""

The Metaverse Is:

* A Collection of Global Industries Working Together to Provide for the World
* A Digital Twin of the Communities and Services that Make & Consume Things
* A Subset of the Internet for Virtual Reality and Open Multiplayer Experiences
* A Set of Distributed Servers Providing Quick Access Links to High Quality Items
* A Set of Virtual Object Creation Tools to aid Rapid Development for Everyone
* A Crossing of Worlds where Multiple Universes Collide and Unite for Innovation
* An Optional Internet Root Domain Name (e.g. xbox.net or facebook.meta + .com)
* An Artificial Intelligence capable of Orchestrating this Big Data Workload
* The Cloud??? But a heavily evolved, really good Cloud...

Crossover Examples:

* Lego x IKEA = ~~LEGOKEA~~ Lego Furniture
* Hornby x Warhammer = ~~Hornhammer~~ Space Marine Train Transport
* NASA x SpaceX = ~~LittleNASX~~ Crew Dragon Rocket and Starlink
* Behringer x Yamaha = ~~Behaha~~ ~~Yamringer~~ DS-80 (CS-80 Synth Restoration)
* Mercedes x AMG = Very Fast Car
* Mercedes x AMG x AMD x Formula 1 = Even Faster Very Fast Car
* Lego x Raspberry Pi = Raspberry Pi Build HAT & SPIKE Prime Set
* Lego x ARM = Mindstorms, NXT, EV3, Boost, Powered Up, Robot Inventor Kit
* Lego x ARM x National Instruments = Mindstorms NXT doing Scientific Datalogging
* ARM x Texas Instruments = BeagleBone Black, Predecessor to Raspberry Pi
* Raspberry Pi x Pimoroni = HyperPixel4 Display HAT (and a lot of others unsung)
* Raspberry Pi x Adafruit = Macropad RP2040 with CircuitPython

"""
