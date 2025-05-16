import time
from collections import deque, defaultdict

# ------------------------------
# Part 1: Inventory Management (FIFO Principle)
# ------------------------------

class FrozenFoodItem:
    def __init__(self, name, category, quantity, expiry_date, cost_per_unit):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.expiry_date = time.strptime(expiry_date, "%Y/%m/%d")
        self.cost_per_unit = cost_per_unit

    def __str__(self):
        expiry_str = time.strftime("%Y/%m/%d", self.expiry_date)
        total_cost = self.quantity * self.cost_per_unit
        return f"{self.name} | {self.category} | {expiry_str} | Qty: {self.quantity} | Cost/Unit: {self.cost_per_unit} | Total: {total_cost}"

class InventoryManager:
    def __init__(self):
        self.inventory = defaultdict(deque)  # Category -> Queue of FrozenFoodItem

    def add_item(self, name, category, quantity, expiry_date, cost_per_unit):
        item = FrozenFoodItem(name, category, quantity, expiry_date, cost_per_unit)
        self.inventory[category].append(item)
        self.inventory[category] = deque(sorted(self.inventory[category], key=lambda x: x.expiry_date))
        print(f"[+] Added {quantity} of {name} (expiry: {expiry_date}) successfully.")

    def remove_item(self, category, quantity_needed):
        if category not in self.inventory or not self.inventory[category]:
            print("[!] No items found in this category.")
            return
        
        while quantity_needed > 0 and self.inventory[category]:
            oldest_item = self.inventory[category][0]
            if oldest_item.quantity <= quantity_needed:
                quantity_needed -= oldest_item.quantity
                print(f"[-] Removed {oldest_item.quantity} of {oldest_item.name} (expiry: {time.strftime('%Y/%m/%d', oldest_item.expiry_date)})")
                self.inventory[category].popleft()
            else:
                oldest_item.quantity -= quantity_needed
                print(f"[-] Removed {quantity_needed} of {oldest_item.name}")
                quantity_needed = 0

    def track_inventory(self):
        print("\n=== Current Frozen Food Inventory ===")
        if not any(self.inventory.values()):
            print("[!] Inventory is empty.")
            return
        for category, queue in self.inventory.items():
            print(f"\n[Category: {category}]")
            for item in queue:
                print(f"  {item}")

    def alert_expiring_items(self):
        today = time.localtime()
        found = False
        print("\n=== Expiry Alerts (Next 30 Days) ===")
        for queue in self.inventory.values():
            for item in queue:
                days_left = (time.mktime(item.expiry_date) - time.mktime(today)) / (24*3600)
                if 0 <= days_left <= 30:
                    found = True
                    print(f"  {item} --> {int(days_left)} days left")
        if not found:
            print("  [No items nearing expiry.]")

# ------------------------------
# Part 2: Search and Sort Module
# ------------------------------

class InventorySearchSort:
    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager

    def search_item_by_name(self, name):
        results = []
        for queue in self.inventory_manager.inventory.values():
            for item in queue:
                if item.name.lower() == name.lower():
                    results.append(item)
        return results

    def search_by_category(self, category):
        return list(self.inventory_manager.inventory.get(category, []))

    def sort_inventory(self, by='expiry'):
        all_items = []
        for queue in self.inventory_manager.inventory.values():
            all_items.extend(queue)
        
        if by == 'expiry':
            all_items.sort(key=lambda x: x.expiry_date)
        elif by == 'quantity':
            all_items.sort(key=lambda x: x.quantity, reverse=True)
        elif by == 'name':
            all_items.sort(key=lambda x: x.name.lower())
        
        return all_items

    def display_sorted_inventory(self, by='expiry'):
        sorted_items = self.sort_inventory(by)
        print(f"\n=== Sorted Inventory by {by.capitalize()} ===")
        for item in sorted_items:
            print(f"  {item}")

# ------------------------------
# Part 3: Performance and Reporting Module
# ------------------------------

