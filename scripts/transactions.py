import logging
import sys
import sqlite3

# REF: https://docs.python.org/3/howto/logging.html#logging-to-a-file
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened,
# or indicative of some problem in the near future (e.g. ‘disk space low’).
# The software is still working as expected.
# ERROR Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL A serious error, indicating that the program itself may be unable to continue running.


# basic logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler("../error.logs")
file_handler.setFormatter(logging_formatter)
logger.addHandler(file_handler)


# db connection function
class RetrieveTransaction:

    def __int__(self):
        pass

    def getConn(self):
        """ Connect To Database Server """

        conn = None

        try:
            logger.info("connection to database...")
            conn = sqlite3.connect('../fallen.db')
        except (Exception, sqlite3.Error) as e:
            logger.error("Error: " + str(e))
            sys.exit(1)

        logger.info("connection is successful")
        return conn

    def get_users(self):
        # the method gets all users
        conn = self.getConn()
        cursor = conn.cursor()

        query = "SELECT * FROM user;"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_users): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_orb_by_location(self, location_id=None):
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"""
            SELECT * FROM orb
            INNER JOIN location_orbs
                ON orb.id = location_orbs.orb_id
            WHERE location_orbs.location_id = {location_id}
        """

        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_orb_by_location): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_orbs(self):
        # the method gets all orbs
        conn = self.getConn()
        cursor = conn.cursor()

        query = "SELECT * FROM orb;"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_orbs): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_inventories(self):
        # the method gets all inventories
        conn = self.getConn()
        cursor = conn.cursor()

        query = "SELECT * FROM inventory;"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_inventories): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_weapons(self):
        # the method gets all weapons
        conn = self.getConn()
        cursor = conn.cursor()

        query = "SELECT * FROM weapon;"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_weapons): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_user_by_id(self, user_id=None):
        # the method gets a user by id
        conn = self.getConn()
        cursor = conn.cursor()
        query = f"SELECT * FROM user WHERE user.id={user_id};"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            if record is not None:
                return record
            return False
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (get_user_by_id): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def login_user(self, username=None, password=None):
        # the method logs users in
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM user WHERE user.username='{username}' AND user.password='{password}';"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            return record
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (login_user): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def check_user(self, username=None):
        # returns true if a user exists
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM user WHERE user.username='{username}';"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            if record is not None:
                return True
            return False
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (check_user): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_realm_by_id(self, realm_id):
        # get a location by id
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM realm WHERE realm.id={realm_id};"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            return record
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (get_realm_by_id): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_location_by_id(self, id_=None):
        # get a location by id
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM location WHERE location.id={id_};"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            return record
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (get_location_by_id): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_weapon_by_id(self, id_=None):
        # get a weapon by id
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM weapon WHERE weapon.id={id_};"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            return record
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (get_weapon_by_id): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_inventory_by_id(self, id_=None):
        # get an inventory by id
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM inventory WHERE inventory.id={id_};"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            return record
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (get_inventory_by_id): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_user_by_username(self, username=None):
        # get an inventory by user
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"SELECT * FROM user WHERE user.username='{username}';"

        try:
            cursor.execute(query)
            record = cursor.fetchone()
            return record
        except (Exception, AttributeError, sqlite3.Error) as e:
            logger.error(f'Error (get_inventory_by_id): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_user_orb(self, user_id=None):
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"""SELECT * FROM user_orb WHERE user_orb.user_id={user_id};
                """
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_user_orb): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_user_locations(self, user_id=None):

        conn = self.getConn()
        cursor = conn.cursor()

        query = f"""SELECT * FROM user_location WHERE user_location.user_id={user_id};
        """
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_user_locations): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_user_weapons(self, user_id=None):
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"""
        SELECT weapon.id, weapon.name FROM weapon
        INNER JOIN user_weapon
            ON weapon.id = user_weapon.weapon_id
        WHERE user_weapon.user_id = {user_id};
        """
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_user_weapons): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()

    def get_user_inventories(self, user_id=None):
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"""SELECT * FROM user_inventory WHERE user_inventory.user_id={user_id};
        """
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except (sqlite3.Error, sqlite3.DatabaseError) as e:
            logger.error(f'Error (get_user_inventories): {e}')
            logger.exception(str(e))
        finally:
            cursor.close()


