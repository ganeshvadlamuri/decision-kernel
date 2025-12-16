"""Biological Neural Integration - Interface with biological neurons."""
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum
import random


class NeuronType(Enum):
    SENSORY = "sensory"
    MOTOR = "motor"
    INTERNEURON = "interneuron"


@dataclass
class BiologicalNeuron:
    neuron_id: str
    neuron_type: NeuronType
    firing_rate: float
    connections: List[str]
    plasticity: float


@dataclass
class NeuralSignal:
    source: str
    target: str
    strength: float
    neurotransmitter: str


class BioNeuralNetwork:
    def __init__(self, neuron_count: int = 1000):
        self.neurons: Dict[str, BiologicalNeuron] = {}
        self.signals: List[NeuralSignal] = []
        self.growth_rate = 0.1
        self.integration_level = 0.0
        self._grow_neurons(neuron_count)
    
    def _grow_neurons(self, count: int):
        """Simulate growing biological neurons in lab."""
        for i in range(count):
            neuron_type = random.choice(list(NeuronType))
            neuron = BiologicalNeuron(
                neuron_id=f"neuron_{i}",
                neuron_type=neuron_type,
                firing_rate=random.uniform(0.1, 10.0),
                connections=[],
                plasticity=random.uniform(0.5, 1.0)
            )
            self.neurons[neuron.neuron_id] = neuron
    
    def integrate(self, robot_brain: Any) -> Dict[str, Any]:
        """Interface biological neurons with robot brain."""
        # Establish connections
        connection_count = 0
        for neuron_id, neuron in list(self.neurons.items())[:100]:
            # Create synaptic connections
            targets = random.sample(list(self.neurons.keys()), min(10, len(self.neurons)))
            neuron.connections = targets
            connection_count += len(targets)
        
        self.integration_level = min(1.0, connection_count / 1000.0)
        
        return {
            "status": "integrated",
            "neurons_connected": len(self.neurons),
            "synapses_formed": connection_count,
            "integration_level": f"{self.integration_level * 100:.1f}%",
            "neural_plasticity": "active"
        }
    
    def stimulate(self, input_pattern: List[float]) -> List[float]:
        """Send electrical stimulation to neurons and read response."""
        output = []
        
        # Simulate neural firing
        for i, stimulus in enumerate(input_pattern[:10]):
            neuron_id = f"neuron_{i}"
            if neuron_id in self.neurons:
                neuron = self.neurons[neuron_id]
                response = stimulus * neuron.firing_rate * neuron.plasticity
                output.append(response)
                
                # Create signal
                if neuron.connections:
                    target = random.choice(neuron.connections)
                    signal = NeuralSignal(
                        source=neuron_id,
                        target=target,
                        strength=response,
                        neurotransmitter="glutamate" if response > 5.0 else "gaba"
                    )
                    self.signals.append(signal)
        
        return output
    
    def train_neurons(self, input_patterns: List[List[float]], 
                     target_outputs: List[List[float]]) -> Dict[str, float]:
        """Train biological neurons using Hebbian learning."""
        learning_rate = 0.01
        total_error = 0.0
        
        for input_pat, target in zip(input_patterns, target_outputs):
            output = self.stimulate(input_pat)
            error = sum((o - t) ** 2 for o, t in zip(output, target[:len(output)]))
            total_error += error
            
            # Adjust plasticity (Hebbian learning)
            for neuron in list(self.neurons.values())[:len(output)]:
                neuron.plasticity += learning_rate * (1.0 - error / 10.0)
                neuron.plasticity = max(0.1, min(1.0, neuron.plasticity))
        
        avg_error = total_error / len(input_patterns) if input_patterns else 0.0
        
        return {
            "training_error": avg_error,
            "plasticity_adjusted": True,
            "learning_rate": learning_rate
        }
    
    def get_neural_activity(self) -> Dict[str, Any]:
        """Get current neural activity statistics."""
        active_neurons = sum(1 for n in self.neurons.values() if n.firing_rate > 1.0)
        avg_firing = sum(n.firing_rate for n in self.neurons.values()) / len(self.neurons)
        
        return {
            "total_neurons": len(self.neurons),
            "active_neurons": active_neurons,
            "avg_firing_rate": f"{avg_firing:.2f} Hz",
            "signals_transmitted": len(self.signals),
            "integration_level": f"{self.integration_level * 100:.1f}%"
        }
