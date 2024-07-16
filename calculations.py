import numpy as np

def calculate_weight_vector(measurements, absolute_tolerances, num_nodes):
    return 2 * np.concatenate((measurements / (absolute_tolerances ** 2), np.zeros(num_nodes)))

def calculate_diagonal_matrix(absolute_tolerances):
    return 2 * np.linalg.inv(np.diag(absolute_tolerances) ** 2)

def calculate_weight_matrix(diag_matrix, B, num_nodes):
    return np.block([[diag_matrix, B.T], [B, np.zeros((num_nodes, num_nodes))]])

def calculate_result(weight_matrix, weight_vector):
    return np.linalg.inv(weight_matrix) @ weight_vector

def reconciliate_data(incidence_matrix, measurements, tolerances):
    try:
        # console.log(incidence_matrix)
        # Ensure inputs are numpy arrays
        incidence_matrix = np.array(incidence_matrix)
        measurements = np.array(measurements)
        tolerances = np.array(tolerances)
    
        num_nodes, num_measurements = incidence_matrix.shape

        assert len(measurements) == num_measurements, "Mismatch in number of measurements"
        assert len(tolerances) == num_measurements, "Mismatch in number of tolerances"

        absolute_tolerances = measurements * tolerances

        weight_vector = calculate_weight_vector(measurements, absolute_tolerances, num_nodes)
        diag_matrix = calculate_diagonal_matrix(absolute_tolerances)
        weight_matrix = calculate_weight_matrix(diag_matrix, incidence_matrix, num_nodes)
        result = calculate_result(weight_matrix, weight_vector)

        reconciled_measurements = result[:num_measurements]
        lagrange_multipliers = result[num_measurements:]
        correction = measurements - reconciled_measurements

        return reconciled_measurements.tolist()
    except ValueError as e:
        raise ValueError("Invalid numbers provided")
    
# [[1, -1, -1, 0, 0], [0, 0, 1, -1, -1]]
# [161, 79, 80, 63, 20]
# [0.05, 0.01, 0.01, 0.10, 0.05]