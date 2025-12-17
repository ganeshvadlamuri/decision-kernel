"""Interactive chat with LLM-powered robot"""

from brain.intent.llm_parser import LLMIntentParser
from brain.kernel import RobotBrainKernel
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def main():
    print("="*70)
    print("CHAT WITH LLM-POWERED ROBOT")
    print("="*70)

    # Setup
    llm_parser = LLMIntentParser(use_llm=True)
    kernel = RobotBrainKernel()
    kernel.intent_parser = llm_parser

    world = WorldState(
        objects=[
            WorldObject("water", "kitchen", "liquid"),
            WorldObject("cup", "kitchen", "container"),
            WorldObject("phone", "bedroom", "device"),
        ],
        robot_location="living room",
        human_location="living room",
        locations=["kitchen", "living room", "bedroom"]
    )

    if llm_parser.llm_available:
        print("\nLLM Mode: ON (Ollama detected)")
        print("Try slang, typos, casual language!\n")
    else:
        print("\nLLM Mode: OFF (using rule-based fallback)")
        print("Install Ollama for better understanding.\n")

    print("Type your commands (or 'quit' to exit):")
    print("-"*70)

    while True:
        try:
            command = input("\nYou: ").strip()

            if command.lower() in ['quit', 'exit', 'bye']:
                print("Robot: Goodbye!")
                break

            if not command:
                continue

            # Parse and plan
            goal = llm_parser.parse(command)
            print(f"[Parsed: action={goal.action}, target={goal.target}]")

            plan = kernel.process(command, world)

            if plan:
                print(f"Robot: Executing {len(plan)} actions:")
                for i, action in enumerate(plan, 1):
                    print(f"  {i}. {action}")
            else:
                print("Robot: I'm not sure how to do that.")

        except KeyboardInterrupt:
            print("\n\nRobot: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
