import os
from app import app
from flask import Flask, request, json
from orator.migrations.database_migration_repository import DatabaseMigrationRepository
from orator.migrations.migrator import Migrator
from orator.seeds.seeder import Seeder
from seeds.database_seeder import DatabaseSeeder
from flask_orator import Orator

env = os.environ.get('FLASK_ENV', 'development')
if env != 'testing':
    raise RuntimeError("Your FLASK_ENV is not testing")

db = Orator(app)    

def reset_database():
    repo = DatabaseMigrationRepository(resolver=db, table='migrations')
    migrator = Migrator(repository=repo, resolver=db)
    seeder = Seeder(resolver=db)
    # run migrations
    if not migrator.repository_exists():
        repo.create_repository()
    migrator.reset(path='migrations')
    migrator.run(path='migrations')
    seeder.call(klass=DatabaseSeeder)