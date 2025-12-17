# LLM Testing Guide

## Quick Tests

### 1. Basic LLM Test
```bash
python test_llm_robot.py
```
**What it does:** Tests 10 commands, shows LLM parsing results

**Expected output:**
```
Command: "yo grab me that thing"
Action: grasp, Target: unknown

Command: "I'm super thirsty dude"  
Plan: 4 actions (brings water)
```

### 2. Side-by-Side Comparison
```bash
python compare_parsers.py
```
**What it does:** Compares rule-based vs LLM parsing

**Expected output:**
```
Command                  Rule-Based    LLM
yo grab that thing       grasp         grasp
can u help              respond       respond
```

### 3. Interactive Chat
```bash
python chat_with_robot.py
```
**What it does:** Chat with robot in real-time

**Try these:**
- "yo bring me water"
- "I'm kinda thirsty"
- "can u help me find my phone"
- "make me a sammich plz"

### 4. Original Demo
```bash
python -m demos.llm_intent_demo
```
**What it does:** Shows LLM handling slang/typos

### 5. CLI with LLM
First, enable LLM in kernel:
```python
# Edit brain/kernel.py
from brain.intent.llm_parser import LLMIntentParser

class RobotBrainKernel:
    def __init__(self):
        self.intent_parser = LLMIntentParser(use_llm=True)
```

Then test:
```bash
python cli/run.py "yo bring me that thing"
python cli/run.py "I'm super thirsty dude"
```

## Test Commands

### Easy (Both Work)
- "bring me water"
- "hi"
- "clean room"
- "go to kitchen"

### Medium (Rules OK, LLM Better)
- "I'm thirsty"
- "what is this"
- "help me"

### Hard (Rules Fail, LLM Succeeds)
- "yo grab that thing"
- "can u help me out"
- "make me a sammich plz"
- "dude where's my phone"
- "I'm kinda tired maybe"
- "what the hell is going on"

## Verify Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Or in Python
python -c "import requests; print('Ollama:', 'Running' if requests.get('http://localhost:11434/api/tags').status_code == 200 else 'Not running')"
```

## Troubleshooting

### "Ollama not detected"
```bash
# Start Ollama
ollama serve

# Pull model if needed
ollama pull llama3.2
```

### "LLM error: timeout"
- Ollama might be slow on first run
- Increase timeout in `llm_parser.py` (line 60): `timeout=10`

### "Model not found"
```bash
# Check available models
ollama list

# Pull llama3.2 if missing
ollama pull llama3.2
```

## Performance Testing

```python
import time
from brain.intent.llm_parser import LLMIntentParser

parser = LLMIntentParser(use_llm=True)

# Test speed
start = time.time()
goal = parser.parse("bring me water")
print(f"Time: {(time.time() - start)*1000:.0f}ms")

# Expected: 50-200ms with LLM, <1ms with rules
```

## Integration Test

```python
# Full end-to-end test
from brain.kernel import RobotBrainKernel
from brain.intent.llm_parser import LLMIntentParser
from brain.world.state import WorldState
from brain.world.objects import WorldObject

# Setup
kernel = RobotBrainKernel()
kernel.intent_parser = LLMIntentParser(use_llm=True)

world = WorldState(
    objects=[WorldObject("water", "kitchen", "liquid")],
    robot_location="living room",
    human_location="living room",
    locations=["kitchen", "living room"]
)

# Test
commands = [
    "yo bring me water",
    "I'm super thirsty dude",
    "can u help me find stuff"
]

for cmd in commands:
    plan = kernel.process(cmd, world)
    print(f"{cmd} -> {len(plan)} actions")
```

## Next Steps

1. ✅ Run `python test_llm_robot.py` - See it work
2. ✅ Run `python chat_with_robot.py` - Interactive test
3. ✅ Run `python compare_parsers.py` - See the difference
4. 🔧 Enable in kernel - Edit `brain/kernel.py`
5. 🚀 Deploy - Use LLM in production

## Results You Should See

**With Ollama running:**
- "yo grab that thing" → ✅ Works
- "I'm kinda thirsty" → ✅ Brings water
- "can u help" → ✅ Collaborates
- Response time: 50-200ms

**Without Ollama:**
- Falls back to rule-based
- Some commands fail
- Response time: <1ms
