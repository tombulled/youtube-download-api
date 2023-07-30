from ytd_api import utils


def test_flatten() -> None:
    assert utils.flatten(
        [
            {"a": "a-1", "b": "b-1", "c": "c-1"},
            {"a": "a-2", "b": "b-2", "c": "c-2"},
        ]
    ) == {
        "a": ["a-1", "a-2"],
        "b": ["b-1", "b-2"],
        "c": ["c-1", "c-2"],
    }
