#!/usr/bin/env python3
#********************************************************************************
# DynoSprite - scripts/build-level.py
# Copyright (c) 2013, Richard Goedeken
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#********************************************************************************

import json
import os
import re
import sys
from compression import *

class ObjectInit:
    def __init__(self):
        self.params = { }
        self.params["groupid"] = None
        self.params["objectid"] = None
        self.params["active"] = None
        self.params["globalx"] = None
        self.params["globaly"] = None
        self.params["initdata"] = None
    def Validate(self):
        for key in self.params:
            if self.params[key] == None:
                print(f"****Error: Object init section missing parameter '{key}'")
                return False
        return True
    def SetParameter(self, key, value, dynosymbols):
        if key == "initdata":
            initList = value
            numList = []
            for initValue in initList:
                if type(initValue) is int:
                    numList.append(initValue)
                elif initValue in dynosymbols:
                    symLoc = dynosymbols[initValue]
                    numList.append(symLoc >> 8)
                    numList.append(symLoc & 255)
                else:
                    print(f"****Error: unknown symbol '{initValue}' in object initialization list")
                    sys.exit(1)
            self.params["initdata"] = numList
            return
        # everything else is an integer
        self.params[key] = int(value)
        return
    def WriteDataStream(self):
        output = bytes((self.params["groupid"], self.params["objectid"], self.params["active"]))
        globalX = self.params["globalx"]
        output += bytes((globalX >> 8, globalX & 0xff))
        globalY = self.params["globaly"]
        output += bytes((globalY >> 8, globalY & 0xff))
        for byteval in self.params["initdata"]:
            output += bytes((byteval,))
        return output

