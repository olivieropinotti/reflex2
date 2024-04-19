# user_management.py
import reflex as rx
from utils.database import get_db_connection

class UserState(rx.State):
    error_message: str = ""

    def register_user(self, email, full_name, password):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)",
                    (email, full_name, password)  # Storing password directly for demonstration
                )
                conn.commit()
        except Exception as e:
            self.error_message = f"Registration failed: {str(e)}"
        finally:
            conn.close()

    def login_user(self, email, password):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT password FROM users WHERE email = %s", (email,)
                )
                result = cursor.fetchone()
                if result and result[0] == password:
                    self.error_message = "Login successful"
                else:
                    self.error_message = "Login failed"
        finally:
            conn.close()

    def logout_user(self):
        # Simple message reset for logout simulation
        self.error_message = "Logged out successfully"
