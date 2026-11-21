import pytest
from django.db import connection


@pytest.mark.django_db
def test_django_puede_conectarse_a_la_base_de_datos():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)
