from django.test.simple import DjangoTestSuiteRunner
from mongoengine import connect

class NoSQLTestRunner(DjangoTestSuiteRunner):
    def setup_databases(self):
        db_name = 'testsuite'
	connect(db_name)
	print 'Creating test-database: ' + db_name
	return db_name	
 
    def teardown_databases(self, db_name,*args):
        from pymongo import Connection
	conn = Connection()
	conn.drop_database(db_name)
	print 'Dropping test-database: ' + db_name

