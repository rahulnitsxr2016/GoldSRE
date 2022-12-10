#!/usr/bin/python3

import sys
import logging
import requests
import json
import datetime
import os
import ssl
import warnings
import psycopg2
import DBConfig
import csv
from copy import deepcopy


# functions
def postRequest(requestType, body):
    logging.info("Start '%s' api", requestType)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
    logging.info("Finish '%s' api", requestType)
    responseObject = json.loads(response.text)
    checkErrorsInResponse(responseObject)
    return responseObject


def checkErrorsInResponse(response):
    error = False
    if "errorCode" in response:
        logging.error("Error code: %s", response["errorCode"])
        error = True
    if "errorMessage" in response:
        logging.error("Error message: %s", response["errorMessage"])
        error = True

    if error:
        logging.error("Status: FAILURE")
        sys.exit(1)


def getAllWsProjectsFromEventsDb():
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT projectname FROM whitesource_project_reference")
        allwsprojects = cursor.fetchall()
        return allwsprojects

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getAllCCProjectsFromEventsDb():
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT regexp_replace(projectname,'|ASL-|GSL-|OnAir-|CIS-|AO-|BP-|Voyager-|MSL-|BI-|Horizon-|SP-|BM-|PSL-|DA-' ::text, ''::text) FROM project_reference")
        allccprojects = cursor.fetchall()
        return allccprojects

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# url = "https://app-eu.whitesourcesoftware.com/api/v1.3"

url = "https://app-eu.whitesourcesoftware.com/api"

args = sys.argv[1:]
if not args or not args[0]:
    logging.error("Please fill startdate as first parameter")
    sys.exit(1)
else:
    startdate = args[0]

if not len(args) > 1:
    logging.error("Please fill enddate as second parameter")
    sys.exit(1)
else:
    enddate = args[1]
'''
startdate = "2020-09-01"
enddate = "2020-09-30"
'''

start_date_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
end_date_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
currenttime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
path = "/home/blackduck/Projects/AutomationSteps/eventscapture/src/reports/"
filename = "new-projects" + currenttime


userKey = "a765df84a78349c1b88bec1b93ab2e91a827b12124b84cdc819843c054244262"
orgToken = "5a68c77bb07645cc94815016e01c5053083c6c745220477e8eb3e4f50f343bd6"
excludeList = ["OSG", "OSGTemplate"]
# get all products in organisation

requestTypeProduct = "getAllProducts"
bodyProduct = {"requestType": requestTypeProduct,
               "userKey": userKey,
               "orgToken": orgToken}

allProducts = postRequest(requestTypeProduct, bodyProduct)
productTokens = {}
print(allProducts["products"])
for member in allProducts["products"]:
    productTokens[member["productName"]] = member["productToken"]

print(productTokens)

'''
productTokens = {"BI-BagPulse": "b74a5cf8125846818a0cda0e267034414fedbb49fc8f4c098532b0d38af69e9a",
                 "BI-PFM": "f0e4f0e2d11a47d5bba86438c2212455a39a2c8cc4a64d5e95a836edad624448",
                 "BM-GG": "22b6d24edd8549bc950fedfe0051a7928536d531515d4efcb14c0da09e851ded",
                 "BM-TAM": "4d09831fd3c14622a97f92c7842b7ad5f835983347b549deaea896cf9a217bc9"}
'''

# Get projects from eventsDb. Populate list for WS and CC projects
wsprojects = getAllWsProjectsFromEventsDb()
wslist = []
print(wsprojects)
for records in wsprojects:
    #    print(records[0])
    wslist.append(records[0])
print("Below is the list of White source projects in events Db")
print(wslist)
numberOfWsProjects = len(wslist)
print('Number of WS projects in eventsdb is %s' % numberOfWsProjects)

ccprojects = getAllCCProjectsFromEventsDb()
print(ccprojects)
cclist = []
for recordscc in ccprojects:
    cclist.append(recordscc[0])
print("Below is list of code center projects")
print(cclist)
numberOfCcProjects = len(cclist)
print('Number of CC projects in eventsdb is %s' % numberOfCcProjects)

