from collections import Counter

from dbx_cicd_sample.sample_data import RAW_ORDER_SCHEMA, sample_orders


def test_sample_data_contains_expected_training_cases() -> None:
    rows = sample_orders()
    counts = Counter(row["order_id"] for row in rows)

    assert len(rows) == 7
    assert counts["O-1002"] == 2
    assert any(row["amount"] < 0 for row in rows)
    assert any(row["customer_id"] is None for row in rows)
    assert any(row["status"] == "CANCELLED" for row in rows)


def test_valid_sample_orders_have_expected_business_total() -> None:
    unique = {}
    for row in sample_orders():
        if (
            row["amount"] > 0
            and row["customer_id"] is not None
            and row["status"] in {"COMPLETED", "PENDING"}
        ):
            unique[row["order_id"]] = row

    assert len(unique) == 3
    assert sum(row["amount"] for row in unique.values()) == 175.0
    assert "order_id STRING" in RAW_ORDER_SCHEMA

