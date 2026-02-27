from app.dashboard import Dashboard
from rapidfuzz import fuzz
import sqlite3

class Database:
    def __init__(self, db_name="data/data.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.products = self.get_all_products()
        self.transaction_running = False
        self.current_transaction_products = []
    
    def get_all_products(self):
        self.cursor.execute("""SELECT p.id, p.name, p.price, s.qty
            FROM product AS p
            JOIN stock AS s
                ON p.id = s.p_id""")
        products = [dict(row) for row in self.cursor.fetchall()]

        return products
    
    def get_all_products_name(self):
        products = [p['name'] for p in self.products]
        return products
    
    def process_item(self, product: dict):
        candidates:list[int] = self.get_candidates(product["product"])
        product_index: int = self.resolve_product(candidates, product['price_hint'], product['qty'])
        self.commit_transaction(self.products[product_index]['id'], product['qty'])

        p = self.products[product_index]
        self.current_transaction_products.append({'name': p['name'], 'price': p['price'], 'qty': product['qty']})
        Dashboard.update_product(p['id'], product['qty'])
    
    def get_candidates(self, product: str, threshold=80) -> list[int]:
        candidates = []
        for i in range(len(self.products)):
            score = fuzz.WRatio(product, self.products[i]['name'])
            self.products[i]['score'] = score
            if score > threshold:
                candidates.append(i)
        
        return candidates
    
    def resolve_product(self, candidates: list[int], spoken_price: int, spoken_qty: int) -> int:
        # just one candidate
        if len(candidates) == 1:
            return candidates[0]
        
        # filter by price
        new_candidates = []
        if spoken_price:
            for i in candidates:
                if self.products[i]['price'] == spoken_price:
                    new_candidates.append(i)
        if len(new_candidates) == 1:
            return new_candidates[0]
        
        # filter by qty
        new_candidates = []
        if spoken_qty:
            for i in candidates:
                if self.products[i]['qty'] >= spoken_qty:
                    new_candidates.append(i)
        if len(new_candidates) == 1:
            return new_candidates[0]
        
        # return the one with the highest score
        max_score = -1
        best_candidate = None
        for i in candidates:
            if self.products[i]['score'] > max_score:
                max_score = self.products[i]['score']
                best_candidate = i
        return best_candidate
    
    def commit_transaction(self, product_id: int, qty: int):
        self.cursor.execute("UPDATE stock SET qty = qty - ? WHERE p_id = ?", (qty, product_id))
        self.connection.commit()

    def start_transaction(self):
        self.transaction_running = True
        Dashboard.start_transaction()

    def stop_transaction(self):
        self.cursor.execute("INSERT INTO sale (date) VALUES (date('now'))")
        sale_id = self.cursor.lastrowid

        for p in self.current_transaction_products:
            self.cursor.execute("INSERT INTO sale_items VALUES (?, ?, ?, ?)", (sale_id, p['name'], p['price'], p['qty']))
        
        self.connection.commit()

        self.current_transaction_products.clear()
        self.transaction_running = False
        Dashboard.stop_transaction()
