from dataclasses import dataclass
import pandas


DATA_FILE_PATH = "hotels.csv"


class DataAccess:
    def __init__(self, data_file_path: str):
        self.file_path = data_file_path
        self.df = pandas.read_csv(data_file_path)

    def get_data_source(self):
        return self.df

    def save(self):
        self.df.to_csv(self.file_path, index=False)


@dataclass
class HotelProps:
    hotel_id: int
    name: str
    city: str
    capacity: int
    available: bool


class Hotel:
    def __init__(self, props: HotelProps):
        self.hotel_id = props.hotel_id
        self.name = props.name
        self.city = props.city
        self.capacity = props.capacity
        self.available = props.available


class HotelService:
    def __init__(self, data_access: DataAccess):
        self.data_access = data_access

    def book(self, hotel_id: str):
        """Book a hotel by changing its available status to 'no'."""
        data_source = self.data_access.get_data_source()
        data_source.loc[data_source["id"] == hotel_id]["available"] = "no"
        self.data_access.save()

    def find_all(self):
        data_source = self.data_access.get_data_source()
        return data_source

    def find_one(self, hotel_id: int) -> Hotel | None:
        """Find and return one hotel."""
        data_source = self.data_access.get_data_source()
        results = data_source.loc[data_source["id"] == hotel_id]
        if len(results) == 0:
            return None
        first_row_dict = results.iloc[0].to_dict()
        hotel_props = HotelProps(
            first_row_dict["id"],
            first_row_dict["name"],
            first_row_dict["city"],
            first_row_dict["capacity"],
            first_row_dict["available"] == "yes",
        )
        hotel = Hotel(hotel_props)
        return hotel


class ReservationTicket:
    def __init__(self, customer_name: str, hotel: Hotel):
        self.customer_name = customer_name
        self.hotel = hotel

    def generate(self) -> str:
        content = f"""Thank your for your reservation 😊
Here is your booking info.
Customer name: {self.customer_name}
Hotel: {self.hotel.name}"""
        return content


def main():
    data_access = DataAccess(DATA_FILE_PATH)
    hotel_service = HotelService(data_access=data_access)
    hotels = hotel_service.find_all()
    print(hotels)
    hotel_id = input("Enter the id of the hotel: ")
    hotel = hotel_service.find_one(int(hotel_id))
    if hotel is not None and hotel.available:
        hotel_service.book(hotel_id)
        customer_name = input("Enter your name: ")
        reservation_ticket = ReservationTicket(customer_name, hotel)
        ticket = reservation_ticket.generate()
        print(ticket)
    elif hotel is None:
        print("Hotel id is not valid 😕")
    else:
        print("Hotel is not available 😕")


if __name__ == "__main__":
    main()
