from brain.intent.schema import Goal
from brain.planner.planner import Planner
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def test_plan_bring():
    planner = Planner()
    goal = Goal(action="bring", target="water", recipient="human")
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        human_location="living room"
    )

    plan = planner.plan(goal, world)
    assert len(plan) == 4
    assert plan[0].action_type == "navigate_to"
    assert plan[1].action_type == "grasp"
    assert plan[2].action_type == "navigate_to"
    assert plan[3].action_type == "release"


def test_plan_navigate():
    planner = Planner()
    goal = Goal(action="navigate", location="kitchen")
    world = WorldState()

    plan = planner.plan(goal, world)
    assert len(plan) == 1
    assert plan[0].action_type == "navigate_to"
    assert plan[0].location == "kitchen"
