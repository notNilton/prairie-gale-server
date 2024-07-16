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
        # incidence_matrix = float(incidence_matrix)
        # measurements = float(measurements)
        # tolerances = float(tolerances)
        # return incidence_matrix + measurements + tolerances

        B = np.array([[1, -1, -1, 0, 0], [0, 0, 1, -1, -1]])  # Adjust according to the problem

        # Measurements and tolerances
        mean = np.array([161, 79, 80, 63, 20])  # Adjust according to the problem
        tole = np.array([0.05, 0.01, 0.01, 0.10, 0.05])  # Adjust according to the problem

        # Calculate necessary dimensions
        num_nodes, num_measurements = B.shape

        # Validate Inputs
        assert len(mean) == num_measurements, "Mismatch in number of measurements"
        assert len(tole) == num_measurements, "Mismatch in number of tolerances"

        # Calculate absolute tolerances
        absolute_tolerances = mean * tole

        # Compute all necessary matrices and results
        weight_vector = calculate_weight_vector(mean, absolute_tolerances, num_nodes)
        diag_matrix = calculate_diagonal_matrix(absolute_tolerances)
        weight_matrix = calculate_weight_matrix(diag_matrix, B, num_nodes)
        result = calculate_result(weight_matrix, weight_vector)

        # Extract results
        reconciled_measurements = result[:num_measurements]
        lagrange_multipliers = result[num_measurements:]
        correction = mean - reconciled_measurements

        # Output results
        print("Incidence Matrix:", incidence_matrix)
        print("Measurements:", measurements)
        print("Tolerances:", tolerances)
        return reconciled_measurements
    except ValueError:
        raise ValueError("Invalid numbers provided")
    
# def main():
#     # Input Data
#     B = np.array([[1, -1, -1, 0, 0], [0, 0, 1, -1, -1]])  # Adjust according to the problem

#     # Measurements and tolerances
#     measurements = np.array([161, 79, 80, 63, 20])  # Adjust according to the problem
#     tolerances = np.array([0.05, 0.01, 0.01, 0.10, 0.05])  # Adjust according to the problem

#     # Calculate necessary dimensions
#     num_nodes, num_measurements = B.shape

#     # Validate Inputs
#     assert len(measurements) == num_measurements, "Mismatch in number of measurements"
#     assert len(tolerances) == num_measurements, "Mismatch in number of tolerances"

#     # Calculate absolute tolerances
#     absolute_tolerances = measurements * tolerances

#     # Compute all necessary matrices and results
#     weight_vector = calculate_weight_vector(measurements, absolute_tolerances, num_nodes)
#     diag_matrix = calculate_diagonal_matrix(absolute_tolerances)
#     weight_matrix = calculate_weight_matrix(diag_matrix, B, num_nodes)
#     result = calculate_result(weight_matrix, weight_vector)

#     # Extract results
#     reconciled_measurements = result[:num_measurements]
#     lagrange_multipliers = result[num_measurements:]
#     correction = measurements - reconciled_measurements

#     # Output results
#     print("Reconciled measurements:", reconciled_measurements)
#     print("Lagrange multipliers:", lagrange_multipliers)
#     print("Correction:", correction)

# if __name__ == "__main__":
#     main()
