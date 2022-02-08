"""
Assignment 3: Editor
CMPUT 175 
Author: Zayd Biberdorf
"""

import shlex


class argumentLengthError(Exception):
    "raised when there is an invalid number of arguments"

    def __init__(self, userInput):
        self.message = print("%s: incorrect number of arguments" % (userInput))
        super().__init__(self.message)


class lineOutOfRangeError(Exception):
    "raised when there is an invalid number of arguments"

    def __init__(self, userInput):
        self.message = "%s: incorrect number of arguments" % (userInput)
        super().__init__(self.message)


class DLinkedListNode:
    def __init__(self, initData, initNext, initPrevious):
        self.data = initData
        self.next = initNext
        self.previous = initPrevious

        if initPrevious != None:
            initPrevious.next = self
        if initNext != None:
            initNext.previous = self

    def __str__(self):
        return "%s" % (self.data)

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def getPrevious(self):
        return self.previous

    def setData(self, newData):
        self.data = newData

    def setNext(self, newNext):
        self.next = newNext

    def setPrevious(self, newPrevious):
        self.previous = newPrevious


class DLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        s = "[ "
        current = self.head
        while current != None:
            s += "%s " % (current)
            current = current.getNext()
        s += "]"
        return s

    def isEmpty(self):
        return self.size == 0

    def length(self):
        return self.size

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found

    def index(self, item):
        current = self.head
        found = False
        index = 0
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
                index = index + 1
        if not found:
            index = -1
        return index

    def add(self, item):
        temp = DLinkedListNode(item, self.head, None)
        if self.head != None:
            self.head.setPrevious(temp)
        else:
            self.tail = temp
        self.head = temp
        self.size += 1

    def append(self, item):
        temp = DLinkedListNode(item, None, None)
        if self.head == None:
            self.head = temp
        else:
            self.tail.setNext(temp)
            temp.setPrevious(self.tail)
        self.tail = temp
        self.size += 1

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
        if current.getNext() != None:
            current.getNext().setPrevious(previous)
        else:
            self.tail = previous
        self.size -= 1

    def removeitem(self, current):
        previous = current.getPrevious()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
        if current.getNext() != None:
            current.getNext().setPrevious(previous)
        else:
            self.tail = previous
        if previous:
            self.curr = previous.getNext()
        else:
            self.curr = None
        self.size -= 1

    def insert(self, current, item, where):

        if current == None:
            newNode = DLinkedListNode(item, current, current)
            current = newNode
        elif where == 0:
            newNode = DLinkedListNode(item, current, current.getPrevious())
            current.setPrevious(newNode)
        else:
            newNode = DLinkedListNode(item, current.getNext(), current)
            current.setNext(newNode)
        self.size += 1


class TextFile:
    def __init__(self, fname):
        self.fname = fname
        self.current = None
        self.line = 1
        self.LinkedList = DLinkedList()

    def load(self, name):
        # read in text
        if not self.LinkedList.isEmpty():
            for i in range(self.LinkedList.length()):
                self.LinkedList.removeitem(self.LinkedList.getHead())
        self.fname = name
        file = open(name, "r")
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip("\n")
            newNode = DLinkedListNode(lines[i], None, None)
            self.LinkedList.append(newNode)

        self.current = self.LinkedList.getTail()
        self.line = self.LinkedList.length()

        print("%s (%d)" % (self.fname, self.LinkedList.length()))

    def write(self, name):
        # write out files text
        file = open(name, "w")
        current = self.LinkedList.getHead()
        for i in range(self.LinkedList.length()):
            if i == self.LinkedList.length():
                file.writelines(str(current.getData()))
            else:
                file.writelines(str(current.getData()) + "\n")
            current = current.getNext()

    def print(self, offset):
        # print line(s), with offset indicating the number of lines before or after the current line to be printed.

        if offset < 0:
            temp = abs(offset)
            offset = self.line
            if temp > offset:
                self.line = 1
                self.current = self.LinkedList.getHead()
            else:
                for i in range(temp):
                    self.current = self.current.getPrevious()
                    self.line -= 1

        elif offset + self.line > self.LinkedList.length():
            offset = self.LinkedList.length()
        else:
            offset = offset + self.line

        while self.line != offset:
            print("  %s: %s" % (self.line, self.current))
            self.current = self.current.getNext()
            self.line += 1

        print("  %s: %s" % (self.line, self.current))

    def linenum(self, lineno):
        # set the current line to be the one at line #
        assert lineno <= self.LinkedList.length() and lineno > 0, lineOutOfRangeError(
            lineno
        )

        if lineno < self.line:
            for i in range(self.line - lineno):
                self.line -= 1
                self.current = self.current.getPrevious()
        else:
            for i in range(lineno - self.line):
                self.line += 1
                self.current = self.current.getNext()

    def add(self, where):
        # where is “insert” (before) or “add” (after) the current line
        runLoop = True
        while runLoop:
            linesToBeAdded = input()
            if linesToBeAdded == "":
                runLoop = False
            else:
                if self.current != None:
                    self.LinkedList.insert(self.current, linesToBeAdded, where)
                    if where == 1:
                        self.current = self.current.getNext()
                    self.line += 1
                else:
                    self.current = DLinkedListNode(linesToBeAdded, None, None)
                    self.LinkedList.add(self.current)

        if where == 0:
            self.current = self.current.getPrevious()
            self.line -= 1

    def delete(self, offset):
        # delete line(s), with offset indicating the number of lines before or after the current line to be deleted
        if offset < 0:
            temp = abs(offset)
            offset = self.line
            if temp > offset:
                self.line = 1
                self.current = self.LinkedList.getHead()
            else:
                for i in range(temp):
                    self.current = self.current.getPrevious()
                    self.line -= 1

        elif offset + self.line > self.LinkedList.length():
            offset = self.LinkedList.length()
        else:
            offset = offset + self.line

        count = self.line

        while count != offset:
            nextNode = self.current.getNext()
            self.LinkedList.removeitem(self.current)
            self.current = nextNode
            count += 1

    def search(self, text, where):
        # where is to look “before” or “after” the current line

        if where == 0:
            startingLineNum = self.line + 1
            while self.line != startingLineNum:
                if text in str(self.current.getData()):
                    return print("%s: %s" % (self.line, self.current))
                else:
                    if self.current.getPrevious() == None:
                        self.current = self.LinkedList.getTail()
                        self.line = self.LinkedList.length()
                    else:
                        self.current = self.current.getPrevious()
                        self.line -= 1

            if text in str(self.current.getData()):
                return print("%s: %s" % (self.line, self.current))
            else:
                self.linenum(startingLineNum - 1)
        else:
            startingLineNum = self.line - 1
            while self.line != startingLineNum:
                if text in str(self.current.getData()):
                    return print("%s: %s" % (self.line, self.current))
                else:
                    if self.current.getNext() == None:
                        self.current = self.LinkedList.getHead()
                        self.line = 1
                    else:
                        self.current = self.current.getNext()
                        self.line += 1

            if text in str(self.current.getData()):
                return print("%s: %s" % (self.line, self.current))
            else:
                self.linenum(startingLineNum + 1)

    def replace(self, text1, text2):
        # in the current line, replace “text1” with “text2”, if possible
        if text1 in str(self.current.getData()):
            self.current.setData(str(self.current.getData()).replace(text1, text2))

    def sort(self):
        # sort the entire file
        LinkedListData = []
        current = self.LinkedList.getHead()
        for i in range(self.LinkedList.length()):
            LinkedListData.append(str(current.getData()))
            current = current.getNext()

        LinkedListData = sorted(LinkedListData)
        self.LinkedList = DLinkedList()
        for i in LinkedListData:
            newNode = DLinkedListNode(i, None, None)
            self.LinkedList.append(newNode)

    def getName(self):
        # get the name of the file
        return self.fname

    def setName(self, fname):
        # set the name of the file
        self.fname = fname

    def getCurr(self):
        # get the current line
        return self.current

    def setCurr(self):
        # set the current line
        pass

    def getLine(self):
        # get the line # of the current line.
        return self.line

    def setLine(self, line):
        # set the line # of the current line
        assert line <= self.LinkedList.length() and line > 0, lineOutOfRangeError(line)
        self.line = line


