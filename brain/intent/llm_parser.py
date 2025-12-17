"""LLM-powered intent parser using open-source models"""

from brain.intent.schema import Goal


class LLMIntentParser:
    """Parse intents using open-source LLM (Ollama/Llama)"""

    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.llm_available = False

        if use_llm:
            try:
                import requests
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
        import requests

        prompt = f"""You are a robot assistant. Parse this command into a structured action.

Command: "{text}"

Respond with ONLY a JSON object with these fields:
- action: one of [bring, clean, navigate, grasp, release, greet, speak, explore, learn_task, emotional_support, entertain, capability_check, answer_question]
- target: the object/topic (or null)
- location: the location (or null)

Examples:
"bring me water" -> {{"action": "bring", "target": "water", "location": null}}
"hi" -> {{"action": "greet", "target": "human", "location": null}}
"go to kitchen" -> {{"action": "navigate", "target": null, "location": "kitchen"}}
"tell me a joke" -> {{"action": "entertain", "target": "joke", "location": null}}

Now parse: "{text}"
JSON:"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",  # or "mistral", "phi3"
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1}
                },
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                llm_output = result.get("response", "")

                # Parse JSON from LLM
                import json
                import re
                json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return Goal(
                        action=parsed.get("action", "respond"),
                        target=parsed.get("target"),
                        location=parsed.get("location")
                    )
        except Exception as e:
            print(f"LLM error: {e}")

        # Fallback
        return self._parse_rule_based(text)

    def _parse_rule_based(self, text: str) -> Goal:
        """Fallback to rule-based parsing"""
        from brain.intent.parser import IntentParser
        parser = IntentParser()
        return parser.parse(text)
