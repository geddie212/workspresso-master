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

    def get_all_records(self):
        all_records = []
        for cafe in self.db_all:
            all_records.append(dict(name=cafe.name, map_url=cafe.map_url, img_url=cafe.img_url, location=cafe.location,
                                    has_sockets=cafe.has_sockets, has_toilet=cafe.has_toilet, has_wifi=cafe.has_wifi,
                                    can_take_calls=cafe.can_take_calls, seats=cafe.seats,
                                    coffee_price=cafe.coffee_price))
        print(all_records)

    def make_record(self, list_dict):

        for r in list_dict:
            record = main.Cafe(name=r['name'], map_url=r['map_url'], img_url=r['img_url'], location=r['location'],
                               has_sockets=r['has_sockets'], has_toilet=r['has_toilet'], has_wifi=r['has_wifi'],
                               can_take_calls=r['can_take_calls'], seats=r['seats'], coffee_price=r['coffee_price'])
            main.db.session.add(record)
            main.db.session.commit()
