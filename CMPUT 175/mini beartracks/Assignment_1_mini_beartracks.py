# ----------------------------------------------------
# assignment one: beartracks simulator
# Purpose of code: This will be a simplified version of UofA's BearTracks registration system.
# you will be able to read information about student, add and drop classes and be able to view current time tables
# Author: Zayd Biberdorf
# Collaborators/references:
# ----------------------------------------------------

from os import access, close, sep, times
import time


def mainMenu():
    """
    This function will prompt the user to select an option from a menu of options, if the selection does not match
    one of the options then the user will be notifyed and be prompted to select again

    input: N/A

    output: userInput [str]
    """
    print(
        "1. Print timetable",
        "2. Enroll in course",
        "3. Drop course",
        "4. Quit",
        sep="\n",
    )
    userInput = input("> ")
    while userInput not in ["1", "2", "3", "4"]:
        print("Sorry, invalid entry. Please enter a choice from 1 to 4. ")
        userInput = input("> ")

    return userInput


def getStudentInfo(studentId):
    """
    this funtion turns the student info text file into a dictionary and will validate student id

    input: studentId [str]

    output: studentInfo [list]
    """

    studentInfo = {}
    studentInfoTxtFile = open("students.txt")
    for student in studentInfoTxtFile:
        values = student.split(sep=",")
        studentInfo[values[0]] = [values[1], values[2].strip("\n")]

    if studentId in studentInfo.keys():
        return studentInfo[studentId]


def getCourseList():
    courseTxtFile = open("courses.txt")
    courseList = []
    for course in courseTxtFile:
        course = course.split(sep=";")
        course[3] = course[3].strip("\n")
        course[1] = course[1][1:]
        course[2] = course[2].strip()
        courseList.append(course)

    courseTxtFile.close()
    return courseList


def getStudentClasses(studentId):
    """
    this function will retreave the classes that a specific student is enrolled in

    input: studentId [str]

    output: classes [list]
    """
    classDetails = []
    studentsClasses = []
    enrollmentTextFile = open("enrollment.txt")

    for studentClass in enrollmentTextFile:
        enrollmentDetails = studentClass.split(sep=":")
        enrollmentDetails[1] = enrollmentDetails[1].strip("\n")
        enrollmentDetails[1] = enrollmentDetails[1].strip()
        if enrollmentDetails[1] == studentId:
            studentsClasses.append(enrollmentDetails[0])

    for aClass in getCourseList():
        if aClass[0] in studentsClasses:
            classDetails.append(aClass)

    enrollmentTextFile.close()
    return classDetails


def getValidStudentId():
    """
    this function will ask for a user id and check to see if it is a valid student ID

    input: N/A

    output: studentId [str]
    """
    studentId = input("\nStudent ID: ")
    if isinstance(getStudentInfo(studentId), list):
        return studentId
    else:
        return "error"


def printTimetable():
    """
    this funtion will prompt the user to enter a student ID, it will then check to see if its a valid ID
    using validateStudentId, will print the students time table and display their name and what faculty they are in

    input: N/A

    output: N/A

    """
    studentId = getValidStudentId()
    studentInfo = getStudentInfo(studentId)
    if studentId == "error":
        print("Invalid student ID. Cannot print timetable \n")
    else:
        print(
            "Time table for %s, in the faculty of %s" % (studentInfo[1], studentInfo[0])
        )
        print(
            "%s Mon %s Tues %s Wed %s Thu %s Fri"
            % (" " * 9, " " * 6, " " * 6, " " * 6, " " * 6)
        )

        classes = getStudentClasses(studentId)
        seporator = " " * 6 + "+" + ("-" * 10 + "+") * 5

        # populating the times list in timetablecontent, this list holds all the times that are to be used in the time table
        timetableContent = {
            "times": [],
            "mon": [],
            "tues": [],
            "wed": [],
            "thu": [],
            "fri": [],
        }
        hours = 8
        minutes = "00"
        for i in range(18):
            timetableContent["times"].append(str(hours) + ":" + str(minutes))
            minutes = int(minutes)
            minutes += 30
            if minutes >= 60:
                hours += 1
                minutes = "00"
            for i in range(2):
                timetableContent["times"].append(" " * 5)

        # populating the time table content list, this list will contain all the content for the time table,
        # ie. spces, comma breaks, class informaton

        for i in range(1, 54):
            if i % 6 == 0 and i != 18 and i != 36:
                MWF = "|" + "-" * 10
                TT = "|" + " " * 10
                ending = "|"

            elif i % 18 == 0:
                MWF = "+" + "-" * 10
                TT = "+" + "-" * 10
                ending = "+"
            elif i % 9 == 0:
                MWF = "|" + " " * 10
                TT = "|" + "-" * 10
                ending = "|"
            else:
                MWF = "|" + " " * 10
                TT = "|" + " " * 10
                ending = "|"

            timetableContent["mon"].append(MWF)
            timetableContent["tues"].append(TT)
            timetableContent["wed"].append(MWF)
            timetableContent["thu"].append(TT)
            timetableContent["fri"].append(MWF + ending)

        for aClass in classes:
            classTime = aClass[1].split(" ")
            newTextindex = timetableContent["times"].index(classTime[1])
            if len(aClass[0]) == 8:
                classNameSpacing = "| "
            else:
                classNameSpacing = "|"

            if len(aClass[2]) == 4:
                classNumSpacingLeft = "|   "
                classNumSpacingRight = "   "
            elif len(aClass[2]) == 3:
                classNumSpacingLeft = "|   "
                classNumSpacingRight = "    "
            elif len(aClass[2]) == 2:
                classNumSpacingLeft = "|    "
                classNumSpacingRight = "    "
            else:
                classNumSpacingLeft = "|     "
                classNumSpacingRight = "    "

            if classTime[0] == "MWF":

                timetableContent["mon"][newTextindex] = (
                    classNameSpacing + aClass[0] + " "
                )
                timetableContent["wed"][newTextindex] = (
                    classNameSpacing + aClass[0] + " "
                )
                timetableContent["fri"][newTextindex] = (
                    classNameSpacing + aClass[0] + " | "
                )
                timetableContent["mon"][newTextindex + 1] = (
                    classNumSpacingLeft + aClass[2] + classNumSpacingRight
                )
                timetableContent["wed"][newTextindex + 1] = (
                    classNumSpacingLeft + aClass[2] + classNumSpacingRight
                )
                timetableContent["fri"][newTextindex + 1] = (
                    classNumSpacingLeft + aClass[2] + classNumSpacingRight + "|"
                )
            else:
                timetableContent["tues"][newTextindex] = (
                    classNameSpacing + aClass[0] + " "
                )
                timetableContent["thu"][newTextindex] = (
                    classNameSpacing + aClass[0] + " "
                )
                timetableContent["tues"][newTextindex + 1] = (
                    classNumSpacingLeft + aClass[2] + classNumSpacingRight
                )
                timetableContent["thu"][newTextindex + 1] = (
                    classNumSpacingLeft + aClass[2] + classNumSpacingRight
                )

        index = 0
        print(seporator)
        for i in range(53):
            if timetableContent["times"][index][0] not in ["8", "9"]:
                printableTime = timetableContent["times"][index]
            else:
                printableTime = " " + timetableContent["times"][index]

            print(
                "%s %s%s%s%s%s"
                % (
                    printableTime,
                    timetableContent["mon"][index],
                    timetableContent["tues"][index],
                    timetableContent["wed"][index],
                    timetableContent["thu"][index],
                    timetableContent["fri"][index],
                )
            )

            index += 1
        print(seporator)


