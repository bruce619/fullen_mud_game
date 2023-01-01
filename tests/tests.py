import unittest
from run import Fallen
from scripts.transactions import RetrieveTransaction, CreateInsertUpdateDeleteRecord


class FallenTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fallen = Fallen()

    def test_account_creation(self):
        self.fallen.create_account()

    def test_login_user(self):
        self.fallen.login()


class RetrieveTransactionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.retrieve = RetrieveTransaction()

    def test_check_user(self):
        user = self.retrieve.check_user(username='lordbizz')
        self.assertTrue(user)

    def test_location_by_id(self):
        location = self.retrieve.get_location_by_id(1)
        self.assertIn("Terra", location[1])

    def test_get_weapon_by_id(self):
        weapon = self.retrieve.get_weapon_by_id(5)
        self.assertEqual(weapon[1], "blade of fire")


class CreateInsertUpdateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.create = CreateInsertUpdateDeleteRecord()
        self.create.create_user(username='Tobi', password='Ken', race_id=2)
        self.retrieve = RetrieveTransaction()

    def test_create_user(self):
        user = self.create.create_user(username='bruce', password='password', race_id=1)
        self.assertTrue(user)

    def test_check_if_user_was_created(self):
        user = self.retrieve.get_user_by_username(username="Tobi")
        self.assertTrue(user)


if __name__=='__main__':
    unittest.main()
