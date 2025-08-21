def get_average():
    with open("files/data.txt", "r", encoding="utf8") as file_reader:
        data = file_reader.readlines()

    values = data[1:]
    values = [float(v) for v in values]

    average = sum(values) / len(values)
    return average


def main():
    average = get_average()
    print(average)


main()
