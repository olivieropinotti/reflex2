import reflex as rx
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor

def get_db_connection():
    # Replace with your actual Supabase/PostgreSQL credentials
    return connect(
        dbname="supabase_db",
        user="username",
        password="password",
        host="your-db-host.supabase.co",
        port="5432"
    )

class AuthState(rx.State):
    username: str = ""
    password: str = ""
    confirm_password: str = ""

    def signup(self):
        if self.password != self.confirm_password:
            return rx.window_alert("Passwords do not match.")

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (self.username,))
                if cursor.fetchone():
                    return rx.window_alert("Username already exists.")

                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (self.username, self.password)
                )
                conn.commit()
                return rx.redirect("/")
        except Exception as e:
            return rx.window_alert(str(e))
        finally:
            conn.close()

    def login(self):
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT password FROM users WHERE username = %s", (self.username,)
                )
                result = cursor.fetchone()
               
