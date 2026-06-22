import json

import pytest

from dbx_cicd_sample.common import TaskConfig, log_event, parse_task_config, quote_identifier


def test_parse_task_config_strips_values() -> None:
    config = parse_task_config(["--catalog", " main ", "--schema", " demo ", "--run-id", " 42 "])
    assert config == TaskConfig(catalog="main", schema="demo", run_id="42")


def test_table_reference_quotes_each_identifier() -> None:
    config = TaskConfig(catalog="main", schema="demo-schema", run_id="42")
    assert config.schema_ref == "`main`.`demo-schema`"
    assert config.table("gold`table") == "`main`.`demo-schema`.`gold``table`"


def test_quote_identifier_rejects_blank_value() -> None:
    with pytest.raises(ValueError, match="cannot be blank"):
        quote_identifier("   ")


def test_log_event_outputs_machine_readable_json(capsys: pytest.CaptureFixture[str]) -> None:
    log_event("test", count=3)
    assert json.loads(capsys.readouterr().out) == {"event": "test", "count": 3}
