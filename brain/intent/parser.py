from brain.intent.schema import Goal


class IntentParser:
    """Parse human commands into structured goals"""

    def parse(self, human_input: str) -> Goal:
        """Extract goal from natural language input"""
        text = human_input.lower().strip()

        if "bring" in text:
            target = self._extract_object(text)
            return Goal(action="bring", target=target, recipient="human")

        if "clean" in text and "room" in text:
            return Goal(action="clean", target="room")

        if "navigate" in text or "go to" in text:
            location = self._extract_location(text)
            return Goal(action="navigate", location=location)

        if "grasp" in text or "pick" in text or "grab" in text:
            target = self._extract_object(text)
            return Goal(action="grasp", target=target)

        return Goal(action="unknown", target=text)

    def _extract_location(self, text: str) -> str:
        for loc in ["kitchen", "bedroom", "living room", "bathroom"]:
            if loc in text:
                return loc
        return "unknown"

    def _extract_object(self, text: str) -> str:
        for obj in ["cup", "water", "bottle", "book", "phone"]:
            if obj in text:
                return obj
        return "unknown"
