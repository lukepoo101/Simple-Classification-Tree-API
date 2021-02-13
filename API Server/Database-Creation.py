import sqlite3 as sl

Data = sl.connect("Data.db")

with Data:
    Data.execute("""
        CREATE TABLE ANIMALS (
            name TEXT,
            legs INTERGER,
            hair BOOLEAN,
            fins BOOLEAN,
            carnivor BOOLEAN,
            herbivore BOOLEAN,
            likes_milk BOOLEAN,
            wool BOOLEAN,
            insect BOOLEAN,
            pet BOOLEAN,
            mammal BOOLEAN
        );
    """)

sql = 'INSERT INTO ANIMALS (name, legs, hair, fins, carnivor, herbivore, likes_milk, wool, insect, pet, mammal) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
data = [
    ("Cat", 4, True, False, True, False, True, False, False, True, True),
    ('Dog', 4, True, False, True, False, False, False, False, True, True),
    ('Pig', 4, False, False, False, True, False, False, False, False, True)
]

with Data:
    Data.executemany(sql, data)
