"""LLM-powered intent parser using open-source models"""

from brain.intent.schema import Goal


class LLMIntentParser:
    """Parse intents using open-source LLM (Ollama/Llama)"""

    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.llm_available = False

        if use_llm:
            try:
                import requests  # type: ignore
                # Check if Ollama is running
                response = requests.get("http://localhost:11434/api/tags", timeout=1)
                self.llm_available = response.status_code == 200
            except Exception:
                self.llm_available = False

    def parse(self, human_input: str) -> Goal:
        """Parse using LLM if available, fallback to rule-based"""

        if self.llm_available:
            return self._parse_with_llm(human_input)
        else:
            return self._parse_rule_based(human_input)

    def _parse_with_llm(self, text: str) -> Goal:
        """Use Ollama/Llama to understand intent"""
        import requests  # type: ignore

        # Ultra-minimal prompt for speed
        prompt = f"""Command: {text}
Action (bring/greet/entertain/emotional_support/explore/navigate/grasp): """

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",  # Faster model
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.0,
                        "num_predict": 10,  # Very short output
                        "top_k": 1  # Greedy decoding for speed
                    }
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                llm_output = result.get("response", "").strip().lower()

                # Parse simple action word from LLM
                action_map = {
                    "bring": "bring",
                    "greet": "greet",
                    "entertain": "entertain",
                    "emotional": "emotional_support",
                    "explore": "explore",
                    "navigate": "navigate",
                    "grasp": "grasp",
                    "help": "collaborate",
                    "question": "answer_question"
                }

                # Find matching action
                for key, action in action_map.items():
                    if key in llm_output:
                        # Infer target based on action
                        target = None
                        if action == "bring":
                            if "thirst" in text.lower() or "water" in text.lower():
                                target = "water"
                            elif "hungry" in text.lower() or "food" in text.lower():
                                target = "food"
                        elif action == "entertain":
                            target = "joke"
                        elif action == "greet":
                            target = "human"

                        return Goal(action=action, target=target, location=None)
        except Exception:
            pass  # Silent fallback to rules

        # Fallback
        return self._parse_rule_based(text)

    def _parse_rule_based(self, text: str) -> Goal:
        """Fallback to rule-based parsing"""
        from brain.intent.parser import IntentParser
        parser = IntentParser()
        return parser.parse(text)