# get all projects for different products

requestType = "getAllProjects"
allProjects = {}

warnings.filterwarnings("ignore")

for product in productTokens:
    if product not in excludeList:
        body = {"requestType": requestType,
                "userKey": userKey,
                "productToken": productTokens[product]}
        allProjects[product] = postRequest(requestType, body)
        print("------------------------------------------------------------------------")
        print('All Projects in product %s:' % (product))
        print(allProjects[product]["projects"])

        for project in allProjects[product]["projects"]:
            # print(project["projectName"])
            # print('project vitals for project %s and projectToken %s' % (project["projectName"], project["projectToken"]))
            requestTypepv = "getProjectVitals"
            projectToken = project["projectToken"]
            bodypv = {"requestType": requestTypepv,
                      "userKey": userKey,
                      "projectToken": projectToken
                      }
            projectVitals = postRequest(requestTypepv, bodypv)
            # print(projectVitals["projectVitals"][0]["creationDate"])
            date_time_str = projectVitals["projectVitals"][0]["creationDate"]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S %z')

            if start_date_obj.date() <= date_time_obj.date() <= end_date_obj.date():
                print(project["projectName"])
                print('CreationDate:', date_time_obj.date())
                print("creation date is in mentioned time frame")
                projectNameAfterRemovingVersion, version = project["projectName"].split(' - ')
                print(projectNameAfterRemovingVersion)
                if projectNameAfterRemovingVersion in wslist:
                    print(
                        'Project %s already exists in White source reference table in eventsdb' % projectNameAfterRemovingVersion)
                else:
                    print(
                        'Project %s is a new project. It does not exist in reference table' % projectNameAfterRemovingVersion)
                    if projectNameAfterRemovingVersion in cclist:
                        print('Project %s exists in code center reference table in eventsdb' % projectNameAfterRemovingVersion)
                        existincclist = 'Yes'
                    else:
                        print('Project %s does not exist in code center reference table in eventsdb' % projectNameAfterRemovingVersion)
                        existincclist= 'No'

			
                    with open(path + filename + ".csv", mode='a', newline='') as new_projects_file:
                        project_writer = csv.writer(new_projects_file, delimiter=',', quotechar='"',
                                                    quoting=csv.QUOTE_MINIMAL)
                        project_writer.writerow([projectNameAfterRemovingVersion, version, product, date_time_obj.date(), existincclist])

csvfilename = path + filename + ".csv"
htmlfilename = path + filename + ".html"

#   checking if new project file exists. If yes, converting it to html table

if os.path.exists(csvfilename):
    filein = open(csvfilename, "r")
    fileout = open(htmlfilename, "w")
    data = filein.readlines()
    table = "<html><body><table>\n"
    
# Create the table's column headers
    header = ["projectname", "versionused", "product", "creationdate", "existinCC"]
    table += "  <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"
    # Create the table's row data
    for line in data[0:]:
        row = line.split(",")
        table += "  <tr>\n"
        for column in row:
            table += "    <td>{0}</td>\n".format(column.strip())
        table += "  </tr>\n"

    table += "</html></body></table>"
    fileout.writelines(table)
    fileout.close()
    filein.close()
#    command = '/usr/local/bin/sendEmail -f opensource@sita.aero -t aman.bhaskar@sita.aero -s mx-atl.sita.aero -u New WhiteSource Projects -a %s -m < %s'
#    print('command' %(csvfilename, htmlfilename))
    os.system("/usr/local/bin/sendEmail -f opensource@sita.aero -t opensource@sita.aero -s mx-atl.sita.aero -u New WhiteSource Projects created between %s and %s -a %s -m < %s" % (startdate, enddate, csvfilename, htmlfilename))

else:
    print("No new projects to be added in WS table")
    os.system("/usr/local/bin/sendEmail -f opensource@sita.aero -t opensource@sita.aero -s mx-atl.sita.aero -u New WhiteSource Projects created between %s and %s -m No new WS project found which does not exist in WS table" % (startdate, enddate))
