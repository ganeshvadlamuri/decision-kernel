from brain.intent.parser import IntentParser


def test_parse_bring_water():
    parser = IntentParser()
    goal = parser.parse("bring me water")
    assert goal.action == "bring"
    assert goal.target == "water"
    assert goal.recipient == "human"


def test_parse_clean_room():
    parser = IntentParser()
    goal = parser.parse("clean the room")
    assert goal.action == "clean"
    assert goal.target == "room"


def test_parse_navigate():
    parser = IntentParser()
    goal = parser.parse("go to kitchen")
    assert goal.action == "navigate"
    assert goal.location == "kitchen"


def test_parse_grasp():
    parser = IntentParser()
    goal = parser.parse("pick up the cup")
    assert goal.action == "grasp"
    assert goal.target == "cup"
