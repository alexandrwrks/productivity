import aiosqlite

class BaseDB:
    def __init__(self, db_name: str ="tg_money_database.db"):
        self.db_name = db_name

    async def execute_query(
            self,
            query: str,
            params: tuple = (),
            fetch_one: bool = False,
            fetch_all: bool = False
    ):
        """Универсальный метод для работы с БД"""  
        try:       
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("PRAGMA foreign_keys = ON")

                cursor = await db.execute(query, params)

                if fetch_one:
                    result = await cursor.fetchone()
                    print(f"Запрос выполнен: {query[:50]}...")
                    return result
                elif fetch_all:
                    result = await cursor.fetchall()
                    print(f"Запрос выполнен: {query[:50]}...")
                    return result
                else:
                    await db.commit()
                    print(f"Запрос выполнене: {query[:50]}...")
                    return cursor.lastrowid

        except aiosqlite.Error as e:
            print(f"Ошибка БД: {e}")
            return None
        
class CostManager(BaseDB):
    async def init_table(self):
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS CurrCost (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                xau REAL NOT NULL,
                xag REAL NOT NULL,
                xpt REAL NOT NULL, 
                xpd REAL NOT NULL,
                datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
            result = await self.execute_query(query)
            return result
        except aiosqlite.Error as e:
            print(f"Ошибка инициализации таблицы: {e}")
            return None
        
    async def add_position(self):
        
        query = '''
        INSERT INTO CurrCost 
        '''
        params = ()