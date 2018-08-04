from orator.seeds import Seeder
from datetime import datetime

class UserTableSeeder(Seeder):

    def run(self):
        self.db.table('user').insert({
            'username': 'sadmin',
            'password': '6e76f6a69486a89f951910e6e169597a4c4bd267226f6df577851032c296232f',
            'password_salt': '44a509a2-217e-4227-a67b-5057feb7c22f',
            'fullname': 'Super Admin',
            'phonenumber': '0700000000000',
            'email': 'admin@admin.com',
            'created_by': 1,
            'updated_at': datetime.now(),
            'updated_by': 1,
            'created_at': datetime.now(),
            'status': 1
        })