class Level:
    def __init__(self, number):
        self.LvlNumber = number
        self.Symbols = None             # input
        self.RawCode = None             # input
        self.CompCode = None            # DEFLATEd object code
        self.CompMap = None             # DEFLATEd tilemap
        self.ParamDict = { }            # from parsing
        self.ObjectGroups = None        # from parsing
        self.ObjectInitStream = b''     # from parsing
        self.NumInitObjects = 0
        self.cc3Data = b''              # output
        self.tilemap = b''
        self.tilemapwidth = 0
        self.tilemapheight = 0

    def validateCode(self, listFile):
        if not 'Level_Initialize' in self.Symbols:
            print(f"****Error: Missing 'Level_Initialize' function in level file '{listFile}'")
            sys.exit(1)
        if not 'Level_CalculateBkgrndNewXY' in self.Symbols:
            print(f"****Error: Missing 'Level_CalculateBkgrndNewXY' function in level file '{listFile}'")
            sys.exit(1)

    def validateParameters(self, descFile):
        paramList = [ "name", "description", "objectgroups", "maxobjecttablesize", "tileset", "tilemapsize", "bkgrndstartx", "bkgrndstarty" ]
        for paramName in paramList:
            if not paramName in self.ParamDict:
                print(f"****Error: Missing '{paramName}' parameter in level file '{descFile}'")
                sys.exit(1)
        # parse the ObjectGroups parameter to make a list
        self.ObjectGroups = [s for s in self.ParamDict["objectgroups"]]
        # set the width and height from tilemapsize
        self.tilemapwidth, self.tilemapheight = (v//16 for v in self.ParamDict["tilemapsize"])

    def parseDescription(self, descFilename, dynosymbols):
        with open(descFilename) as f:
            data = json.load(f)

        # First set the level section
        for key, value in data["Level"].items():
            if key != "_comment":
                self.ParamDict[key.lower()] = value

        # Fill out object section
        for obj in data["Objects"]:
            curObject = ObjectInit()
            for key, value in obj.items():
                if key != "_comment":
                    curObject.SetParameter(key.lower(), value, dynosymbols)
            if not curObject.Validate():
                print(f"****Error: in level description file '{descFilename}'")
                sys.exit(1)
            self.ObjectInitStream += curObject.WriteDataStream()
            self.NumInitObjects += 1

    def parseMap(self, mapFilename):
        f = open(mapFilename).read()
        for line in f.split("\n"):
            # remove comments and whitespace from line
            pivot = line.find("*")
            if pivot != -1:
                line = line[:pivot]
            line = line.strip()
            if len(line) < 1:
                continue
            # handle tile index values (hex)
            tiles = "".join(line.split())
            if (len(tiles) & 1) == 1:
                print(f"****Error: invalid tilemap line length ({int(len(tiles))}) in map file '{mapFilename}'")
                sys.exit(1)
            for i in range(0, len(tiles), 2):
                v = int(tiles[i:i+2], 16)
                self.tilemap += bytes((v,))
            continue
        # validate tilemap length
        if len(self.tilemap) != lvl.tilemapwidth * lvl.tilemapheight:
            print(f"****Error: tilemap length ({int(len(self.tilemap))}) in file '{mapFilename}' doesn't match width and height given in level descriptor file")
            sys.exit(1)

    def generateData(self):
        # level directory
        self.cc3Data += outputWord(len(self.ObjectInitStream))
        self.cc3Data += outputWord(len(self.RawCode))
        self.cc3Data += outputWord(len(self.CompCode))
        self.cc3Data += outputWord(len(self.CompMap))
        self.cc3Data += outputWord(self.Symbols["Level_Initialize"])
        self.cc3Data += outputWord(self.Symbols["Level_CalculateBkgrndNewXY"])
        # data blocks
        self.cc3Data += self.ObjectInitStream
        self.cc3Data += self.CompCode
        self.cc3Data += self.CompMap

def outputWord(value):
    hi = (value >> 8) & 0xff
    lo = value & 0xff
    return bytes((hi, lo))

def SymbolExtract(listName):
    # parse input list and extract all global symbols
    bFoundSymTable = False
    SymDict = { }
    f = open(listName).read()
    for line in f.split("\n"):
        line = line.strip()
        # look for symbol table
        if not bFoundSymTable:
            if line == "Symbol Table:":
                bFoundSymTable = True
            continue
        # check this symbol
        if len(line) > 40 and line[0:4] == '[ G]' and line.find(".") == -1 and line.find("{") == -1:
            symdef = line[5:].split()
            SymDict[symdef[0]] = int(symdef[1], 16)

    if bFoundSymTable:
        return SymDict

    symbol_parser = re.compile('^Symbol: ([^ ]+) ([^ ]+) = ([0-9A-F]+)$')
    for line in f.split("\n"):
        line = line.strip()
        # look for symbol table
        if not bFoundSymTable:
            if line == "Symbol:":
                bFoundSymTable = True

        if not line.startswith('Symbol: '):
            continue

        # check this symbol
        match = symbol_parser.match(line)
        SymDict[match.group(1)] = int(match.group(3), 16)

    return SymDict

def StringOut(inString):
    delimiters = "'\"`~_/|"
    for char in delimiters:
        if inString.find(char) == -1:
            return char + inString + char
    print(f"This is a bad string: {inString}")
    sys.exit(1)

#******************************************************************************
# main function for standard script execution
#

if __name__ == "__main__":
    print("DynoSprite Level Builder script")
    # get input paths
    if len(sys.argv) != 8:
        print(f"****Usage: {sys.argv[0]} <in_level_folder> <dynosprite-pass1.lst> <in_gfx_folder> <in_raw_folder> <in_list_folder> <out_cc3_folder> <out_asm_folder>")
        sys.exit(1)
    leveldir = sys.argv[1]
    dynolist = sys.argv[2]
    gfxdir = sys.argv[3]
    rawdir = sys.argv[4]
    listdir = sys.argv[5]
    cc3dir = sys.argv[6]
    asmdir = sys.argv[7]
    # make lists of level files (description, raw/list from asm source, tilemap) found
    filelist = os.listdir(leveldir)
    lvlDescFiles = [name for name in filelist if len(name) >= 6 and name[:2].isdigit() and name[-5:].lower() == ".json"]
    lvlDescFiles.sort()
    rawlist = os.listdir(rawdir)
    listlist = os.listdir(listdir)
    lvlRawFiles = [name for name in rawlist if len(name) >= 11 and name[:5] == "level" and name[5:7].isdigit() and name[-4:].lower() == ".raw"]
    lvlRawFiles.sort()
    lvlListFiles = [name for name in listlist if len(name) >= 11 and name[:5] == "level" and name[5:7].isdigit() and name[-4:].lower() == ".lst"]
    lvlListFiles.sort()
    gfxlist = os.listdir(gfxdir)
    print(gfxlist)
    lvlMapFiles = [name for name in gfxlist if len(name) >= 13 and name[:7] == "tilemap" and name[7:9].isdigit() and name[-4:].lower() == ".txt"]
    lvlMapFiles.sort()
    # make sure we have same # of files in each list
    numLevels = len(lvlDescFiles)
    if len(lvlMapFiles) != numLevels or len(lvlRawFiles) != numLevels or len(lvlListFiles) != numLevels:
        print(f"****Error: Mismatched level description/assembly/map files in '{leveldir}' and/or '{rawdir}'")
        print(f"  {int(len(lvlMapFiles))} map files found, {int(numLevels)} expected")
        print(f"  {int(len(lvlRawFiles))} raw files found, {int(numLevels)} expected")
        print(f"  {int(len(lvlListFiles))} list files found, {int(numLevels)} expected")
        sys.exit(1)
    print(f"    Found {int(numLevels)} levels")
    # get symbol locations for DynoSprite engine
    dynosymbols = SymbolExtract(dynolist)
    # parse input files and create levels
    allLevels = [ ]
    for i in range(numLevels):
        lvlNum = int(lvlDescFiles[i][:2])
        if int(lvlMapFiles[i][7:9]) != lvlNum or int(lvlRawFiles[i][5:7]) != lvlNum or int(lvlListFiles[i][5:7]) != lvlNum:
            print(f"****Error: mis-matched level description/assembly/map files in '{leveldir}' and/or '{rawdir}' with number {int(lvlNum)}")
            sys.exit(1)
        lvl = Level(lvlNum)
        lvl.Symbols = SymbolExtract(os.path.join(listdir, lvlListFiles[i]))
        lvl.RawCode = open(os.path.join(rawdir, lvlRawFiles[i]), "rb").read()
        comp = Compressor(lvl.RawCode)
        lvl.CompCode = comp.Deflate(bPrintInfo=False, bUseGzip=True)
        lvl.validateCode(lvlListFiles[i])
        lvl.parseDescription(os.path.join(leveldir, lvlDescFiles[i]), dynosymbols)
        lvl.validateParameters(lvlDescFiles[i])
        lvl.parseMap(os.path.join(gfxdir, lvlMapFiles[i]))
        comp = Compressor(lvl.tilemap)
        lvl.CompMap = comp.Deflate(bPrintInfo=False, bUseGzip=True)
        lvl.generateData()
        allLevels.append(lvl)
    # write out the data file
    f = open(os.path.join(cc3dir, "LEVELS.DAT"), "wb")
    for lvl in allLevels:
        f.write(lvl.cc3Data)
    f.close()
    # write level directory table to include in DynoSprite core
    f = open(os.path.join(asmdir, "gamedir-levels.asm"), "w")
    f.write("Gamedir_Levels\n")
    s = str(len(allLevels))
    f.write(f"{' ' * 24}fcb     {s}{' ' * (16 - len(s))}* total number of levels\n")
    for lvl in allLevels:
        f.write(f"{' ' * 24}* Level {lvl.LvlNumber}: {lvl.ParamDict['name']}\n")
        s = str(lvl.LvlNumber)
        f.write(f"{' ' * 24}fcb     {s}{' ' * (16 - len(s))}* Level number\n")
        s = f"Level{int(lvl.LvlNumber):02}Name"
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* Pointer to level name\n")
        s = f"Level{int(lvl.LvlNumber):02}Desc"
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* Pointer to level description\n")
        s = str(len(lvl.cc3Data))
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* Level size on disk in bytes\n")
        s = str(len(lvl.ObjectGroups))
        f.write(f"{' ' * 24}fcb     {s}{' ' * (16 - len(s))}* number of object groups to load with level\n")
        s = f"Level{int(lvl.LvlNumber):02}Groups"
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* pointer to group number list to load\n")
        s = str(int(lvl.ParamDict["maxobjecttablesize"]))
        f.write(f"{' ' * 24}fcb     {s}{' ' * (16 - len(s))}* Maximum number of objects in Current Object Table\n")
        s = str(lvl.NumInitObjects)
        f.write(f"{' ' * 24}fcb     {s}{' ' * (16 - len(s))}* number of objects to initialize from Init Stream\n")
        s = str(int(lvl.ParamDict["tileset"]))
        f.write(f"{' ' * 24}fcb     {s}{' ' * (16 - len(s))}* tileset number to load\n")
        s = str(lvl.tilemapwidth)
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* width of background tilemap\n")
        s = str(lvl.tilemapheight)
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* height of background tilemap\n")
        s = str(int(lvl.ParamDict["bkgrndstartx"]))
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* background tilemap starting position X\n")
        s = str(int(lvl.ParamDict["bkgrndstarty"]))
        f.write(f"{' ' * 24}fdb     {s}{' ' * (16 - len(s))}* background tilemap starting position Y\n")
    for lvl in allLevels:
        f.write(f"{'Level%02iName             fcn     ' % lvl.LvlNumber + StringOut(lvl.ParamDict['name'])}\n")
        f.write(f"{'Level%02iDesc             fcn     ' % lvl.LvlNumber + StringOut(lvl.ParamDict['description'])}\n")
        f.write(f"{'Level%02iGroups           fcb     ' % lvl.LvlNumber + ','.join([str(og) for og in lvl.ObjectGroups])}\n")
    f.close()


