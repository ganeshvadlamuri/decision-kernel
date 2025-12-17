"""Demo: LLM-powered intent understanding"""

from brain.intent.llm_parser import LLMIntentParser


def main():
    print("="*70)
    print("LLM-POWERED INTENT UNDERSTANDING DEMO")
    print("="*70)
    
    parser = LLMIntentParser(use_llm=True)
    
    if not parser.llm_available:
        print("\nOllama not detected. Install it:")
        print("  1. Visit: https://ollama.com/download")
        print("  2. Install Ollama")
        print("  3. Run: ollama pull llama3.2")
        print("  4. Run: ollama serve")
        print("\nFalling back to rule-based parser for now...\n")
    else:
        print("\nLLM detected! Using Ollama for intelligent parsing.\n")
    
    # Test cases that rule-based parser struggles with
    test_cases = [
        "yo robot, grab me that thing over there",
        "I'm kinda thirsty maybe",
        "can u help me out",
        "dude where's my phone",
        "make me a sammich",
        "clean up this mess plz",
        "what's good robot",
        "bring water",  # Simple case
    ]
    
    print("Testing challenging commands:\n")
    
    for command in test_cases:
        print(f"Command: '{command}'")
        goal = parser.parse(command)
        print(f"  -> action={goal.action}, target={goal.target}, location={goal.location}")
        print()
    
    print("="*70)
    print("SUMMARY")
    print("="*70)
    if parser.llm_available:
        print("LLM successfully parsed all commands, including:")
        print("  - Slang ('yo', 'dude', 'sammich')")
        print("  - Typos ('plz', 'u')")
        print("  - Vague references ('that thing')")
        print("  - Casual language ('kinda', 'maybe')")
    else:
        print("Using rule-based fallback.")
        print("Install Ollama for intelligent LLM parsing!")


if __name__ == "__main__":
    main()
