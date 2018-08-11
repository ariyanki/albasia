from orator.migrations import Migration


class CreateUserTable(Migration):

    def up(self):
        with self.schema.create('user') as table:
            table.increments('id')
            table.string('username', 255).unique()
            table.string('password', 500)
            table.string('password_salt', 500).nullable()
            table.string('fullname', 255)
            table.string('phonenumber', 255)
            table.string('email', 255)
            table.string('longitude', 255).nullable()
            table.string('latitude', 255).nullable()
            table.string('photo_filename', 255).nullable()
            table.integer('is_loggedin').default(0)
            table.integer('login_attempt').default(0)
            table.timestamp('last_loggedin_at').nullable()
            table.string('access_source', 255).nullable()
            table.timestamp('last_access_at').nullable()
            table.integer('status').default(0)
            table.integer('created_by').nullable()
            table.integer('updated_by').nullable()
            table.timestamps()

    def down(self):
        self.schema.drop_if_exists('user')
