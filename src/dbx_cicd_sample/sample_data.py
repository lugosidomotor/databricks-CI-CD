"""Kicsi, determinisztikus bemeneti adat a tanulási példához."""

from __future__ import annotations

from typing import TypedDict


class RawOrder(TypedDict):
    order_id: str
    order_ts: str
    customer_id: str | None
    country: str
    amount: float
    status: str


RAW_ORDER_SCHEMA = (
    "order_id STRING, order_ts STRING, customer_id STRING, "
    "country STRING, amount DOUBLE, status STRING"
)


def sample_orders() -> list[RawOrder]:
    """Szándékosan tartalmaz duplikátumot és hibás rekordokat."""
    return [
        {
            "order_id": "O-1001",
            "order_ts": "2026-01-15T08:30:00Z",
            "customer_id": "C-001",
            "country": "HU",
            "amount": 100.0,
            "status": "COMPLETED",
        },
        {
            "order_id": "O-1002",
            "order_ts": "2026-01-15T09:10:00Z",
            "customer_id": "C-002",
            "country": "DE",
            "amount": 50.0,
            "status": "COMPLETED",
        },
        {
            "order_id": "O-1002",
            "order_ts": "2026-01-15T09:10:00Z",
            "customer_id": "C-002",
            "country": "DE",
            "amount": 50.0,
            "status": "COMPLETED",
        },
        {
            "order_id": "O-1003",
            "order_ts": "2026-01-16T10:00:00Z",
            "customer_id": "C-003",
            "country": "HU",
            "amount": 25.0,
            "status": "PENDING",
        },
        {
            "order_id": "O-1004",
            "order_ts": "2026-01-16T11:00:00Z",
            "customer_id": "C-004",
            "country": "AT",
            "amount": 75.0,
            "status": "CANCELLED",
        },
        {
            "order_id": "O-1005",
            "order_ts": "2026-01-16T12:00:00Z",
            "customer_id": "C-005",
            "country": "HU",
            "amount": -10.0,
            "status": "COMPLETED",
        },
        {
            "order_id": "O-1006",
            "order_ts": "2026-01-16T13:00:00Z",
            "customer_id": None,
            "country": "HU",
            "amount": 10.0,
            "status": "COMPLETED",
        },
    ]

