"""Quick test: LLM-powered robot"""

from brain.intent.llm_parser import LLMIntentParser
from brain.kernel import RobotBrainKernel
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def test_llm_vs_rules():
    """Compare LLM vs rule-based parsing"""

    print("="*70)
    print("TESTING LLM-POWERED ROBOT")
    print("="*70)

    # Setup
    llm_parser = LLMIntentParser(use_llm=True)

    if llm_parser.llm_available:
        print("\nOllama detected! Testing LLM parsing...\n")
    else:
        print("\nOllama not running. Using rule-based fallback.\n")
        print("To enable LLM:")
        print("  1. Install: https://ollama.com/download")
        print("  2. Run: ollama pull llama3.2")
        print("  3. Run: ollama serve\n")

    # Test cases
    test_commands = [
        # Easy (rules work)
        "bring me water",
        "hi",
        "clean room",

        # Hard (rules fail, LLM succeeds)
        "yo grab me that thing over there",
        "I'm kinda thirsty maybe",
        "can u help me out",
        "dude where's my phone",
        "make me a sammich plz",
        "what the hell is going on",
    ]

    print(f"{'Command':<40} {'Action':<20} {'Target':<15}")
    print("-"*70)

    for cmd in test_commands:
        goal = llm_parser.parse(cmd)
        print(f"{cmd:<40} {goal.action:<20} {goal.target or 'None':<15}")

    print("\n" + "="*70)
    print("FULL ROBOT TEST")
    print("="*70)

    # Test with full kernel
    kernel = RobotBrainKernel()
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living room",
        human_location="living room",
        locations=["kitchen", "living room"]
    )

    # Replace parser with LLM
    kernel.intent_parser = llm_parser

    test_with_kernel = [
        "yo bring me water",
        "I'm super thirsty dude",
        "can u help me find my phone",
    ]

    for cmd in test_with_kernel:
        print(f"\nCommand: '{cmd}'")
        try:
            plan = kernel.process(cmd, world)
            print(f"Plan: {len(plan)} actions")
            for i, action in enumerate(plan, 1):
                print(f"  {i}. {action}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_llm_vs_rules()
