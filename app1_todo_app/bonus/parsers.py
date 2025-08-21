def parse(feet_inches: str) -> dict[str, float]:
    parts = feet_inches.split("ft")
    feet = float(parts[0])
    inches = float(parts[1])
    return {"feet": feet, "inches": inches}
