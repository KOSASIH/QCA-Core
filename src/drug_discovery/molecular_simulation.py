# src/drug_discovery/molecular_simulation.py

import numpy as np
import matplotlib.pyplot as plt
from numba import jit, prange
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class MolecularDynamics:
    def __init__(self, num_particles, box_size, time_step, num_steps, temperature):
        self.num_particles = num_particles
        self.box_size = box_size
        self.time_step = time_step
        self.num_steps = num_steps
        self.temperature = temperature
        self.positions = np.random.rand(num_particles, 3) * box_size
        self.velocities = np.random.randn(num_particles, 3) * np.sqrt(temperature)
        self.trajectory = []

    @staticmethod
    @jit(nopython=True, parallel=True)
    def lennard_jones_potential(r):
        """Calculate the Lennard-Jones potential."""
        return 4 * ((1 / r)**12 - (1 / r)**6)

    @staticmethod
    @jit(nopython=True, parallel=True)
    def compute_forces(positions, box_size):
        """Compute forces on particles based on Lennard-Jones potential."""
        num_particles = positions.shape[0]
        forces = np.zeros_like(positions)
        for i in prange(num_particles):
            for j in range(i + 1, num_particles):
                r_vec = positions[j] - positions[i]
                r_vec -= np.round(r_vec / box_size) * box_size  # Periodic boundary conditions
                r = np.linalg.norm(r_vec)
                if r < 2.5:  # Only consider interactions within a cutoff distance
                    force_magnitude = MolecularDynamics.lennard_jones_potential(r)
                    forces[i] += force_magnitude * (r_vec / r)
                    forces[j] -= force_magnitude * (r_vec / r)
        return forces

    def apply_thermostat(self):
        """Apply a simple velocity rescaling thermostat."""
        kinetic_energy = 0.5 * np.sum(self.velocities**2)
        current_temperature = (2 / 3) * (kinetic_energy / self.num_particles)
        scaling_factor = np.sqrt(self.temperature / current_temperature)
        self.velocities *= scaling_factor

    def simulate(self):
        """Run the molecular dynamics simulation."""
        for step in range(self.num_steps):
            forces = self.compute_forces(self.positions, self.box_size)
            self.velocities += forces * self.time_step
            self.positions += self.velocities * self.time_step
            self.positions %= self.box_size  # Apply periodic boundary conditions
            self.apply_thermostat()  # Control temperature
            self.trajectory.append(self.positions.copy())
        return np.array(self.trajectory)

    def plot_trajectory(self):
        """Plot the trajectory of the particles."""
        trajectory = np.array(self.trajectory)
        for i in range(self.num_particles):
            plt.plot(trajectory[:, i, 0], trajectory[:, i, 1], label=f'Particle {i}')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Molecular Dynamics Simulation Trajectory')
        plt.legend()
        plt.show()

    def save_trajectory(self, filename='trajectory.npy'):
        """Save the trajectory data to a file."""
        np.save(filename, self.trajectory)
        logging.info(f"Trajectory saved to {filename}.")

# Example usage
if __name__ == "__main__":
    md_simulation = MolecularDynamics(num_particles=10, box_size=10.0, time_step=0.01, num_steps=1000, temperature=300)
    trajectory = md_simulation.simulate()
    md_simulation.plot_trajectory()
    md_simulation.save_trajectory()
