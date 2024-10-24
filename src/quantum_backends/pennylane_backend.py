# pennylane_backend.py

import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt

class PennylaneBackend:
    def __init__(self, num_wires, device_name='default.qubit', wires=None):
        self.num_wires = num_wires
        self.device_name = device_name
        self.wires = wires if wires else range(num_wires)
        self.dev = qml.device(device_name, wires=self.wires)

    def create_circuit(self, gate_error=0.01, readout_error=0.05):
        """Create a simple quantum circuit with noise models."""
        @qml.qnode(self.dev)
        def circuit():
            for i in range(self.num_wires):
                qml.Hadamard(wires=i)
            for i in range(self.num_wires):
                qml.measure(wires=i)
            return [qml.probs(wires=i) for i in range(self.num_wires)]
        return circuit

    def execute_circuit(self, circuit, shots=1024):
        """Execute the quantum circuit with noise models and return results."""
        start_time = time.time()
        result = circuit()
        end_time = time.time()

        probs = [result[i][1] for i in range(self.num_wires)]
        logging.info(f"Execution Time: {end_time - start_time:.6f} seconds")
        return probs

    def visualize_results(self, probs):
        """Visualize the results of the quantum circuit."""
        plt.bar(range(2**self.num_wires), probs)
        plt.xlabel('Outcome')
        plt.ylabel('Probability')
        plt.show()

    def visualize_noise_model(self):
        """Visualize the noise model."""
        if self.dev.noise_model:
            plt.imshow(self.dev.noise_model.noise_matrix, cmap='hot', interpolation='nearest')
            plt.xlabel('Qubit Index')
            plt.ylabel('Error Type')
            plt.title('Noise Model')
            plt.show()

# Example usage
if __name__ == "__main__":
    pennylane_backend = PennylaneBackend(3)
    circuit = pennylane_backend.create_circuit()
    probs = pennylane_backend.execute_circuit(circuit)
    pennylane_backend.visualize_results(probs)
    pennylane_backend.visualize_noise_model()
