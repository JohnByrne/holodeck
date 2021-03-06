#!/usr/bin/python

class Holodeck:

    #DEBUG MODE
    debugmode = False

    #USE SQL
    import sqlite3
    #SELECT DATABASE
    conn = sqlite3.connect("./holodeckdb")#Change to absolute path to allow users to add to the same world together.
    db = conn.cursor()

    #CREATE TABLE
    emptydb = True
    try:
        db.execute("CREATE TABLE construct (id INTEGER PRIMARY KEY, parent_id INTEGER, snippet TEXT, description TEXT, nextroom INTEGER)")
        conn.commit()
    except:
        emptydb = False

    #GET TIME
    import time
    currtime = int(time.time())

    #ACTIONS AVAILABLE
    #look ___
    #describe ___
    #go ___
    #drop pin
    #look pin
    #look back

    #SET DEFAULTS
    room = 1 #location
    pin = 1 #bookmarked location
    #The pin can be dropped and pointed back to.
    roomsummary = ""

    #INITIAL MESSAGE ON STARTUP
    print ""
    print "#  #  ##  #     ##  ###  ####  ###  #  #   ======="
    print "#  # #  # #    #  # #  # #    #   # # #     | | |"
    print "#### #  # #    #  # #  # ###  #     ##       | |"
    print "#  # #  # #    #  # #  # #    #   # # #     | | |"
    print "#  #  ##  ####  ##  ###  ####  ###  #  #   ======="
    print ""
    print "This holodeck hosts a virtual world that can be explored and added to by anyone in town!"
    print ""
    print "The commands are 'look', 'describe', and 'go'."
    print ""
    print "[ Status: This program is still a work in progress. ]"
    print "[ For more info: https://tilde.town/~ne1/code.html  ]"
    print ""

    #Ask whether to print out the How To Play tutorial or not.
    trigger_tutor = raw_input("Would you like to look at How To Play?(y/n) ")
    print ""
    if trigger_tutor!="n" and trigger_tutor!="no":
        print("-- How To Play! --")
        print ""
        print "LOOK"
        print ""
        print "look"
        print "You can type 'look' to look at the room you're in. Which"
        print "basically just means printing out the room description."
        print ""
        print "look SOMETHING"
        print "Where SOMETHING is an exact fragment of the room description."
        print "If SOMETHING has a description, it will be printed. Otherwise,"
        print "it will say \"There's nothing there.\""
        print ""
        raw_input("--press enter--")
        print ""
        print "DESCRIBE"
        print ""
        print "describe SOMETHING"
        print "Where SOMETHING is an exact fragment of the room description."
        print "This will set the description of SOMETHING."
        print ""
        print "You cannot 'go' somewhere that hasn't been 'describe'd as"
        print "something you can 'look' at."
        print ""
        raw_input("--press enter--")
        print ""
        print "GO"
        print ""
        print "go SOMEWHERE"
        print "Where SOMEWHERE is an exact fragment of the room description -"
        print "one that has already had it's description set using 'describe'."
        print "This moves you from one 'room' to another."
        print "If you're the first one to enter a 'room', you will be asked"
        print "to describe the 'room', answering the question \"What do you see?\""
        print "which sets the 'room description'."
        print ""
        print "go back"
        print "This moves you one 'room' closer to the first 'room'."
        print ""
        raw_input("--press enter--")
        print ""
        print "PIN"
        print ""
        print "drop pin"
        print "This bookmarks a certain 'room' to refer to later."
        print ""
        print "pin"
        print "If you're the first person to enter a 'room', you will be asked to"
        print "describe the 'room'. Alternatively, if you've dropped a pin, you can"
        print "simply type 'pin' and 'go' will link to the pinned 'room'."
        print ""
        raw_input("--press enter--")
        print ""
        print "EXIT"
        print ""
        print "exit"
        print "This just exits the program."
        print ""
        print "Protip:"
        print "You can use 'l', 'd', and 'g' to refer to commands 'look', 'describe', and 'go'."
        print ""
        raw_input("--press enter--")
        print ""

    #START IN ROOM 1 EVERY TIME
    db.execute("SELECT * FROM construct WHERE id=1")
    results = db.fetchall()
    #for result in results:
    #    print result[3]#description
    if len(results)<1:
        roomsummary = raw_input("Describe the first room: ")
        db.execute("INSERT INTO construct (parent_id, snippet, description, nextroom) VALUES (?, ?, ?, ?)",(0,"",roomsummary,1))#nextroom points to itself
        conn.commit()
        room = db.lastrowid

    #print "Room is: "+str(room)

    print "Basics: [look|describe|go] followed by a fragment of the room description."
    print "Or 'go back'. Or 'exit'."

    commands = ""
    command = ""
    #commands = raw_input("> ")
    import sys#using sys.exit to exit.
    while True:
        db.execute("SELECT * FROM construct WHERE id=?",(str(room),))
        results = db.fetchall()
        for result in results:
            room = result[0]
            roomsummary = result[3]
            parent_id = result[1]
        print "\n"+roomsummary

        commands = raw_input("\nCommand: ")
        commands = commands.split(" ")
        command = commands[0]
        target = " ".join(commands[1:]).strip()
        if command=="look" or command=="l":
            if target in roomsummary:
                if len(target)>0:
                    db.execute("SELECT * FROM construct WHERE parent_id=? AND snippet=?",(str(room),target))
                    results = db.fetchall()
                    if len(results)>0:
                        for result in results:
                            print "\n\""+result[3]+"\""
                    else:
                        print "\nThere's nothing there."
            else:
                print "\nNot found."
        elif command=="describe" or command=="desc" or command=="d":
            if target in roomsummary:
                if len(target)>0:
                    db.execute("SELECT * FROM construct WHERE parent_id=? AND snippet=?",(str(room),target))
                    results = db.fetchall()
                    if len(results)>0:
                        for result in results:
                            print "\n\""+result[3]+"\""
                    else:
                        description = raw_input("\nWhat do you see? ")
                        db.execute("INSERT INTO construct (parent_id, snippet, description, nextroom) VALUES (?, ?, ?, ?)",(room,target,description,room))
                        conn.commit()
            else:
                print "\nNot found."
        elif command=="go" or command=="g":
            if target=="back":
                if parent_id>0:
                    room = parent_id
                else:
                    print "You can't go back any further."
            elif target in roomsummary:
                db.execute("SELECT * FROM construct WHERE parent_id=? AND snippet=?",(str(room),target))
                results = db.fetchall()
                if len(results)>0:
                    for result in results:
                        snippetid = result[0]
                        snippetnextroom = result[4]
                        if snippetnextroom!=room:
                            room = snippetnextroom
                        else:#no nextroom - not yet!
                            #therefore, create it!
                            description = raw_input("\nWhat do you see? (or use 'pin') ")
                            if description=="pin":
                                db.execute("UPDATE construct SET nextroom=? WHERE id=?",(str(pin),str(snippetid)))
                                conn.commit()
                                room = pin
                            else:
                                db.execute("INSERT INTO construct (parent_id, snippet, description, nextroom) VALUES (?, ?, ?, ?)",(room,description,description,room))
                                conn.commit()
                                newroomid = db.lastrowid
                                #set new room to have nextroom point to itself, as is the default we're using
                                db.execute("UPDATE construct SET nextroom=? WHERE id=?",(str(newroomid),str(newroomid)))
                                conn.commit()
                                #set the snippet indicated by 'go' to now point to the new room
                                db.execute("UPDATE construct SET nextroom=? WHERE id=?",(str(newroomid),str(snippetid)))
                                conn.commit()
                                #Move into new room
                                room = newroomid
                else:
                    print "\nThere's nowhere to go."
            else:
                print "\nNot found."
        elif command=="drop" and target=="pin":
            pin = room
            print "\n\"Pin dropped.\""
        elif command=="exit":
            sys.exit()
        else:
            #No command was recognized.
            if len(commands)>0:
                print "\nUse: [look|describe|go] followed by a fragment of the room description."
                print "Or 'go back'. Or 'exit'."
            else:
                print ""

