"""
Quantum Circuit (Hadamard superposition) with Qiskit

DO NOT commit IBM Quantum API tokens to GitHub.
"""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, execute
from qiskit.visualization import plot_histogram, plot_bloch_multivector

OUT_DIR = Path(__file__).resolve().parent / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main(shots: int = 1024) -> None:
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    fig = qc.draw(output="mpl")
    fig.savefig(OUT_DIR / "01_circuit.png", dpi=200)
    plt.close(fig)

    print("OpenQASM:\n", qc.qasm())

    backend = Aer.get_backend("qasm_simulator")
    job = execute(qc, backend, shots=shots)
    counts = job.result().get_counts(qc)
    print("Counts:", counts)

    fig = plot_histogram(counts)
    fig.savefig(OUT_DIR / "02_histogram.png", dpi=200)
    plt.close(fig)

    qc_state = QuantumCircuit(1)
    qc_state.h(0)

    backend_sv = Aer.get_backend("statevector_simulator")
    state = execute(qc_state, backend_sv).result().get_statevector(qc_state)
    print("Statevector:", state)

    fig = plot_bloch_multivector(state)
    fig.savefig(OUT_DIR / "03_bloch.png", dpi=200)
    plt.close(fig)

    backend_u = Aer.get_backend("unitary_simulator")
    unitary = execute(qc_state, backend_u).result().get_unitary()
    print("Unitary:\n", unitary)

    print(f"Done. Figures saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
