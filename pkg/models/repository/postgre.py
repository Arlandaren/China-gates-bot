import asyncpg,datetime

class Database:
    async def InitDB(self, conn) -> None:
        try:
            self.pool = await asyncpg.create_pool(conn)
            async with self.pool.acquire() as c:
                async with c.transaction():
                    await c.execute('''
                        CREATE TABLE IF NOT EXISTS users(
                        id BIGINT PRIMARY KEY,
                        username VARCHAR,
                        balance INTEGER default 0,
                        joined_at TIMESTAMP WITH TIME ZONE
                        );
                    ''')
                    await c.execute('''
                        CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        login VARCHAR NOT NULL,
                        password VARCHAR NOT NULL,
                        truck_grnz VARCHAR NOT NULL,
                        trunk_grnz VARCHAR NOT NULL,
                        driver_email VARCHAR NOT NULL,
                        driver_phone VARCHAR NOT NULL
                        );
                    ''')
        except Exception as err:
            print("Ошибка при создании таблиц:", err)

    async def create_user(self, id, username):
        async with self.pool.acquire() as c:
            try:
                await c.execute(
                    "INSERT INTO users (id, username, balance, joined_at) VALUES ($1, $2, $3, $4)",
                    id, username, 0, datetime.datetime.now()
                )
                return True
            except Exception as err:
                print("ошибка бд: ", err)
                return False
    async def check_user(self,id) -> bool:
        async with self.pool.acquire() as c:
            result = await c.fetchval(f"SELECT * FROM users WHERE id = $1 LIMIT 1", id)
            if result:
                return True
            else:
                return False
    async def get_user(self,id):
        async with self.pool.acquire() as c:
            try:
                user = await c.fetchrow("SELECT * FROM users WHERE id = $1", int(id))   
                if user:
                    return user
                return None
            except Exception as err:
                print(err)
                return None
    async def increase_balance_user(self, amount: int, user_id: int) -> bool:
        async with self.pool.acquire() as c:
            try:
                await c.execute(
                    "UPDATE users SET balance = balance + $1 WHERE id = $2",
                    amount, user_id
                )
                return True
            except Exception as err:

                print("Ошибка при обновлении баланса пользователя:", err)
                return False
    async def decrease_balance_user(self, amount: int, user_id: int) -> bool:
        async with self.pool.acquire() as c:
            try:
                await c.execute(
                    "UPDATE users SET balance = balance - $1 WHERE id = $2",
                    amount, user_id
                )
                return True
            except Exception as err:

                print("Ошибка при обновлении баланса пользователя:", err)
                return False
    async def create_order(self,login,password,truck_grnz,trunk_grnz,driver_email,driver_phone):
        async with self.pool.acquire() as c:
            try:
                await c.execute("INSERT INTO orders (login,password,truck_grnz,trunk_grnz,driver_email,driver_phone) VALUES ($1,$2,$3,$4,$5,$6)", login,password,truck_grnz,trunk_grnz,driver_email,driver_phone)
                return True
            except Exception as err:
                print("Ошибка при создании заказа:", err)
                return False
            
DB = Database()