from brain.intent.schema import Goal


class IntentParser:
    """Parse human commands into structured goals"""

    def parse(self, human_input: str) -> Goal:
        """Extract goal from natural language input"""
        text = human_input.lower().strip()

        # Complex tasks
        if "make coffee" in text or "brew coffee" in text:
            return Goal(action="make_coffee", target="coffee")
        
        if "deliver" in text and "package" in text:
            location = self._extract_location(text)
            return Goal(action="deliver_package", location=location)
        
        if "monitor" in text:
            location = self._extract_location(text)
            return Goal(action="monitor_area", location=location)
        
        # Emergency commands
        if "fire" in text and ("emergency" in text or "detected" in text):
            return Goal(action="emergency_fire")
        
        if "intrusion" in text and ("emergency" in text or "detected" in text):
            return Goal(action="emergency_intrusion")

        # Basic tasks
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
        locations = [
            "kitchen", "bedroom", "living room", "bathroom",
            "warehouse", "charging_station", "storage", "office",
            "room_305", "exit", "safe_room"
        ]
        for loc in locations:
            if loc in text or loc.replace("_", " ") in text:
                return loc
        # Extract room numbers
        import re
        match = re.search(r'room\s*(\d+)', text)
        if match:
            return f"room_{match.group(1)}"
        return "unknown"

    def _extract_object(self, text: str) -> str:
        objects = [
            "cup", "water", "bottle", "book", "phone",
            "coffee", "package", "keys", "medicine", "table",
            "coffee_cup", "bean_bag", "water_container"
        ]
        for obj in objects:
            if obj in text or obj.replace("_", " ") in text:
                return obj
        return "unknown"
