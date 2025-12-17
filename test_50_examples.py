"""Test with 50+ diverse examples"""

from brain.intent.parser import IntentParser


def main():
    print("="*80)
    print("ULTIMATE TEST - 50+ EXAMPLES")
    print("="*80)

    parser = IntentParser()

    tests = [
        # Thirst (10 variations)
        "im dying of thirst",
        "im so thirsty",
        "i need water",
        "im parched",
        "im dehydrated",
        "need a drink",
        "get me water",
        "can i have water",
        "water please",
        "bring water",

        # Hunger (7 variations)
        "im starving",
        "im so hungry",
        "i need food",
        "im famished",
        "need to eat",
        "get me food",
        "bring me food",

        # Entertainment (8 variations)
        "tell me a joke",
        "tell me something funny",
        "make me laugh",
        "say something funny",
        "entertain me",
        "amuse me",
        "cheer me up",
        "do something fun",

        # Greetings (8 variations)
        "hi",
        "hello",
        "hey",
        "whats up",
        "sup",
        "howdy",
        "yo",
        "good morning",

        # Emotions (9 variations)
        "im stressed",
        "im tired",
        "im sad",
        "im angry",
        "im upset",
        "im anxious",
        "im worried",
        "im depressed",
        "im exhausted",

        # Questions (5 variations)
        "what is this",
        "where is my phone",
        "why is this happening",
        "how does this work",
        "when will this be done",

        # Tasks (8 variations)
        "bring me water",
        "clean the room",
        "go to kitchen",
        "grab that cup",
        "explore bedroom",
        "help me",
        "teach me python",
        "thank you",
    ]

    print(f"\nTesting {len(tests)} commands...\n")

    success = 0
    fallback = 0

    for cmd in tests:
        goal = parser.parse(cmd)
        if goal.action != "respond":
            success += 1
            status = "OK"
        else:
            fallback += 1
            status = "FALLBACK"

        print(f"{cmd:<35} -> {goal.action:<20} [{status}]")

    print("\n" + "="*80)
    print("RESULTS:")
    print(f"  Success: {success}/{len(tests)} ({success*100//len(tests)}%)")
    print(f"  Fallback: {fallback}/{len(tests)} ({fallback*100//len(tests)}%)")
    print("="*80)

    if success == len(tests):
        print("\nPERFECT SCORE! All commands understood!")
    elif success >= len(tests) * 0.9:
        print("\nEXCELLENT! 90%+ success rate!")
    elif success >= len(tests) * 0.8:
        print("\nGOOD! 80%+ success rate!")
    else:
        print("\nNeeds improvement.")


if __name__ == "__main__":
    main()
