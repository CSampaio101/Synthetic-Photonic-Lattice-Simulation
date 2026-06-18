import numpy as np
import matplotlib.pyplot as plt

# Number of roundtrips and pulses
M = 43
N = 21
NUM_STAGES = 10


def f(x, alpha):
    """Nonlinear phase response f(|x|^2) = exp(i alpha |x|^2)."""
    return np.exp(1j * alpha * np.abs(x) ** 2)


def normalize_complex(z, eps=1e-12):
    """Normalize a complex amplitude without dividing by zero."""
    mag = np.abs(z)
    if mag < eps:
        return 0.0 + 0.0j
    return z / mag


def F(U, V, phi, psi, alpha, gamma, theta):
    """
    Evolve the pulse amplitudes U and V through the synthetic photonic lattice.

    U[n, m] and V[n, m] store the complex amplitudes of the nth pulse after the
    mth roundtrip. This function updates U and V in-place.
    """
    num_pulses, num_roundtrips = U.shape

    for m in range(1, num_roundtrips):
        for n in range(num_pulses):
            n_left = (n - 1) % num_pulses
            n_right = (n + 1) % num_pulses

            u_update = np.exp(1j * phi[n, m - 1] + gamma[n, m - 1]) * (
                f(U[n_left, m - 1], alpha) * U[n_left, m - 1] * np.cos(theta[n_left, m - 1])
                + 1j * f(V[n_left, m - 1], alpha) * V[n_left, m - 1] * np.sin(theta[n_left, m - 1])
            )

            v_update = np.exp(1j * psi[n, m - 1]) * (
                f(V[n_right, m - 1], alpha) * V[n_right, m - 1] * np.cos(theta[n_right, m - 1])
                + 1j * f(U[n_right, m - 1], alpha) * U[n_right, m - 1] * np.sin(theta[n_right, m - 1])
            )

            # This keeps the amplitudes bounded, as in your original temporary fix.
            U[n, m] = normalize_complex(u_update)
            V[n, m] = normalize_complex(v_update)


# Create a dictionary of SPL stages.
d = {}
for i in range(NUM_STAGES):
    U = np.random.uniform(1, 1.5, (N, M)) + 1j * np.random.uniform(1, 1.5, (N, M))
    V = np.random.uniform(1, 1.5, (N, M)) + 1j * np.random.uniform(1, 1.5, (N, M))

    phi = np.ones((N, M), dtype=complex)
    psi = np.ones((N, M), dtype=complex)
    alpha = 1
    gamma = np.ones((N, M), dtype=complex)
    theta = np.ones((N, M), dtype=complex)

    d[i] = [U, V, phi, psi, alpha, gamma, theta]


# Run each SPL stage and feed the final output column into the next stage.
for i in range(NUM_STAGES):
    U_curr, V_curr, phi_curr, psi_curr, alpha_curr, gamma_curr, theta_curr = d[i]
    F(U_curr, V_curr, phi_curr, psi_curr, alpha_curr, gamma_curr, theta_curr)

    if i < NUM_STAGES - 1:
        d[i + 1][0][:, 0] = U_curr[:, -1]
        d[i + 1][1][:, 0] = V_curr[:, -1]


# Plot all pulse amplitudes in the first SPL stage.
U_plot = d[0][0]  # shape: (N, M), rows = pulses, columns = roundtrips

# Matplotlib's 3D scatter requires x, y, and z to have the same shape.
# Since U_plot has N*M complex entries, make N*M x-values too.
roundtrip_grid = np.broadcast_to(np.arange(M), U_plot.shape)
xpoints = roundtrip_grid.ravel()      # shape: (N*M,)
ypoints = U_plot.real.ravel()         # shape: (N*M,)
zpoints = U_plot.imag.ravel()         # shape: (N*M,)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter3D(xpoints, ypoints, zpoints)
ax.set_xlabel("Roundtrip", fontsize=10)
ax.set_ylabel("Real part", fontsize=10)
ax.set_zlabel("Imaginary part", fontsize=10)

# Save the plot before showing it.
# This will create a PNG in the same folder where the script is run.
output_filename = "SPL_stage0_3d_scatter.png"
fig.savefig(output_filename, dpi=300, bbox_inches="tight")
print(f"Saved plot to {output_filename}")

plt.show()
