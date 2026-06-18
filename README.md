# Synthetic Photonic Lattice Simulation

This project simulates a synthetic nonlinear photonic lattice inspired by optical neural network architectures based on time-domain multiplexing.

The code evolves two complex pulse-amplitude arrays, corresponding to short-loop and long-loop pulse trains, through repeated roundtrips using nonlinear phase modulation, gain/phase parameters, and coupler mixing.

## Project purpose

The goal of this project is to reproduce the basic pulse evolution of a synthetic photonic lattice and explore how multiple pairs of loops could be connected to create a more complex optical neural network architecture.

## Files

- `spl_simulation.py`: Main simulation code.
- `outputs/`: Example generated plots.
- `docs/report.pdf`: Background report explaining the physical setup and motivation.

## How to run

Install the dependencies:

```bash
pip install -r requirements.txt
