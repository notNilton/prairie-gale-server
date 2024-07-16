import numpy as np

def reconciliate_data(incidence_matrix, measurements, tolerances):
    """
    Reconcile the data based on the provided incidence matrix, measurements, and tolerances.
    
    Parameters:
        incidence_matrix (list or np.ndarray): The incidence matrix.
        measurements (list or np.ndarray): Array of measurements.
        tolerances (list or np.ndarray): Array of tolerances.

    Returns:
        list: Reconciled measurements.
    
    Raises:
        ValueError: If there is a mismatch in the number of measurements or tolerances.
    """
    try:
        # Convert inputs to numpy arrays
        incidence_matrix = np.array(incidence_matrix)
        measurements = np.array(measurements)
        tolerances = np.array(tolerances)
        
        num_nodes, num_measurements = incidence_matrix.shape

        if len(measurements) != num_measurements:
            raise ValueError("Mismatch in number of measurements")
        if len(tolerances) != num_measurements:
            raise ValueError("Mismatch in number of tolerances")

        absolute_tolerances = measurements * tolerances

        # Calculate weight vector
        weight_vector = 2 * np.concatenate((measurements / (absolute_tolerances ** 2), np.zeros(num_nodes)))
        
        # Calculate diagonal matrix
        diag_matrix = 2 * np.linalg.inv(np.diag(absolute_tolerances) ** 2)
        
        # Calculate weight matrix
        weight_matrix = np.block([[diag_matrix, incidence_matrix.T], [incidence_matrix, np.zeros((num_nodes, num_nodes))]])
        
        # Calculate result
        result = np.linalg.inv(weight_matrix) @ weight_vector

        reconciled_measurements = result[:num_measurements]
        lagrange_multipliers = result[num_measurements:]
        correction = measurements - reconciled_measurements

        return reconciled_measurements.tolist()
    except ValueError as e:
        raise ValueError("Invalid numbers provided: " + str(e))
    except Exception as e:
        raise Exception("An error occurred during reconciliation: " + str(e))
    
# Example usage:
# incidence_matrix = [[1, -1, -1, 0, 0], [0, 0, 1, -1, -1]]
# measurements = [161, 79, 80, 63, 20]
# tolerances = [0.05, 0.01, 0.01, 0.10, 0.05]
# reconciliated_measurements = reconciliate_data(incidence_matrix, measurements, tolerances)
# print(reconciliated_measurements)
