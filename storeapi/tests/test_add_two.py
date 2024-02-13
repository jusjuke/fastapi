def test_add_two():
    x = 2
    y = 3
    assert x + y == 5


def test_dict_contains():
    d = {"a": 1, "b": 2}
    assert "a" in d
    assert "b" in d
    assert "c" not in d
    expected = {"a": 1}
    assert expected.items() <= d.items()
