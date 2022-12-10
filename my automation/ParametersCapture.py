#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script is to get the project paramters from some.xml and stores them into database
"""

import sys
import psycopg2

def parse_arguments(arguments):
 projectdict = {}
 for args in arguments:
   args = args.strip('--')
   projectparameter, value = args.split('=')
   print(projectparameter, value)
   if value:
     projectdict[projectparameter]=value
   else:
     projectdict[projectparameter]="Not set by team"
 return projectdict


projectdict=parse_arguments(sys.argv[1:])
print(projectdict)

def check_ifProjectExists(projectname):
  print(projectname['project.name'])
  pm=projectname['project.name']
  print(pm)
  try:
       connection = psycopg2.connect(user = "postgres",
                                  password = "pwd",
                                  host = "ip addr",
                                  port = "port of postgres",
                                  database = "db name")

       cursor = connection.cursor()
       cursor.execute("SELECT * FROM parameters where projectname='%s'" %(pm))
       record = cursor.fetchone()
       print(record)

  except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
  finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

check_ifProjectExists(projectdict)


