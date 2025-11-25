import requests
import random

BASE = "https://qa-internship.avito.com/api/1"

def gen_seller():
    return random.randint(111111, 999999)

def create_item(payload):
    return requests.post(f"{BASE}/item", json=payload)

def test_create_item_success():
    payload = {
        "title": "Laptop",
        "description": "Good laptop",
        "price": 50000,
        "sellerId": gen_seller()
    }
    r = create_item(payload)
    assert r.status_code == 200
    assert "id" in r.json()

def test_create_item_no_title():
    payload = {
        "description": "aaa",
        "price": 100,
        "sellerId": gen_seller()
    }
    r = create_item(payload)
    assert r.status_code == 400

def test_get_existing_item():
    payload = {
        "title": "Test",
        "description": "Test",
        "price": 100,
        "sellerId": gen_seller()
    }
    created = create_item(payload).json()
    item_id = created["id"]

    r = requests.get(f"{BASE}/item/{item_id}")
    assert r.status_code == 200
    assert r.json()["title"] == payload["title"]

def test_get_item_not_found():
    r = requests.get(f"{BASE}/item/99999999")
    assert r.status_code in (404, 400)

def test_get_seller_items():
    seller = gen_seller()
    create_item({"title": "T1", "description": "d", "price": 1, "sellerId": seller})
    create_item({"title": "T2", "description": "d", "price": 2, "sellerId": seller})

    r = requests.get(f"{BASE}/seller/{seller}")
    assert r.status_code == 200
    assert len(r.json()) >= 2

def test_get_seller_invalid():
    r = requests.get(f"{BASE}/seller/1")
    assert r.status_code == 400

def test_stat_nonexistent():
    r = requests.get(f"{BASE}/stat/123456789")
    assert r.status_code in (404, 400)