class PerformanceAnalyzer:
    def __init__(self):
        self.logs = []

    def log_action(self, action_type, item_name):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logs.append((timestamp, action_type, item_name))

    def show_logs(self):
        print("\n=== Action Logs ===")
        for log in self.logs:
            print(f"  {log[0]} | {log[1]} | {log[2]}")

    def report_inventory_health(self, inventory_manager):
        total_items = 0
        soon_expiring = 0
        today = time.localtime()
        for queue in inventory_manager.inventory.values():
            for item in queue:
                total_items += item.quantity
                days_left = (time.mktime(item.expiry_date) - time.mktime(today)) / (24*3600)
                if 0 <= days_left <= 30:
                    soon_expiring += item.quantity
        
        print("\n=== Inventory Health Report ===")
        print(f"  Total items in stock: {total_items}")
        print(f"  Items expiring soon (within 30 days): {soon_expiring}")

    def analyze_complexity(self):
        print("\n=== Time Complexity (Theoretical) ===")
        print("  Add Item: O(log n) (due to sorting)")
        print("  Remove Item: O(1) per removal")
        print("  Search Item: O(n)")
        print("  Sort Inventory: O(n log n)")

# ------------------------------
# Main Program Menu
# ------------------------------

def get_valid_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("[!] Invalid input. Please enter a valid number.")

def get_valid_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("[!] Invalid input. Please enter a valid number.")

def get_valid_date_input(prompt):
    while True:
        try:
            date_input = input(prompt)
            time.strptime(date_input, "%Y/%m/%d")
            return date_input
        except ValueError:
            print("[!] Invalid date format. Please use YYYY/MM/DD.")

def main():
    inventory = InventoryManager()
    search_sort = InventorySearchSort(inventory)
    performance = PerformanceAnalyzer()

    while True:
        print("\n=== Frozen Food Inventory Management ===")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Track Inventory")
        print("4. Alert Expiring Items")
        print("5. Search Item by Name")
        print("6. Search Item by Category")
        print("7. Sort and Display Inventory")
        print("8. Show Action Logs")
        print("9. Inventory Health Report")
        print("10. Analyze Time/Space Complexity")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            name = input("Enter item name: ")
            category = input("Enter category: ")
            quantity = get_valid_int_input("Enter quantity: ")
            expiry_date = get_valid_date_input("Enter expiry date (YYYY/MM/DD): ")
            cost_per_unit = get_valid_float_input("Enter cost per unit: ")
            inventory.add_item(name, category, quantity, expiry_date, cost_per_unit)
            performance.log_action("Add", name)

        elif choice == "2":
            category = input("Enter category to remove from: ")
            quantity = get_valid_int_input("Enter quantity to remove: ")
            inventory.remove_item(category, quantity)
            performance.log_action("Remove", category)

        elif choice == "3":
            inventory.track_inventory()

        elif choice == "4":
            inventory.alert_expiring_items()

        elif choice == "5":
            name = input("Enter product name to search: ")
            results = search_sort.search_item_by_name(name)
            if results:
                print("\nFound items:")
                for item in results:
                    print(f"  {item}")
            else:
                print("[!] No item found with that name.")

        elif choice == "6":
            category = input("Enter category to search: ")
            results = search_sort.search_by_category(category)
            if results:
                print("\nFound items:")
                for item in results:
                    print(f"  {item}")
            else:
                print("[!] No items found in that category.")

        elif choice == "7":
            print("\nSort by: expiry / quantity / name")
            sort_by = input("Enter your choice: ")
            search_sort.display_sorted_inventory(sort_by)

        elif choice == "8":
            performance.show_logs()

        elif choice == "9":
            performance.report_inventory_health(inventory)

        elif choice == "10":
            performance.analyze_complexity()

        elif choice == "0":
            print("Exiting Program. Goodbye!")
            break

        else:
            print("[!] Invalid choice, try again.")

if __name__ == "__main__":
    main()
