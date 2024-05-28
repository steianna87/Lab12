from dataclasses import dataclass

from model.retailer import Retailer


@dataclass
class Connessione:
    retailer1: Retailer
    retailer2: Retailer
    peso: int

    def __hash__(self):
        return hash((self.retailer1.Retailer_code, self.retailer2.Retailer_code))

    def __str__(self):
        return f"{self.retailer1.Retailer_name} - {self.retailer2.Retailer_name}, peso: {self.peso}"
