#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

class SqliteDB():
    
    dbname = ""

    def initializeDB(self, dbname):
        self.dbname = dbname + ".db"
 
        con = lite.connect(self.dbname)
       
        with con:
            cur = con.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
    
            data = cur.fetchone()
    
            print dbname + " Databse SQLite version: %s" % data  

        with con:
            cur = con.cursor()    
    
            cur.execute("DROP TABLE IF EXISTS Member")
            cur.execute("CREATE TABLE Member(Id INT, Name TEXT, Intelligence INT, Charism INT, Force INT, Agility INT, Dexterity INT)")

    def insertMembers(self):
        try:
            con = lite.connect(self.dbname)

            cur = con.cursor()  

            cur.executescript("""
                INSERT INTO Member VALUES(1, 'Bruce', 5, 2, 6, 4, 2);
                INSERT INTO Member VALUES(2, 'Sam', 5, 7, 1, 2, 7);
                INSERT INTO Member VALUES(3, 'Tony', 9, 6, 8, 2, 5);
                INSERT INTO Member VALUES(4, 'Fox', 2, 9, 0, 5, 0);
                """)

            con.commit()
            
        except lite.Error, e:
            
            if con:
                con.rollback()
                
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
        finally:
            
            if con:
                con.close() 
                        
    def listMembers(self):
        con = lite.connect(self.dbname)    

        with con:
            
            con.row_factory = lite.Row
               
            cur = con.cursor() 
            cur.execute("SELECT * FROM Member")

            rows = cur.fetchall()

            for row in rows:
                print "%s %s %s %s" % (row["Id"], row["Name"], row["Intelligence"], row["Force"])
                
    def __init__(self):
            print "Initialize Sqlite Database"

