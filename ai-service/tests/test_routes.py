import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# ----------------------------
# HEALTH TEST
# ----------------------------

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200


# ----------------------------
# DESCRIBE TESTS
# ----------------------------

def test_describe_success(client):
    response = client.post("/describe", json={
        "text": "Cyber attack"
    })

    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_describe_invalid_input(client):
    response = client.post("/describe", json={})

    assert response.status_code == 400


def test_describe_empty_text(client):
    response = client.post("/describe", json={
        "text": ""
    })

    assert response.status_code == 400


# ----------------------------
# RECOMMEND TESTS
# ----------------------------

def test_recommend_success(client):
    response = client.post("/recommend", json={
        "text": "Banking fraud"
    })

    assert response.status_code == 200


def test_recommend_invalid_input(client):
    response = client.post("/recommend", json={})

    assert response.status_code == 400


# ----------------------------
# GENERATE REPORT TESTS
# ----------------------------

def test_generate_report_success(client):
    response = client.post("/generate-report", json={
        "text": "Cyber threat"
    })

    assert response.status_code == 200


def test_generate_report_invalid(client):
    response = client.post("/generate-report", json={})

    assert response.status_code == 400


# ----------------------------
# ANALYSE DOCUMENT TESTS
# ----------------------------

def test_analyse_document_success(client):
    response = client.post("/analyse-document", json={
        "text": "Suspicious transaction detected"
    })

    assert response.status_code == 200


def test_analyse_document_invalid(client):
    response = client.post("/analyse-document", json={})

    assert response.status_code == 400