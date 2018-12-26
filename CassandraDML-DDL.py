import logging
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
from cassandra.query import SimpleStatement


class CassandraBase:

    def __init__(self):
        self.cluster = None
        self.session = None
        self.keyspace = None
        self.log = None

    def __del__(self):
        self.cluster.shutdown()

    def createsession(self):
        self.cluster = Cluster(['localhost'])
        self.session = self.cluster.connect(self.keyspace)

    def getsession(self):
        return self.session

    #log info to see what went wrong
    def setlogger(self):
        log = logging.getLogger()
        log.setLevel('INFO')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        log.addHandler(handler)
        self.log = log

    # Create Keyspace based on Given Name
    def createkeyspace(self, keyspace):
        """
        :param keyspace:  The Name of Keyspace to be created
        :return:
        """
        # Before we create new lets check if exiting keyspace; we will drop that and create new
        rows = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if keyspace in [row[0] for row in rows]:
            self.log.info("dropping existing keyspace...")
            self.session.execute("DROP KEYSPACE " + keyspace)

        self.log.info("creating keyspace...")
        self.session.execute("""
                CREATE KEYSPACE %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % keyspace)

        self.log.info("setting keyspace...")
        self.session.set_keyspace(keyspace)

    def create_table(self):
        c_sql = """
                CREATE TABLE IF NOT EXISTS employee (emp_id int PRIMARY KEY,
                                              ename varchar,
                                              sal double,
                                              city varchar);
                 """
        self.session.execute(c_sql)
        self.log.info("Employee Table Created !!!")

    #batch insert
    def insert_data(self):
        insert_sql = self.session.prepare("INSERT INTO  employee (emp_id, ename , sal,city) VALUES (?,?,?,?)")
        batch = BatchStatement()
        batch.add(insert_sql, (1, 'e1', 2555, 'c1'))
        batch.add(insert_sql, (2, 'e2', 5660, 'c2'))
        batch.add(insert_sql, (3, 'e3', 2547, 'c3'))
        batch.add(insert_sql, (4, 'e4', 2547, 'c4'))
        self.session.execute(batch)
        self.log.info('Batch Insert Completed')

    def select_data(self):
        rows = self.session.execute('select * from employee limit 5;') #user can provide desired CQL querry to execute
        for row in rows:
            print(row.ename, row.sal)

    def update_data(self):
        pass

    def delete_data(self):
        pass


if __name__ == '__main__':
    run = CassandraBase()
    run.createsession()
    run.setlogger()
    run.createkeyspace('KS1') #user can define desired keyspace name
    run.create_table()
    run.insert_data()
    run.select_data()