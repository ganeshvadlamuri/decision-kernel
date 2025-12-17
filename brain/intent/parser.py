from brain.intent.schema import Goal


class IntentParser:
    """Parse human commands into structured goals"""

    def parse(self, human_input: str) -> Goal:
        """Extract goal from natural language input"""
        text = human_input.lower().strip()

        # Greetings & Social
        if text in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]:
            return Goal(action="greet", target="human")

        if "how are you" in text or "what's up" in text:
            return Goal(action="status_report", target="self")

        if "thank" in text or "thanks" in text:
            return Goal(action="acknowledge", target="gratitude")

        # Questions & Information
        if text.startswith("what") or text.startswith("where") or text.startswith("when"):
            return Goal(action="answer_question", target=text)

        if "explain" in text or "tell me about" in text:
            return Goal(action="explain", target=self._extract_object(text))

        # Emotional Intelligence
        if "stressed" in text or "tired" in text or "angry" in text or "sad" in text:
            return Goal(action="emotional_support", target="human")

        if "thirsty" in text:
            return Goal(action="bring", target="water", recipient="human")

        if "hungry" in text:
            return Goal(action="bring", target="food", recipient="human")

        # Learning & Training
        if "learn" in text or "remember" in text or "teach" in text:
            return Goal(action="learn_task", target=text)

        if "practice" in text or "improve" in text:
            return Goal(action="self_improve", target=text)

        # Exploration & Curiosity
        if "explore" in text or "discover" in text or "find" in text:
            location = self._extract_location(text)
            return Goal(action="explore", location=location)

        # Prediction & Planning
        if "predict" in text or "what will happen" in text:
            return Goal(action="predict_future", target=text)

        if "plan" in text and "for" in text:
            return Goal(action="create_plan", target=text)

        # Collaboration & Negotiation
        if "help me" in text or "assist" in text:
            return Goal(action="collaborate", target=text)

        if "negotiate" in text or "compromise" in text:
            return Goal(action="negotiate", target=text)

        # Complex tasks
        if "make coffee" in text or "brew coffee" in text:
            return Goal(action="make_coffee", target="coffee")

        if "deliver" in text and "package" in text:
            location = self._extract_location(text)
            return Goal(action="deliver_package", location=location)

        if "monitor" in text:
            location = self._extract_location(text)
            return Goal(action="monitor_area", location=location)

        if "charge" in text or "battery" in text:
            return Goal(action="charge", location="charging_station")

        # Emergency commands
        if "fire" in text and ("emergency" in text or "detected" in text):
            return Goal(action="emergency_fire")

        if "intrusion" in text and ("emergency" in text or "detected" in text):
            return Goal(action="emergency_intrusion")

        if "stop" in text or "halt" in text or "emergency stop" in text:
            return Goal(action="emergency_stop")

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

        if "release" in text or "drop" in text or "put down" in text:
            target = self._extract_object(text)
            return Goal(action="release", target=target)

        if "wait" in text or "pause" in text:
            return Goal(action="wait", target="pause")

        # Entertainment & Fun
        if "dance" in text or "sing" in text or "joke" in text or "play" in text:
            return Goal(action="entertain", target=text)

        # Capability questions
        if text.startswith("can you") or text.startswith("are you able"):
            return Goal(action="capability_check", target=text)

        # Emotional/Relationship
        if "love" in text or "friend" in text or "like me" in text:
            return Goal(action="emotional_response", target=text)

        # Smart fallback - ALWAYS respond
        return Goal(action="respond", target=text)

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
