import psycopg2
import DBConfig

def check_ifProjectExistsinProjecttable(project):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    print(project['projectname'])
    print(project['projectversion'])
    pn = project['projectname']
    pv = project['projectversion']
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        global projectpid
        cursor = connection.cursor()
        cursor.execute("SELECT projectid FROM project where projectname='%s' and projectversion='%s'" % (pn, pv))
        projectpid = cursor.fetchone()
        if projectpid:
            print('project id of project name %s and version %s is %s' %(pn,pv,projectpid[0]))
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_ifProjectExistsinParameterstable(id):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    print(id)
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM parameters where projectid='%s'" % (id))
        record = cursor.fetchone()
        print(record)
        if record:
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
def check_ifintpendidcounthasvalue(id):
    print("-----------------------Inside check_ifintpendidcounthasvalue Function-------------------------")
    print(id)
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT initialpendingidcount FROM project where projectid='%s'" % (id))
        record = cursor.fetchone()
        print(record[0])
        if record[0] is '' or record[0] == "NotSet":
            return "Valuedoesnotexist"
        else:
            return record[0]

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_ifProjectExistsineventstable(id):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    print(id)
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events where projectid='%s'" % (id))
        record = cursor.fetchone()
        print(record)
        if record:
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_ifProjectExistsinCommentsTable(id):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    print(id)
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM project_comments where projectid='%s'" % (id))
        record = cursor.fetchone()
        print(record)
        if record:
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_ifProjectExistsinRemediationtable(name):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    print(name)
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM project_remediation where projectname='%s'" % (name))
        record = cursor.fetchone()
        print(record)
        if record:
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_ifProjectExistsinprojectsizetable(id):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    print(id)
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM project_size where projectid='%s'" % (id))
        record = cursor.fetchone()
        print(record)
        if record:
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_ifProjectExistsinWSReftable(pn, pr):
    print("-----------------------Inside check_ifProjectExists Function-------------------------")
    projectName = pn
    product = pr

    print('projectname and product : %s and %s' % (projectName, product))
    try:
        params = DBConfig.config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM whitesource_project_reference where projectname ='%s' and product = '%s'" % (
        projectName, product))
        record = cursor.fetchone()
        print(record)
        if record:
            return "ProjectExists"
        else:
            return "ProjectDoesNotExist"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

