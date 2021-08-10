import sqlite3


class Connector:

    def __init__(self, path="db.db"):
        self.__con = sqlite3.connect(path)
        self.__cur = self.__con.cursor()

    def __load_object(self, object):

        tables_dict = {'F': 'food', 'V': 'venom', 'W': 'wall', 'C': 'cell'}
        table_format = ''
        data = list(object.get_cords())

        if str(object) == 'C':
            table_format = ', health, turns, direction, pointer'
            data.extend(object.get_data())

            self.__cur.execute("SELECT * FROM cell_objects")
            cell_number = len(self.__cur.fetchall())

            self.__cur.execute("CREATE TABLE genotype{}("
                               "ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                               "gen INTEGER NOT NULL)".format(cell_number + 1))

            genotype = object.get_genotype()
            for i in range(len(genotype)):
                self.__cur.execute("INSERT INTO genotype{}(gen)"
                                   "VALUES({})".format(cell_number + 1, genotype[i]))

        self.__cur.execute("INSERT INTO {}_objects(x, y{}) "
                           "VALUES({})".format(tables_dict[str(object)], table_format, str(data)[1:-1]))

        self.__con.commit()

    def load_data(self, world_data, objects):
        self.clear_db()

        self.__cur.execute("DELETE FROM world_data")
        self.__cur.execute("INSERT INTO world_data(generation)"
                           "VALUES({})".format(world_data[0]))
        self.__cur.execute("INSERT INTO summary_lifetime(time)"
                           "VALUES({})".format(world_data[1]))
        for object in objects:
            self.__load_object(object)

        self.__con.commit()

    def get_data(self):

        data = {}

        self.__cur.execute("SELECT * FROM world_data")
        data['generation'] = self.__cur.fetchall()[-1]
        data['objects'] = {}

        object_types = ['food', 'venom', 'wall', 'cell']
        for i in range(len(object_types)):

            self.__cur.execute('select * from {}_objects'.format(object_types[i]))
            heads = list(map(lambda x: x[0], self.__cur.description))

            self.__cur.execute("SELECT {} FROM {}_objects".format(', '.join(i for i in heads if i != "ID"),
                                                                  object_types[i]))
            data['objects'][object_types[i]] = self.__cur.fetchall()

        return data

    def clear_db(self):

        tables_dict = {0: 'food', 1: 'venom', 2: 'wall', 3: 'cell'}

        self.__cur.execute("SELECT * FROM cell_objects")
        cells = self.__cur.fetchall()

        for i in range(len(cells)):
            self.__cur.execute("DROP TABLE IF EXISTS genotype{}".format(str(i + 1)))

        for i in range(4):
            self.__cur.execute("DELETE FROM {}_objects".format(tables_dict[i]))

        self.__cur.execute("DELETE FROM world_data")

        self.__con.commit()


"""    def save_gen(self, descendants_genotypes, summary_lifetime, generation):
        self.__cur.execute('INSERT INTO world_data(summary_lifetime, generation) '
                           'VALUES({}, {})'.format(summary_lifetime, generation))

        for i in range(len(descendants_genotypes)):
            self.__cur.execute("CREATE TABLE genotype{}("
                               "ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                               "gen INTEGER NOT NULL)".format(i + 1))
            for gen in descendants_genotypes[i]:
                self.__cur.execute('INSERT INTO genotype{}(gen) '
                                   'VALUES({})'.format(i + 1, gen))

        self.__con.commit()"""