import pytest
from fastapi.testclient import TestClient
from fastapi_movies_api import app

# Create a TestClient
client = TestClient(app)

# Test for cantidad_filmaciones_mes endpoint
def test_cantidad_filmaciones_mes():
    response = client.get('/cantidad_filmaciones_mes/enero')
    assert response.status_code == 200
    assert "cantidad de películas fueron estrenadas en el mes de enero" in response.json()["mensaje"]

# Test for cantidad_filmaciones_dia endpoint
def test_cantidad_filmaciones_dia():
    response = client.get('/cantidad_filmaciones_dia/lunes')
    assert response.status_code == 200
    assert "cantidad de películas fueron estrenadas en los días lunes" in response.json()["mensaje"]

# Test for score_titulo endpoint
def test_score_titulo():
    response = client.get('/score_titulo/Toy Story')
    assert response.status_code == 200
    assert "La película Toy Story fue estrenada en el año" in response.json()["mensaje"]

# Test for votos_titulo endpoint
def test_votos_titulo():
    response = client.get('/votos_titulo/Toy Story')
    assert response.status_code == 200
    assert "La película Toy Story fue estrenada en el año" in response.json()["mensaje"] or "No cumple con la condición de tener al menos 2000 valoraciones" in response.json()["mensaje"]

# Test for get_actor endpoint
def test_get_actor():
    response = client.get('/get_actor/Tom Hanks')
    assert response.status_code == 200
    assert "El actor Tom Hanks ha participado de" in response.json()["mensaje"]

# Test for get_director endpoint
def test_get_director():
    response = client.get('/get_director/Steven Spielberg')
    assert response.status_code == 200
    assert "director" in response.json()
    assert "peliculas" in response.json()
