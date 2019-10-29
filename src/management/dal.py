import sqlite3
import os
import time

create_table_script = '''create table systems_meta
                        (
                            id text not null
                                constraint systems_meta_pk
                                    primary key,
                            last_updated int not null,
                            cpu_count int not null,
                            cpu_freq int not null,
                            cpu_perc TEXT not null,
                            mem_total int not null,
                            mem_available int not null,
                            mem_used int not null,
                            mem_free int not null,
                            mem_used_perc TEXT not null,
                            swap_total int not null,
                            swap_used int not null,
                            swap_free int not null,
                            swap_used_perc text not null
                        );

                        create unique index systems_meta_id_uindex
                            on systems_meta (id);'''


class DAL:
    def __init__(self):
        self.connection = sqlite3.connect(os.environ.get('DB_LOCATION', '/data/data.db'))
        self.cursor = self.connection.cursor()
        self.cursor.row_factory = self._dict_factory

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def _dict_factory(cursor, row):
        dict_record = dict()
        for idx, col in enumerate(cursor.description):
            dict_record[col[0]] = row[idx]
        return dict_record

    def create_table_if_not_exists(self):
        self.cursor.execute('''SELECT name FROM `sqlite_master` WHERE type='table' AND name='systems_meta';''')
        if len(self.cursor.fetchall()) == 0:
            self.cursor.executescript(create_table_script)

    def insert_new_record(self, payload):
        sql = '''INSERT INTO `systems_meta`(id, last_updated, cpu_count, cpu_freq, cpu_perc, mem_total, mem_available,
                mem_used, mem_free, mem_used_perc, swap_total, swap_used, swap_free, swap_used_perc)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        self.cursor.execute(sql, payload.to_tuple())
        self.connection.commit()

    def update_record(self, payload):
        sql = '''UPDATE `systems_meta` SET last_updated=?, cpu_count=?, cpu_freq=?, cpu_perc=?, mem_total=?, 
        mem_available=?, mem_used=?, mem_free=?, mem_used_perc=?, swap_total=?, swap_used=?, swap_free=?, 
        swap_used_perc=? WHERE id=?;'''
        self.cursor.execute(sql, payload.to_tuple()[1:] + (payload.to_tuple()[0],))
        self.connection.commit()

    def already_exists(self, identifier):
        self.cursor.execute('''SELECT id FROM `systems_meta` WHERE id=?;''', (identifier,))
        if len(self.cursor.fetchall()) == 0:
            return False
        return True

    def get_older_records(self):
        self.cursor.execute(f'''SELECT * FROM `systems_meta` WHERE last_updated < {int(time.time()) - 60};''')
        return self.cursor.fetchall()

    def get_all_recent_updated_records(self):
        self.cursor.execute(f'''SELECT * FROM `systems_meta` WHERE last_updated > {int(time.time()) - 60};''')
        return self.cursor.fetchall()
