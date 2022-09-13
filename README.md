# opccsvserver
serves up OPC using tags and values from contents of a csv file, at one second intervals, more or less

messy code needs a tidy but does what I need for now

csv file format:
tag, value

example use 
./opccsvserver 0.0.0.0 4840 -f ../asim006_chuditch/data/CALCsmVar.txt

./opccsvserver 0.0.0.0 4840 -m -f ../asim006_chuditch/data/csvfilelist.txt

the -m option is for multiple so then the filename points to a file with contents of a list of csv files so it can serve up multiple files

Note: it serves everything as a string, it's just easier that way, convert to int or whatever at the other end.

Based on minimal server from opcasync, but had to do some trickery (for me anyway) involving
converting strings to tags and getting asych problems

Needs to be killed to stop, ctrl-c will leave a process behind that hogs the port

main.py = source
opccsvserver = compiled by pyinstaller for ubuntu 22.04

Its handy, but use at yoiur peril

