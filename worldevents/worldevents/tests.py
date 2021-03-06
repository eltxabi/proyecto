from django.conf import settings
from django.db.models.loading import cache
from django.test.simple import DjangoTestSuiteRunner
from django.test.simple import build_suite, build_test, reorder_suite
from django.test.testcases import SimpleTestCase, TransactionTestCase
from django.utils import unittest
from mongoengine import connect
from mongoengine.connection import get_db, disconnect


class MongoTestCase(SimpleTestCase):
    """
TestCase class that drops all collections the collections between the tests
"""

    def tearDown(self):
        db = get_db()
        for collection in db.collection_names():
            if collection == 'system.indexes':
                continue
            db.drop_collection(collection)


class MongoHybridTestCase(MongoTestCase, TransactionTestCase):

    def tearDown(self):
        MongoTestCase.tearDown(self)
        TransactionTestCase.tearDown(self)


class MongoTestSuiteRunner(DjangoTestSuiteRunner):
    """
TestRunner that could be set as TEST_RUNNER in Django settings module to
test MongoEngine projects that do not use RDBMS.
"""
    db_name = 'test_%s' % settings._MONGODB_NAME

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.setup_test_environment()
        teardown_data = self.setup_databases()
        suite = self.build_suite(test_labels, extra_tests)
        result = self.run_suite(suite)
        self.teardown_databases(teardown_data)
        self.teardown_test_environment()
        return self.suite_result(suite, result)

    def setup_databases(self):
        disconnect()
        return connect(self.db_name)

    def teardown_databases(self, connection, **kwargs):
        connection.disconnect()

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        """
Rewrite of the original build_suite method of the DjangoTestSuiteRunner
to skip tests from the Django own test cases as they restricted to the
Django ORM settings that we do not need to be set at all.
"""
        suite = unittest.TestSuite()

        if test_labels:
            for label in test_labels:
                if '.' in label:
                    suite.addTest(build_test(label))
                else:
                    app = cache.get_app(label)
                    suite.addTest(build_suite(app))
        else:
            for app in self.get_apps():
                suite.addTest(build_suite(app))

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (SimpleTestCase,))

    def get_apps(self):
        """
Do not run Django own tests
"""
        return filter(
            lambda app: app.__name__.split('.', 1)[0] != 'django',
            cache.get_apps())


class MongoHybridTestSuiteRunner(MongoTestSuiteRunner):
    """
Hybrid TestRunner that could be set as TEST_RUNNER in Django settings
module to test MongoEngine projects that use both Mongoengine and Django
built in RDBMS features.
"""

    def setup_databases(self):
        return {
            'connection': MongoTestSuiteRunner.setup_databases(self),
            'old_config': DjangoTestSuiteRunner.setup_databases(self),
        }

    def teardown_databases(self, teardown_data, **kwargs):
        MongoTestSuiteRunner.teardown_databases(self, teardown_data['connection'], **kwargs)
        DjangoTestSuiteRunner.teardown_databases(self, teardown_data['old_config'], **kwargs)

'''
from django.test.simple import DjangoTestSuiteRunner
from mongoengine import connect
#For select test database in models
from django.conf import settings
#--------------------------------

class NoSQLTestRunner(DjangoTestSuiteRunner):
#For select test database in models    	
    def __init__(self,*args,**kwargs):
	settings.TEST_MODE=True
	super(NoSQLTestRunner,self).__init__(*args,**kwargs)
#---------------------------------
 
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
'''
