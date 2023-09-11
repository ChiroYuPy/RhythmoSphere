import csv


class CircleManager:
    def __init__(self):
        self.circle_data = []

    def load_map(self, filename):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) == 3:
                        time, circle_x, circle_y = map(float, row)
                        self.circle_data.append([time, circle_x, circle_y, False])
        except FileNotFoundError:
            print(f"Le fichier {filename} n'existe pas.")