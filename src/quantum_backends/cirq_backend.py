# quantum_backends/cirq_backend.py

import cirq
import numpy as np
import matplotlib.pyplot as plt

class CirqBackend:
 def __init__(self, num_qubits, noise_model=None):
        self.num_qubits = num_qubits
        self.noise_model = noise_model
        self.simulator = cirq.Simulator(noise=self.noise_model)

    def create_circuit(self, gate_error=0.01, readout_error=0.05):
        """Create a simple quantum circuit with noise models."""
        circuit = cirq.Circuit()
        qubits = [cirq.GridQubit(0, i) for i in range(self.num_qubits)]
        circuit.append(cirq.H.on_each(*qubits))  # Apply Hadamard gates
        circuit.append(cirq.measure(*qubits, key='z'))  # Measure all qubits
        return circuit

    def execute_circuit(self, circuit):
        """Execute the quantum circuit with noise models and return results."""
        start_time = time.time()
        result = self.simulator.run(circuit, repetitions=1024)
        end_time = time.time()

        counts = result.histogram(key='z')
        logging.info(f"Execution Time: {end_time - start_time:.6f} seconds")
        return counts

    def visualize_results(self, counts):
        """Visualize the results of the quantum circuit."""
        plt.bar(range(2**self.num_qubits), counts)
        plt.xlabel('Outcome')
        plt.ylabel('Frequency')
        plt.show()

    def visualize_noise_model(self):
        """Visualize the noise model."""
        if self.noise_model:
            plt.imshow(self.noise_model.noise_matrix, cmap='hot', interpolation='nearest')
            plt.xlabel('Qubit Index')
            plt.ylabel('Error Type')
            plt.title('Noise Model')
            plt.show()

# Example usage
if __name__ == "__main__":
    cirq_backend = CirqBackend(3)
    circuit = cirq_backend.create_circuit()
    counts = cirq_backend.execute_circuit(circuit)
    cirq_backend.visualize_results(counts)
    cirq_backend.visualize_noise_model()
