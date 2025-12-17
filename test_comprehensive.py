"""Comprehensive test with many examples"""

from brain.intent.parser import IntentParser
from brain.kernel import RobotBrainKernel
from brain.world.state import WorldState
from brain.world.objects import WorldObject


def main():
    print("="*80)
    print("COMPREHENSIVE TEST - 30+ EXAMPLES")
    print("="*80)
    
    parser = IntentParser()
    kernel = RobotBrainKernel()
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living room",
        human_location="living room",
        locations=["kitchen", "living room", "bedroom"]
    )
    
    tests = [
        # Thirst variations
        ("im dying of thirst", "Thirst"),
        ("im so thirsty", "Thirst"),
        ("i need water", "Thirst"),
        ("im parched", "Thirst"),
        
        # Hunger variations
        ("im starving", "Hunger"),
        ("im so hungry", "Hunger"),
        ("i need food", "Hunger"),
        
        # Entertainment
        ("tell me a joke", "Entertainment"),
        ("tell me something funny", "Entertainment"),
        ("make me laugh", "Entertainment"),
        ("say something funny", "Entertainment"),
        
        # Greetings
        ("hi", "Greeting"),
        ("hello", "Greeting"),
        ("hey whats up", "Greeting"),
        ("sup", "Greeting"),
        ("good morning", "Greeting"),
        
        # Emotions
        ("im stressed", "Emotion"),
        ("im so tired", "Emotion"),
        ("im sad", "Emotion"),
        ("im angry", "Emotion"),
        
        # Questions
        ("what is this", "Question"),
        ("where is my phone", "Question"),
        ("why is this happening", "Question"),
        ("how does this work", "Question"),
        
        # Tasks
        ("bring me water", "Task"),
        ("clean the room", "Task"),
        ("go to kitchen", "Navigation"),
        ("grab that cup", "Grasp"),
        ("explore bedroom", "Exploration"),
        
        # Social
        ("thank you", "Gratitude"),
        ("thanks", "Gratitude"),
        ("how are you", "Status"),
        ("help me", "Collaboration"),
    ]
    
    print(f"\n{'Command':<35} {'Category':<15} {'Action':<20} {'Works'}")
    print("-"*80)
    
    success = 0
    for cmd, cat in tests:
        goal = parser.parse(cmd)
        works = "YES" if goal.action != "respond" else "FALLBACK"
        if works == "YES":
            success += 1
        print(f"{cmd:<35} {cat:<15} {goal.action:<20} {works}")
    
    print("\n" + "="*80)
    print(f"SUCCESS RATE: {success}/{len(tests)} ({success*100//len(tests)}%)")
    print("="*80)
    
    # Test full execution
    print("\nFULL EXECUTION EXAMPLES:\n")
    
    exec_tests = [
        "im dying of thirst",
        "tell me something funny",
        "hey whats up",
        "im stressed",
        "explore kitchen"
    ]
    
    for cmd in exec_tests:
        print(f"\nCommand: '{cmd}'")
        plan = kernel.process(cmd, world)
        print(f"Actions: {len(plan)}")
        for i, action in enumerate(plan, 1):
            print(f"  {i}. {action.action_type}({action.target or action.location or ''})")


if __name__ == "__main__":
    main()
