
from typing import List, Dict, Any

def calculate_revenue_recognition(
    transaction_price: float,
    costs_incurred: float,
    total_estimated_costs: float,
    standalone_selling_prices: List[float],
    performance_obligations: List[Any],  # placeholder, not used in logic here
    probabilities: List[float]
) -> Dict[str, Any]:
    """
    Calculates the revenue recognition schedule based on provided parameters.

    Args:
        transaction_price (float): Total expected consideration from the contract.
        costs_incurred (float): Cumulative costs incurred to date.
        total_estimated_costs (float): Total expected costs for the project.
        standalone_selling_prices (List[float]): Prices for each obligation.
        performance_obligations (List[Any]): List of obligations (not used directly).
        probabilities (List[float]): Probabilities for variable consideration.

    Returns:
        Dict[str, Any]: Contains schedule (list of dicts) and total recognized revenue.
    
    Raises:
        ValueError: For invalid inputs such as negative prices, probabilities sums, or mismatched lengths.
    """
    # Validate inputs
    if transaction_price < 0:
        raise ValueError("Transaction price cannot be negative.")
    if costs_incurred < 0:
        raise ValueError("Costs incurred cannot be negative.")
    if total_estimated_costs < 0:
        raise ValueError("Total estimated costs cannot be negative.")
    if len(standalone_selling_prices) != len(probabilities):
        raise ValueError("Mismatch in lengths of standalone_selling_prices and probabilities.")
    if any(p < 0 or p > 1 for p in probabilities):
        raise ValueError("Probabilities must be between 0 and 1.")
    if sum(probabilities) > 1 + 1e-8:
        raise ValueError("Sum of probabilities cannot exceed 1.")
    if len(standalone_selling_prices) != len(performance_obligations):
        raise ValueError("Mismatch in number of stand-alone prices and obligations.")
    if len(standalone_selling_prices) == 0:
        # No obligations, no revenue
        return {'schedule': [], 'revenue': 0.0}
    # Handle division by zero in total_estimated_costs
    if total_estimated_costs == 0:
        raise ValueError("Total estimated costs cannot be zero for allocation.")

    # Adjust standalone prices by probabilities
    adjusted_selling_prices = []
    for ssp, p in zip(standalone_selling_prices, probabilities):
        # Validate individual probabilities
        if p < 0 or p > 1:
            raise ValueError("Probabilities must be between 0 and 1.")
        adjusted_selling_prices.append(ssp * p)

    total_allocated_price = sum(adjusted_selling_prices)
    # Cap total allocated price at transaction_price if it exceeds
    if total_allocated_price > transaction_price + 1e-8:
        scale_factor = transaction_price / total_allocated_price
        adjusted_selling_prices = [asp * scale_factor for asp in adjusted_selling_prices]
        total_allocated_price = transaction_price

    # Compute percentage complete
    percentage_complete = min(calculate_percentage_complete(costs_incurred, total_estimated_costs), 1.0)

    # Recognize revenue proportionally
    revenue = transaction_price * percentage_complete

    # Build a basic schedule - linear recognition over percentage
    schedule = [
        {
            'period': 0,
            'percentage_complete': 0.0,
            'recognized_revenue': 0.0
        },
        {
            'period': 1,
            'percentage_complete': percentage_complete,
            'recognized_revenue': revenue
        }
    ]

    return {
        'schedule': schedule,
        'revenue': revenue
    }

def calculate_percentage_complete(costs_incurred: float, total_estimated_costs: float) -> float:
    """
    Calculate the percentage of completion based on costs incurred and total estimated costs.
    Safeguards against division by zero.

    Args:
        costs_incurred (float): Cumulative costs incurred.
        total_estimated_costs (float): Total estimated costs.

    Returns:
        float: Percentage complete between 0 and 1.
    """
    if total_estimated_costs == 0:
        return 1.0 if costs_incurred > 0 else 0.0
    return min(costs_incurred / total_estimated_costs, 1.0)
