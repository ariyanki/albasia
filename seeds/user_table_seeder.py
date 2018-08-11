from orator.seeds import Seeder
from datetime import datetime

class UserTableSeeder(Seeder):

    def run(self):
        self.db.table('user').insert({
            'username': 'admin',
            'password': '32e6c60eddbdb220e9d52d40c8633b3e666bd0d6d75af14473146ad38552e0e0',
            'password_salt': '6bf0b1fe-0377-438a-b915-2f9c11009a18',
            'fullname': 'Administrator',
            'phonenumber': '0700000000000',
            'email': 'admin@admin.com',
            'created_by': 1,
            'updated_at': datetime.now(),
            'updated_by': 1,
            'created_at': datetime.now(),
            'status': 1
        })

