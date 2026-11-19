def calculate_trip_budget(
    hotel_cost: float,
    food_cost: float,
    transport_cost: float,
    other_cost: float
) -> float:
    """Calculate the total estimated travel budget."""

    return (
        hotel_cost
        + food_cost
        + transport_cost
        + other_cost
    )