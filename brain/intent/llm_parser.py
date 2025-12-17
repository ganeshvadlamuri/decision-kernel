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

        # Ultra-short prompt for speed
        prompt = f"""Convert to JSON:
"{text}"

thirsty->bring water, funny->entertain joke, hi->greet, stressed->emotional_support

JSON:"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",  # Faster model
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 50  # Limit output length for speed
                    }
                },
                timeout=5  # Shorter timeout
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
