from dataclasses import dataclass
import pandas


HOTELS_DATA_PATH = "hotels.csv"
CARDS_DATA_PATH = "cards.csv"
CARDS_SECURITY_DATA_PATH = "card-security.csv"


@dataclass
class DataPaths:
    hotels_data_path: str
    cards_data_path: str
    cards_security_data_path: str


class DataAccess:
    def __init__(self, paths: DataPaths):
        self.hotels_data_path = paths.hotels_data_path
        self.cards_data_path = paths.cards_data_path
        self.cards_security_data_path = paths.cards_security_data_path
        self.hotels_df = pandas.read_csv(paths.hotels_data_path, dtype={"id": str})
        self.cards_df = pandas.read_csv(paths.cards_data_path, dtype=str)
        self.cards_security_df = pandas.read_csv(
            paths.cards_security_data_path, dtype=str
        )

    def save_hotels(self):
        self.hotels_df.to_csv(self.hotels_data_path, index=False)

    def save_cards(self):
        self.cards_df.to_csv(self.cards_data_path, index=False)


@dataclass
class HotelProps:
    hotel_id: str
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
        hotels_df = self.data_access.hotels_df
        hotels_df.loc[hotels_df["id"] == hotel_id, "available"] = "no"
        self.data_access.save_hotels()

    def find_all(self):
        return self.data_access.hotels_df

    def find_one(self, hotel_id: str) -> Hotel | None:
        """Find and return one hotel."""
        hotels_df = self.data_access.hotels_df
        results = hotels_df.loc[hotels_df["id"] == hotel_id]
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


@dataclass
class CreditCard:
    holder: str
    number: str
    expiration: str
    cvc: str


class PaymentService:
    def __init__(self, data_access: DataAccess):
        self.data_access = data_access

    def validate_card(self, credit_card: CreditCard) -> bool:
        cards_df_list = self.data_access.cards_df.to_dict(orient="records")
        card_to_check = {
            "number": credit_card.number,
            "expiration": credit_card.expiration,
            "cvc": credit_card.cvc,
            "holder": credit_card.holder,
        }
        return card_to_check in cards_df_list

    def authenticate(self, card_number: str, password: str) -> bool:
        cards_security_df = self.data_access.cards_security_df
        rows = cards_security_df.loc[cards_security_df["number"] == card_number]
        return len(rows) > 0 and rows.iloc[0].to_dict()["password"] == password


def main():
    data_paths = DataPaths(HOTELS_DATA_PATH, CARDS_DATA_PATH, CARDS_SECURITY_DATA_PATH)
    data_access = DataAccess(data_paths)
    hotel_service = HotelService(data_access=data_access)
    payment_service = PaymentService(data_access=data_access)
    hotels = hotel_service.find_all()
    print(hotels)
    hotel_id = input("Enter the id of the hotel: ")
    hotel = hotel_service.find_one(hotel_id)
    if hotel is not None and hotel.available:
        hotel_service.book(hotel_id)
        card_number = input("Enter credit card number: ")
        holder_name = input("Enter holder name: ")
        expiration_date = input("Enter expiration date: ")
        cvc = input("Enter CVC: ")
        credit_card = CreditCard(holder_name, card_number, expiration_date, cvc)
        password = input("Enter password: ")
        if payment_service.validate_card(
            credit_card=credit_card
        ) and payment_service.authenticate(card_number, password):
            reservation_ticket = ReservationTicket(holder_name, hotel)
            ticket = reservation_ticket.generate()
            print(ticket)
        else:
            print("There was a problem with your payment")
    else:
        print("Hotel is not valid or available 😕")


if __name__ == "__main__":
    main()
