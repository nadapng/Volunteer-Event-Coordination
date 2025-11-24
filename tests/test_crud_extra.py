import pytest
from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper


@pytest.fixture
def db():
    config_dict = {
        "connection": {
            "config": {
                "database": "volunteer_event_db",
                "user": "root",
                "password": "root",
                "host": "localhost",
                "port": 3306,
                "use_pure": True
            },
            "pool": {
                "name": "volunteer_event_coordination_db_pool",
                "size": 10,
                "reset_session": True
            }
        }
    }
    return MySQLPersistenceWrapper(config_dict)


def test_fetch_all_events(db):
    results = db.fetch_all("events")
    assert results is not None


def test_insert_and_get_by_id(db):
    data = {"first_name": "Nada", "last_name": "Test", "email": "get@test.com"}
    db.insert_record("users", data)

    last_id = db.fetch_all("users")[-1][0]  # this is user_id
    record = db.get_by_id("users", "user_id", last_id)
    assert record is not None


def test_update_record(db):
    data = {"first_name": "Update", "last_name": "User", "email": "update@test.com"}
    db.insert_record("users", data)

    last_id = db.fetch_all("users")[-1][0]

    update_data = {"last_name": "Updated"}
    result = db.update_record("users", "user_id", last_id, update_data)
    assert result is True


def test_delete_record(db):
    data = {"first_name": "Delete", "last_name": "User", "email": "delete@test.com"}
    db.insert_record("users", data)

    last_id = db.fetch_all("users")[-1][0]

    result = db.delete_record("users", "user_id", last_id)
    assert result is True
