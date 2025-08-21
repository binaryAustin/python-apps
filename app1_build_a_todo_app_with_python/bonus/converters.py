from bonus.parsers import parse


def convert(feet_inches: str) -> float:
    """Convert the string presentation of feet inches to centimeters."""
    parsed = parse(feet_inches)
    centimeters = (parsed["feet"] * 0.3048 + parsed["inches"] * 0.0254) * 100
    return centimeters
