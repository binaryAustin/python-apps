def convert(feet_inches: str) -> float:
    parts = feet_inches.split("ft")
    feet = float(parts[0])
    inches = float(parts[1])

    centimeters = (feet * 0.3048 + inches * 0.0254) * 100
    return centimeters


def main():
    feet_inches = input("Enter feet and inches: ")
    centimeters = convert(feet_inches)
    print(f"{feet_inches} is equal to {centimeters} cm")


main()
