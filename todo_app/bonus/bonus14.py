from bonus.converters import convert


def main():
    feet_inches = input("Enter feet and inches: ")
    centimeters = convert(feet_inches)
    print(f"{feet_inches} is equal to {centimeters} cm")
    if centimeters >= 120:
        print("Kid can use the slide.")
    else:
        print("Kid is too small.")


main()