def enroll():
    """
    This function will get the user id, and a course the that the user would like to enroll in,
    this function will check to see if the class is full and if the user is alrady enrolled in either that class
    or a class with the same given time.

    input: N/A

    output: N/A
    """
    studentId = getValidStudentId()
    studentClasses = getStudentClasses(studentId)
    updateInfo = True
    if studentId == "error":
        print("Invalid student ID. Cannot continue with course enrollment.")
    else:
        # ask user to enter a course
        selectedCourse = input("Course name:").upper()
        courseList = getCourseList()

        if (
            True not in [selectedCourse == course[0] for course in courseList]
            or selectedCourse == ""
        ):
            print("Invalid course name.")
            updateInfo = False

        for course in courseList:
            for aClass in studentClasses:
                if selectedCourse == course[0] and course[1] == aClass[1]:
                    print(
                        "Schedule conflict: already registered for course on %s"
                        % (course[1])
                    )
                    updateInfo = False

            if int(course[2]) <= 0:
                print(
                    "Cannot enroll. %s is already at capacity. Please contact advisor to get on waiting list."
                    % (selectedCourse)
                )
                updateInfo = False

        if updateInfo:
            enrollmentTxtFile = open("enrollment.txt", "a")
            coursesTxtFile = open("courses.txt", "w")
            enrollmentTxtFile.write("\n%s: %s" % (selectedCourse, studentId))
            enrollmentTxtFile.close()
            print(
                "%s has successfully been enrolled in %s, on TR 8:00"
                % (getStudentInfo(studentId)[1].strip(), selectedCourse)
            )
            for course in courseList:
                if course[0] == selectedCourse:
                    course[2] = str(int(course[2]) - 1)
                coursesTxtFile.write(
                    "%s; %s; %s;%s \n" % (course[0], course[1], course[2], course[3])
                )
            coursesTxtFile.close()

            # subtract the number from the thing waka waka poop fart dfjalsjdfla;kjdf;lasdjkf;lasjkf;lsdafk;lsadf


def dropClass():
    """
    This funtion will promp the user to ender a student id then let them drop a class of their choice.

    input: N/A

    output: N/A
    """

    studentId = getValidStudentId()
    studentClasses = getStudentClasses(studentId)
    studentInfo = getStudentInfo(studentId)

    if studentId == "error":
        print("invalid student ID \n")

    else:
        print("select a class you would like to drop: ")
        for aClass in studentClasses:
            print("- %s" % (aClass[0]))
        classToDrop = input("> ").upper()
        if True not in [classToDrop == aClass[0] for aClass in studentClasses]:
            print(
                "Drop failed. %s is not currently registered in %s."
                % (studentInfo[1], classToDrop)
            )
        else:
            enrollmentTxtFile = open("enrollment.txt", "r")
            enrollmentLines = enrollmentTxtFile.readlines()
            enrollmentTxtFile.close()
            enrollmentTxtFileW = open("enrollment.txt", "w")
            for line in enrollmentLines:
                if classToDrop not in line:
                    enrollmentTxtFileW.write(line)
            print(
                "%s Soleiman has successfully dropped %s"
                % (studentInfo[1], classToDrop)
            )


def main():

    print("=" * 26, "Welcome to Mini-BearTracks", "=" * 26, sep="\n")

    quit = False
    while not quit:
        action = mainMenu()

        if action == "1":
            printTimetable()
        if action == "2":
            enroll()
        if action == "3":
            dropClass()
        if action == "4":
            quit = True


main()
