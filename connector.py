import sqlite3


class Connector:

    def __init__(self, path="db.db"):
        self.__con = sqlite3.connect(path)
        self.__cur = self.__con.cursor()

    def __load_object(self, object):

        tables_dict = {'F': 'food', 'V': 'venom', 'W': 'walls', 'C': 'cells'}
        data = list(object.get_cords())

        if str(object) == 'C':
            data.extend(object.get_data())

            self.__cur.execute("SELECT * FROM cell_objects")
            cell_number = len(self.__cur.fetchall())

            self.__cur.execute("CREATE TABLE genotype{}("
                                "ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                                "gen INTEGER NOT NULL)".format(cell_number))

            genotype = object.get_genotype()
            for i in range(len(genotype)):
                self.__cur.execute("INSERT INTO genotype{}(gen)"
                                   "VALUES({})".format(cell_number, genotype[i]))

        self.__cur.execute("INERT INTO {}_elements(x, y)"
                           "VALUES ()".format(tables_dict[str(object)]), *data)

        self.__con.commit()

    def load_data(self, world_data, objects):

        self.__cur.execute("INSERT INTO world_data(generation)"
                           "VALUES({})".format(world_data[0]))

        for object in objects:
            self.__load_object(object)

        self.__con.commit()

    def get_data(self):

        data = {}

        self.__cur.execute("SELECT * FROM TABLE world_data")
        data['generation'] = self.__cur.fetchone()

        return data

    def clear_db(self):

        tables_dict = {0: 'food', 1: 'venom', 2: 'wall', 3: 'cell'}

        self.__cur.execute("SELECT * FROM cell_objects")
        cells = self.__cur.fetchall()

        for i in range(len(cells)):
            self.__cur.execute("DROP TABLE genotype{}".format(i + 1))

        for i in range(4):
            self.__cur.execute("DELETE FROM {}_objects".format(tables_dict[i]))

        self.__cur.execute("DELETE FROM world_data")

        self.__con.commit()