def main():
    """
    This function will handle user input and exicute the program accordingly
    input: N/A
    output: N/A
    """
    quit = False
    textFileSaved = False

    print("Welcome to ed379")
    textFile = TextFile("defult.txt")
    while not quit:
        userInput = input(">")
        userInput = shlex.split(userInput)
        try:
            if "/" in userInput:
                assert len(userInput) == 2, argumentLengthError(userInput)
                textFile.search(userInput[1], 1)
            elif "?" in userInput:
                assert len(userInput) == 2, argumentLengthError(userInput)
                textFile.search(userInput[1], 0)
            elif "l" in userInput:
                assert len(userInput) == 2, argumentLengthError(userInput)
                textFileSaved = True
                textFile.load(userInput[1])
            elif "p" in userInput:
                assert len(userInput) <= 2, argumentLengthError(userInput)

                if len(userInput) > 1:
                    textFile.print(int(userInput[1]))
                else:
                    print("  %s: %s" % (textFile.getLine(), textFile.getCurr()))
            elif "a" in userInput:
                assert len(userInput) == 1, argumentLengthError(userInput)
                textFileSaved = False
                textFile.add(1)
            elif "i" in userInput:
                assert len(userInput) == 1, argumentLengthError(userInput)
                textFileSaved = False
                textFile.add(0)
            elif "d" in userInput:
                assert len(userInput) >= 1 and len(userInput) <= 2, argumentLengthError(
                    userInput
                )
                textFileSaved = False
                if len(userInput) == 1:
                    textFile.delete(1)
                else:
                    textFile.delete(int(userInput[1]))
            elif "q" in userInput:
                assert len(userInput) == 1, argumentLengthError(userInput)
                if textFileSaved == False:
                    wantToSave = input("Would you like to save before quiting? (Y, N)")
                    if wantToSave.lower() == "y":
                        textFile.write(textFile.getName())
                        print("Your text has been saved")
                        print("Good-bye")
                else:
                    print("Good-bye")
                quit = True
            elif "r" in userInput:
                assert len(userInput) <= 3, argumentLengthError(userInput)
                textFileSaved = False
                if len(userInput) == 3:

                    textFile.replace(userInput[1], userInput[2])
                else:

                    textFile.replace(userInput[1], "")
            elif "w" in userInput:
                assert len(userInput) <= 2, argumentLengthError(userInput)
                textFileSaved = True
                if len(userInput) == 2:
                    textFile.write(userInput[1])
                else:
                    textFile.write(textFile.getName())
            elif "s" in userInput:
                assert len(userInput) == 1
                textFileSaved = False
                textFile.sort()
            elif len(userInput) == 1:
                textFile.linenum(int(userInput[0]))
            elif len(userInput) == 0:
                textFile.linenum(textFile.getLine() + 1)
                print("  %s: %s" % (textFile.getLine(), textFile.getCurr()))

        except AssertionError as error:
            print(error)
        except argumentLengthError as error:
            print(error)
        except FileNotFoundError:
            print("%s: File not found" % (userInput[1]))
        except lineOutOfRangeError as error:
            print(error)
        except ValueError as error:
            print(error)


main()
