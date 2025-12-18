from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver


def test_choose_first():
    choose_first = ChooseFirstResolver()
    assert choose_first.resolve(["HP:123456", "HP:987654"]) == "HP:123456"
