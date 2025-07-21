import hashlib
import time
import datetime

class Block:
    def __init__(self, index, timestamp, transaction, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transaction}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        prev_block = self.get_last_block()
        new_block = Block(len(self.chain), time.time(), transaction, prev_block.hash)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {time.ctime(block.timestamp)}")
            print(f"Transaction: {block.transaction}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print("-" * 50)

blockchain = Blockchain()

print()
print("Welcome to polytechnics vending machince !")
items = {
    41: {"name": "Snickers", "price": 45, "quantity": 4},
    42: {"name": "Slai o'lai", "price": 25, "quantity": 6},
    43: {"name": "Sando", "price": 18, "quantity": 3},
    44: {"name": "Kinder", "price": 18, "quantity": 2},
    45: {"name": "Kit-kat", "price": 45, "quantity": 5},
    46: {"name": "Oreo", "price": 23, "quantity": 2},
    31: {"name": "Fuse Tea", "price": 50, "quantity": 3},
    32: {"name": "Coca-cola", "price": 55, "quantity": 5},
    33: {"name": "Water", "price": 22, "quantity": 6},
    34: {"name": "White Mirinda", "price": 42, "quantity": 2},
    35: {"name": "Pink Mirinda", "price": 42, "quantity": 7},
    36: {"name": "Sprite", "price": 55, "quantity": 2},
}

def display_items():
    name_width = 15
    price_width = 12
    id_width = 6
    quantity_width = 15

    print(f"{'Snacks':<{name_width}} {'Price(Rs)':<{price_width}} {'ID':<{id_width}} {'Quantity left':<{quantity_width}}")
    print("-" * (name_width + price_width + id_width + quantity_width + 3))
    for id, item in items.items():
        if id >= 41:
            print(f"{item['name']:<{name_width}} {item['price']:<{price_width}} {id:<{id_width}} {item['quantity']:<{quantity_width}}")

    print()

    print(f"{'Beverages':<{name_width}} {'Price(Rs)':<{price_width}} {'ID':<{id_width}} {'Quantity left':<{quantity_width}}")
    print("-" * (name_width + price_width + id_width + quantity_width + 3))
    for id, item in items.items():
        if id < 41:
            print(f"{item['name']:<{name_width}} {item['price']:<{price_width}} {id:<{id_width}} {item['quantity']:<{quantity_width}}")

def find_item(item_id):
    return items.get(item_id)

display_items()

print()
print("Minimun money accpeted by the machine is Rs50")
print("Maximun money accepted by the machine is Rs200")
print()
while True:
    Adim_or_student=int(input("Enter 1 for Org1(Adim) & 2 for Org2(Student) or 3 to exit:"))
    if Adim_or_student == 2 :
        try:
            money = int(input("Enter your money in (RS):"))
            if not 50 <= money <= 200:
                print("Your money wasn't accepted. Your refund is: Rs", money)
                continue

            item_id = int(input("Enter the ID of the item that you want: "))
            item = find_item(item_id)

            if not item:
                print("You have inserted a wrong ID. Your refund is: Rs", money)
                continue
            
            quantity = int(input("Enter the quantity that you want: "))
            if quantity > item["quantity"]:
                print("There is not enough product available. Your refund is: Rs", money)
                continue

            price = item["price"] * quantity
            if price > money:
                print("You don't have enough money. Your refund is: Rs", money)
                continue
            
            confirm = int(input("Enter 1 to confirm your purchase or enter 2 to exit: "))
            if confirm == 2:
                print("You have exited the vending machine. Your refund is: Rs", money)
                continue
            
            change = money - price
            item["quantity"] -= quantity
            print(f"You have selected {quantity} {item['name']}(s).")
            print(f"Your change is: Rs {change}")

            blockchain.add_transaction({
                "item": item["name"],
                "price": item["price"],
                "quantity": quantity,
                "paid": money,
                "change": change,
                "date": str(datetime.datetime.now())
            })
            print("\n--- Updated Menu ---")
            display_items()

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif Adim_or_student == 1 :
        # password is 1234
        password = int(input("Enter Adim password to access the machine program :"))
        if password != 1234 :
            print("You have entered a wrong password")
        else :
            print(" 1.  Add new product")
            print(" 2.  Update existing product/delete it")
            print(" 3.  List all products")
            print(" 4.  view transaction log for purchases")
            print()
            command = int(input("Enter the command for the action that you want to execute :"))
            if command == 1 :
                new_product_name=input("Enter new product name :")
                new_product_id = int(input("Enter the new products ID :"))
                new_product_price = int(input("Enter new product price :"))
                new_product_quantity = int(input("Enter the quantity of the new product :"))
                items[new_product_id] = {"name": new_product_name, "price": new_product_price, "quantity": new_product_quantity}
                display_items()
            elif command == 2:
                update_delete = int(input("Enter 1 to update or 2 to delete an item: "))
                if update_delete == 1:
                    update_id = int(input("Enter the ID of the product you want to update: "))
                    if update_id in items:
                        update_price = int(input("Enter the new price of the product: "))
                        update_quantity = int(input("Enter the new quantity of the product: "))
                        items[update_id]["price"] = update_price
                        items[update_id]["quantity"] = update_quantity
                        display_items()
                    else:
                        print("Item not found.")
                elif update_delete == 2:
                    delete_id = int(input("Enter the ID of the product you want to delete: "))
                    if delete_id in items:
                        del items[delete_id]
                        print("Item deleted successfully.")
                        display_items()
                    else:
                        print("Item not found.")
                else:
                    print("Invalid option selected.")
            elif command == 3 :
                display_items()
            elif command == 4:
                print("--- Blockchain Ledger ---")
                blockchain.print_chain()
    elif Adim_or_student == 3:
        break
    else :
        print("You have inserted a wrong command")
    
