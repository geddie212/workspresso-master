import main


class SQLReturn:

    def __init__(self):
        self.db_all = main.Cafe.query.all()

    def all_locations(self):
        locations = []
        for loc in self.db_all:
            if loc.location not in locations:
                locations.append(loc.location)
        return locations

    def all_seats(self):
        seats = []
        for seat in self.db_all:
            if seat.seats not in seats:
                seats.append(seat.seats)
        return seats

    def all_prices(self):
        prices = []
        for price in self.db_all:
            if price.coffee_price not in prices:
                prices.append(price.coffee_price)
        return prices

    def single_cafe(self, cafe_name):
        one_cafe = main.Cafe.query.filter_by(name=cafe_name).first()
        return one_cafe

