import json
import pytest
from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper

@pytest.fixture
def db():
    # Load config from the real JSON file
    with open("src/config/app_config.json") as f:
        config = json.load(f)

    print("\nCONFIG USED:", config)

    wrapper = MySQLPersistenceWrapper(config)
    return wrapper


def test_connection(db):
    conn = db.connection
    assert conn is not None


def test_insert_user(db):
    user_data = {
        "first_name": "Nada",
        "last_name": "Test",
        "email": "nada@test.com"
    }

    result = db.create_user(user_data)
    assert result is True
