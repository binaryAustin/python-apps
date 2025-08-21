def parse(feet_inches: str) -> dict[str, float]:
    parts = feet_inches.split("ft")
    feet = float(parts[0])
    inches = float(parts[1])
    return {"feet": feet, "inches": inches}


def convert(feet_inches: str) -> float:
    """Convert the string presentation of feet inches to centimeters."""
    parsed = parse(feet_inches)
    centimeters = (parsed["feet"] * 0.3048 + parsed["inches"] * 0.0254) * 100
    return centimeters


def main():
    feet_inches = input("Enter feet and inches: ")
    centimeters = convert(feet_inches)
    print(f"{feet_inches} is equal to {centimeters} cm")
    if centimeters >= 120:
        print("Kid can use the slide.")
    else:
        print("Kid is too small.")


main()
