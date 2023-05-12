class Player:
    def __init__(self,id, first_name, last_name, password, food, item, money):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.food = food
        self.item = item
        self.money = money
        # sahip olduğu alanlar
        self.properties = []
        # Çalıştığı yer
        self.workplace = None

    # alan satın al
    def buy_property(self, property):
        if len(self.properties) < 2:
            self.properties.append(property)
            self.money -= property.price

    # alan sat
    def sell_property(self, property):
        if property in self.properties:
            self.properties.remove(property)
            self.money += property.price

    # alan kirala
    def rent_property(self, property, price):
        property.owner = self
        self.money -= price

    # Çalış
    def work(self):
        if self.workplace:
            self.money += self.workplace.salary



class Admin:
    def __init__(self):
        self.players = []
        self.properties = []
        self.grid_size = (3, 3)

    # Oyuncu Ekle
    def add_player(self, player):
        self.players.append(player)

    # Alan Ekle
    def add_property(self, property):
        self.properties.append(property)

    # Oyun grid boyutu belirle
    def set_grid_size(self, size):
        self.grid_size = size

    # Alan Fiyatu belirle
    def set_property_price(self, property, price):
        property.price = price


class Property:
    def __init__(self, owner, price, level=1):
        self.owner = owner
        self.price = price
        self.level = level


class Market(Property):
    def __init__(self, owner, price, level=1):
        super().__init__(owner, price, level)
        self.food = 100

    # Yiyecek Sat
    def sell_food(self, player, amount):
        if self.food >= amount:
            self.food -= amount
            player.money -= amount

# Arazi
class Estate(Property):
    def __init__(self, owner, price, level=1):
        super().__init__(owner, price, level)
        self.rent = 10 * level

class Shop(Property):
    def __init__(self, owner, price, level=1):
        super().__init__(owner, price, level)
        self.items = 100

    # Eşya Sat
    def sell_item(self, player, amount):
        if self.items >= amount:
            self.items -= amount
            player.money -= amount

admin = Admin()
admin.set_grid_size((3, 3))

player1 = Player("Alice", 100, 100, 100)
player2 = Player("Bob", 100, 100, 100)
admin.add_player(player1)
admin.add_player(player2)

market = Market(admin, 1000)
estate = Estate(admin, 5000)
shop = Shop(admin, 3000)

admin.add_property(market)
admin.add_property(estate)
admin.add_property(shop)

player1.buy_property(market)
player2.buy_property(estate)
player1.rent_property(shop, 100)
player2.workplace = shop

print(player1.properties)
print(player2.properties)
print(player1)
