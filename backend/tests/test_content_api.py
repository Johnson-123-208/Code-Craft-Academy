from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_courses() -> None:
    response = client.get("/api/courses")
    assert response.status_code == 200
    courses = response.json()
    assert isinstance(courses, list)
    assert len(courses) >= 5
    slugs = {c["slug"] for c in courses}
    assert "python" in slugs
    assert "dsa" in slugs


def test_get_course_python() -> None:
    response = client.get("/api/courses/python")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "python"
    assert "modules" in data


def test_get_lesson() -> None:
    response = client.get("/api/lessons/python-intro-and-setup")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "python-intro-and-setup"
    assert len(data["content"]) > 100


def test_list_problems() -> None:
    response = client.get("/api/problems")
    assert response.status_code == 200
    problems = response.json()
    assert len(problems) >= 1


def test_search() -> None:
    response = client.get("/api/search", params={"q": "python"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["query"] == "python"
