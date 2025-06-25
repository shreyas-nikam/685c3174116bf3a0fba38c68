import pytest
from definition_262b8a4dec1642549b2338e231394a05 import calculate_revenue_recognition

@pytest.mark.parametrize("transaction_price, costs_incurred, total_estimated_costs, standalone_selling_prices, performance_obligations, probabilities, expected", [
    # Basic valid case with single performance obligation, no variable consideration
    (1000.0, 200.0, 1000.0, [500.0, 500.0], [1, 1], [1, 0], {'schedule': [...], 'revenue': ...}),  # Placeholder for actual expected dict

    # Multiple performance obligations, allocation sums to transaction price
    (2000.0, 400.0, 2000.0, [1000.0, 1000.0], [1, 1], [1, 1], {'schedule': [...], 'revenue': ...}),

    # Zero costs incurred
    (1500.0, 0.0, 1500.0, [750.0, 750.0], [1, 1], [0.5, 0.5], {'schedule': [...], 'revenue': ...}),

    # Zero total estimated costs (edge case, should handle division by zero)
    (1500.0, 300.0, 0.0, [750.0, 750.0], [1, 1], [1, 0], ValueError),

    # Probabilities sum to more than 1 (edge case)
    (1200.0, 300.0, 1200.0, [600.0, 600.0], [1, 1], [0.7, 0.7], {'schedule': [...], 'revenue': ...}),

    # Probabilities sum to less than 1
    (1800.0, 360.0, 1800.0, [900.0, 900.0], [1, 1], [0.4, 0.4], {'schedule': [...], 'revenue': ...}),

    # Negative transaction price (invalid input)
    (-1000.0, 200.0, 1000.0, [500.0, 500.0], [1, 1], [1, 0], ValueError),

    # Negative costs incurred
    (1000.0, -200.0, 1000.0, [500.0, 500.0], [1, 1], [1, 1], ValueError),

    # Negative total_estimated_costs
    (1000.0, 200.0, -1000.0, [500.0, 500.0], [1, 1], [1, 1], ValueError),

    # Standalone selling prices not matching number of obligations
    (1000.0, 200.0, 1000.0, [500.0], [1, 1], [1, 1], ValueError),

    # Standalone selling prices are negative
    (1000.0, 200.0, 1000.0, [500.0, -100.0], [1, 1], [1, 1], ValueError),

    # Probabilities array length mismatch
    (1000.0, 200.0, 1000.0, [500.0, 500.0], [1, 1], [0.5], ValueError),

    # Probabilities contain invalid values (>1)
    (1000.0, 200.0, 1000.0, [500.0, 500.0], [1, 1], [1.2, -0.2], ValueError),

    # Probabilities sum to exactly 1
    (1000.0, 200.0, 1000.0, [600.0, 400.0], [1, 1], [0.6, 0.4], {'schedule': [...], 'revenue': ...}),
])

def test_calculate_revenue_recognition(transaction_price, costs_incurred, total_estimated_costs, standalone_selling_prices, performance_obligations, probabilities, expected):
    if isinstance(expected, dict):
        result = calculate_revenue_recognition(transaction_price, costs_incurred, total_estimated_costs, standalone_selling_prices, performance_obligations, probabilities)
        # Assert dictionary keys and approximate values as needed
        assert isinstance(result, dict)
        # Further detailed assertions can be added based on expected structure
    elif issubclass(expected, Exception):
        with pytest.raises(expected):
            calculate_revenue_recognition(transaction_price, costs_incurred, total_estimated_costs, standalone_selling_prices, performance_obligations, probabilities)
    else:
        # For cases with placeholder expectations, just ensure the function completes without error
        result = calculate_revenue_recognition(transaction_price, costs_incurred, total_estimated_costs, standalone_selling_prices, performance_obligations, probabilities)
        assert result is not None
