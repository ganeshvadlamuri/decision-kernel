"""Compare rule-based vs LLM parsing side-by-side"""

from brain.intent.llm_parser import LLMIntentParser
from brain.intent.parser import IntentParser


def main():
    print("="*80)
    print("RULE-BASED vs LLM PARSER COMPARISON")
    print("="*80)

    rule_parser = IntentParser()
    llm_parser = LLMIntentParser(use_llm=True)

    if not llm_parser.llm_available:
        print("\nWARNING: Ollama not detected. LLM will fallback to rules.")
        print("Install Ollama to see the difference!\n")

    # Test cases
    tests = [
        # Easy cases (both work)
        ("bring me water", "Easy"),
        ("hi", "Easy"),
        ("clean room", "Easy"),

        # Medium (rules might struggle)
        ("I'm thirsty", "Medium"),
        ("what is this", "Medium"),
        ("help me", "Medium"),

        # Hard (rules fail, LLM succeeds)
        ("yo grab that thing", "Hard"),
        ("can u help", "Hard"),
        ("make me a sammich", "Hard"),
        ("dude where's my stuff", "Hard"),
        ("I'm kinda tired maybe", "Hard"),
    ]

    print(f"\n{'Command':<30} {'Level':<10} {'Rule-Based':<20} {'LLM':<20}")
    print("-"*80)

    for command, level in tests:
        rule_goal = rule_parser.parse(command)
        llm_goal = llm_parser.parse(command)

        rule_action = rule_goal.action
        llm_action = llm_goal.action

        # Highlight differences
        match = "SAME" if rule_action == llm_action else "DIFFERENT"
        marker = "" if match == "SAME" else " <--"

        print(f"{command:<30} {level:<10} {rule_action:<20} {llm_action:<20}{marker}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    if llm_parser.llm_available:
        print("LLM parser handles:")
        print("  - Slang and casual language")
        print("  - Typos and abbreviations")
        print("  - Vague references")
        print("  - Context and nuance")
        print("\nRule-based parser:")
        print("  - Fast but limited")
        print("  - Requires exact patterns")
        print("  - Fails on variations")
    else:
        print("Install Ollama to see LLM benefits:")
        print("  1. Visit: https://ollama.com/download")
        print("  2. Run: ollama pull llama3.2")
        print("  3. Run: ollama serve")


if __name__ == "__main__":
    main()
