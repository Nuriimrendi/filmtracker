import csv
import os
from PyQt5.QtWidgets import QMessageBox

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.watched_path = os.path.join(self.data_dir, "watched_films.csv")
        self.watchlist_path = os.path.join(self.data_dir, "watchlist.csv")
        self.init_storage()

    def init_storage(self):
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize watched films CSV
        if not os.path.exists(self.watched_path):
            with open(self.watched_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Director", "Year", "Rating", "Comments", "Watch Date"])
                
        # Initialize watchlist CSV
        if not os.path.exists(self.watchlist_path):
            with open(self.watchlist_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Added Date"])

    def update_watched_film(self, original_data, new_data):
        try:
            # Read all films
            with open(self.watched_path, 'r', encoding='utf-8') as f:
                films = list(csv.reader(f))
                header = films[0]
                films = films[1:]
                
            # Find and replace
            for idx, film in enumerate(films):
                if film == original_data:
                    films[idx] = new_data
                    break
                    
            # Write back all data
            with open(self.watched_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(films)
                
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Update failed: {str(e)}")
            return False
    
    def delete_watched_film(self, film_data):
        try:
            with open(self.watched_path, 'r', encoding='utf-8') as f:
                films = list(csv.reader(f))
                header = films[0]
                films = films[1:]
                
            # Remove matching entry
            new_films = [film for film in films if film != film_data]
            
            # Write back remaining films
            with open(self.watched_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(new_films)
                
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Delete failed: {str(e)}")
            return False
    
    def get_watched_films(self):
        try:
            with open(self.watched_path, 'r', encoding='utf-8') as f:
                return list(csv.reader(f))[1:]  # Skip header
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load data: {str(e)}")
            return []

    def add_watched_film(self, film_data):
        try:
            with open(self.watched_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(film_data)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save data: {str(e)}")
            return False
    
    def get_watchlist(self):
        try:
            with open(self.watchlist_path, 'r', encoding='utf-8') as f:
                return list(csv.reader(f))[1:]  # Skip header
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load watchlist: {str(e)}")
            return []

    def add_to_watchlist(self, item_data):
        try:
            with open(self.watchlist_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(item_data)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save watchlist: {str(e)}")
            return False
    
    def update_watchlist(self, original_data, new_data):
        try:
            with open(self.watchlist_path, 'r', encoding='utf-8') as f:
                items = list(csv.reader(f))
                header = items[0]
                items = items[1:]
                
            for idx, item in enumerate(items):
                if item == original_data:
                    items[idx] = new_data
                    break
                    
            with open(self.watchlist_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(items)
                
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Watchlist update failed: {str(e)}")
            return False

    def delete_watchlist(self, item_data):
        try:
            with open(self.watchlist_path, 'r', encoding='utf-8') as f:
                items = list(csv.reader(f))
                header = items[0]
                items = items[1:]
                
            new_items = [item for item in items if item != item_data]
            
            with open(self.watchlist_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(new_items)
                
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Watchlist delete failed: {str(e)}")
            return False