class CreateInsertUpdateDeleteRecord:

    def __int__(self):
        pass

    def getConn(self):
        """ Connect To Database Server """

        conn = None

        try:
            logger.info("connection to database...")
            conn = sqlite3.connect('../fallen.db')
        except (Exception, sqlite3.Error) as e:
            logger.error("Error: " + str(e))
            sys.exit(1)

        logger.info("connection is successful")
        return conn

    def create_user(self, username=None, password=None, race_id=None):
        # used in creating new user records
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"INSERT INTO user (username, password, race_id) VALUES ('{username}', '{password}', {race_id});"

        try:
            cursor.execute(query)
            conn.commit()
            record = cursor.lastrowid
            return record
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (create_user): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def game_won(self, user_id=None):
        # used in creating new user records
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"update user set won = true where user.id = {user_id};"

        try:
            cursor.execute(query)
            conn.commit()
            record = cursor.lastrowid
            return record
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (create_user): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def update_price(self, user_id=None, balance=None):
        # used to save a users current location
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"UPDATE user SET coins = {balance} WHERE user.id={user_id}"

        try:
            cursor.execute(query)
            conn.commit()
            return True
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (update_price): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def update_strength_level(self, user_id=None, strength=None):
        # used to save a users current location
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"""
        UPDATE user
        SET strength_level = strength_level + {strength}
        WHERE user.id = {user_id};
        """

        try:
            cursor.execute(query)
            conn.commit()
            return True
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (update_strength_level): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def update_rank(self, user_id=None, rank=None):
        # used to save a users current location
        conn = self.getConn()
        cursor = conn.cursor()

        query = f" UPDATE user SET rank = '{rank}' WHERE user.id={user_id};"

        try:
            cursor.execute(query)
            conn.commit()
            return True
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (update_rank): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def save_user_location(self, user_id, location_id):
        # used to save a users current location
        conn = self.getConn()
        cursor = conn.cursor()

        query = f"INSERT INTO user_location (user_id, location_id) VALUES ({user_id}, {location_id});"

        try:
            cursor.execute(query)
            conn.commit()
            record = cursor.lastrowid
            return record
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (save_user_location): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def save_user_weapon(self, user_id=None, weapon_id=None):

        conn = self.getConn()
        cursor = conn.cursor()

        query = f"INSERT INTO user_weapon (user_id, weapon_id) VALUES ({user_id}, {weapon_id});"

        try:
            cursor.execute(query)
            conn.commit()
            record = cursor.lastrowid
            return record
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (save_user_weapon): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def save_user_inventory(self, user_id=None, inventory_id=None):

        conn = self.getConn()
        cursor = conn.cursor()

        query = f"INSERT INTO user_inventory (user_id, inventory_id) VALUES ({user_id}, {inventory_id});"

        try:
            cursor.execute(query)
            conn.commit()
            record = cursor.lastrowid
            return record
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (save_user_inventory): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()

    def save_user_orb(self, user_id=None, orb_id=None):

        conn = self.getConn()
        cursor = conn.cursor()

        query = f"INSERT INTO user_orb (user_id, orb_id) VALUES ({user_id}, {orb_id});"

        try:
            cursor.execute(query)
            conn.commit()
            record = cursor.lastrowid
            return record
        except (Exception, AttributeError, sqlite3.IntegrityError, sqlite3.Error) as e:
            logger.error(f'Error (save_user_orb): {e}')
            logger.exception(str(e))
            conn.rollback()
        finally:
            cursor.close()