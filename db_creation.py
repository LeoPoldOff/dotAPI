from account import Account
from uuid import uuid4
import sqlite3


client1 = Account(uuid4(), 'Петров Иван Сергеевич', 1700, 300, 1)
client2 = Account(uuid4(), 'Kazitsky Jason', 200, 200, 1)
client3 = Account(uuid4(), 'Пархоменко        Антон Александрович', 10, 300, 1)
client4 = Account(uuid4(), 'Петечкин Петр Измаилович', 1000000, 1, 0)

clientBase = [(str(client1.number), client1.fio, client1.balance, client1.holds, client1.status),
              (str(client2.number), client2.fio, client2.balance, client2.holds, client2.status),
              (str(client3.number), client3.fio, client3.balance, client3.holds, client3.status),
              (str(client4.number), client4.fio, client4.balance, client4.holds, client4.status)
              ]

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE clientbase")
cursor.execute("""CREATE TABLE clientBase(
                    number VARCHAR(50),
                    fio VARCHAR(50),
                    balance INT,
                    holds INT,
                    status BIT)
                """)
cursor.executemany("INSERT INTO clientbase VALUES (?, ?, ?, ?, ?)", clientBase)
conn.commit()
cursor.close()
