# LLM Integration Guide

## Why Use LLM?

**Problems with Rule-Based Parser:**
- Limited to predefined patterns
- Can't understand context or nuance
- Fails on creative/unusual commands
- No learning from interactions

**Benefits of LLM:**
- ✅ Understands ANY command naturally
- ✅ Handles typos, slang, context
- ✅ Creative interpretation
- ✅ Multi-language support
- ✅ Learns from examples

## Quick Start

### Option 1: Ollama (Recommended - Free & Local)

**Install Ollama:**
```bash
# Windows/Mac/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from: https://ollama.com/download
```

**Pull a model:**
```bash
# Small & fast (1.3GB)
ollama pull llama3.2

# Or alternatives:
ollama pull mistral      # 4GB
ollama pull phi3         # 2GB
ollama pull gemma2       # 2GB
```

**Start Ollama:**
```bash
ollama serve
```

**Use LLM parser:**
```python
from brain.intent.llm_parser import LLMIntentParser

parser = LLMIntentParser(use_llm=True)
goal = parser.parse("yo robot, grab me that thing over there")
# Works! LLM understands slang and vague references
```

### Option 2: Hugging Face Transformers (Local)

```bash
pip install transformers torch
```

```python
from transformers import pipeline

# Use small model (1GB)
classifier = pipeline("text-classification", model="distilbert-base-uncased")

def parse_with_hf(text):
    result = classifier(text)
    # Map to robot actions
    return Goal(action=result[0]['label'])
```

### Option 3: OpenAI API (Cloud - Costs Money)

```bash
pip install openai
```

```python
import openai

openai.api_key = "your-key"

def parse_with_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Parse robot command: {text}"}]
    )
    return response.choices[0].message.content
```

## Comparison

| Method | Size | Speed | Cost | Offline | Quality |
|--------|------|-------|------|---------|---------|
| **Ollama (llama3.2)** | 1.3GB | Fast | Free | ✅ Yes | Excellent |
| **Ollama (mistral)** | 4GB | Fast | Free | ✅ Yes | Excellent |
| **HuggingFace** | 1GB | Medium | Free | ✅ Yes | Good |
| **OpenAI GPT-4** | Cloud | Fast | $$ | ❌ No | Best |
| **Rule-based** | 0KB | Instant | Free | ✅ Yes | Limited |

## Integration in Kernel

**Modify `brain/kernel.py`:**

```python
from brain.intent.llm_parser import LLMIntentParser

class RobotBrainKernel:
    def __init__(self, use_llm=True):
        # Use LLM if available, fallback to rules
        self.intent_parser = LLMIntentParser(use_llm=use_llm)
```

## Example Results

### Before (Rule-based):
```
"yo grab that thing" → Error: Empty plan
"I'm kinda thirsty maybe" → Error: Empty plan
"can u help" → Error: Empty plan
```

### After (LLM):
```
"yo grab that thing" → grasp(target=unknown)
"I'm kinda thirsty maybe" → bring(target=water)
"can u help" → collaborate(target=assist)
```

## Advanced: Fine-tune on Robot Data

```python
# Collect robot-specific data
data = [
    {"text": "bring water", "action": "bring", "target": "water"},
    {"text": "yo get me H2O", "action": "bring", "target": "water"},
    # ... 1000s more examples
]

# Fine-tune Llama
from transformers import AutoModelForCausalLM, Trainer

model = AutoModelForCausalLM.from_pretrained("llama3.2")
trainer = Trainer(model=model, train_dataset=data)
trainer.train()

# Now understands YOUR robot's specific commands!
```

## Hybrid Approach (Best)

```python
class HybridParser:
    def parse(self, text):
        # Try rule-based first (instant)
        if self.is_simple_command(text):
            return self.rule_based_parse(text)
        
        # Use LLM for complex/ambiguous
        return self.llm_parse(text)
```

## Performance

**Rule-based:** <1ms  
**Ollama (llama3.2):** 50-200ms  
**OpenAI GPT-4:** 500-2000ms  

**Recommendation:** Use Ollama for best balance of speed, quality, and privacy.

## Next Steps

1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull model: `ollama pull llama3.2`
3. Test: `python -m demos.llm_intent_demo`
4. Integrate: Update `brain/kernel.py` to use `LLMIntentParser`

## Resources

- Ollama: https://ollama.com
- Llama models: https://ollama.com/library/llama3.2
- Hugging Face: https://huggingface.co/models
- Fine-tuning guide: https://huggingface.co/docs/transformers/training
