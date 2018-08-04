from orator.migrations import Migration


class CreateUserAuthenticationTable(Migration):

    def up(self):
        with self.schema.create('user_authentication') as table:
            table.increments('id')
            table.integer('user_id').unsigned()
            table.string('username', 255)
            table.string('password', 500)
            table.string('password_salt', 500).nullable()
            table.integer('status').default(0)
            table.integer('created_by').nullable()
            table.integer('updated_by').nullable()
            table.timestamps()
            table.foreign('user_id').references('id').on('user').on_delete('restrict').on_update('restrict')

    def down(self):
        self.schema.drop_if_exists('user_authentication')
