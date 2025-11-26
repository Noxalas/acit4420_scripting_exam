import pytest
from conway.rules import RuleSet


def test_ruleset_conway_alive_survive():
    ruleset = RuleSet("B3/S23")
    assert ruleset.evaluate(True, 2) == "survive"
    assert ruleset.evaluate(True, 3) == "survive"
    assert ruleset.evaluate(True, 1) == "die"
    assert ruleset.evaluate(True, 4) == "die"


def test_ruleset_conway_dead_born():
    """Dead cell is born if neighbors in B"""
    ruleset = RuleSet("B3/S23")
    assert ruleset.evaluate(False, 3) == "born"
    assert ruleset.evaluate(False, 2) == "die"
    assert ruleset.evaluate(False, 4) == "die"


def test_ruleset_highlife():
    """Test HighLife (B36/S23) rule"""
    ruleset = RuleSet("B36/S23")
    assert ruleset.evaluate(False, 3) == "born"
    assert ruleset.evaluate(False, 6) == "born"
    assert ruleset.evaluate(False, 4) == "die"


def test_ruleset_invalid_format():
    """Invalid rule strings should raise ValueError"""
    with pytest.raises(ValueError):
        RuleSet(None)

    with pytest.raises(ValueError):
        RuleSet("3/S23")

    with pytest.raises(ValueError):
        RuleSet("B3/23")

    with pytest.raises(ValueError):
        RuleSet("B3S23")
