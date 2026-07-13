from __future__ import annotations
import pytest
from jobrun.parse import parse_jobs
from jobrun.plan import order_jobs
from jobrun.exec import run_jobs
from jobrun.report import summarize
from jobrun.pipeline import run

def test_parse():
    jobs=parse_jobs("b:a\na:\n#c\n")
    names={j["name"] for j in jobs}
    assert names=={"a","b"}
    b=[j for j in jobs if j["name"]=="b"][0]
    assert b["deps"]==["a"]

def test_order():
    jobs=[{"name":"b","deps":["a"]},{"name":"a","deps":[]},{"name":"c","deps":["a"]}]
    assert order_jobs(jobs)[0]=="a"

def test_cycle():
    with pytest.raises(ValueError):
        order_jobs([{"name":"a","deps":["b"]},{"name":"b","deps":["a"]}])

def test_pipeline():
    text="b:a\na:\n"
    out=run(text, lambda n: f"ok-{n}")
    assert out=="ok-a\nok-b\n"
