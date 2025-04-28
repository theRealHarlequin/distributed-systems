import os

class Tabelle:
    def __init__(self):
        self.name = ""
        self.spalten = []
        self.daten = []

    def tabelle_erstellen(self, name, spalten):
        """Erstellt die Tabelle mit Name und Spaltenüberschriften."""
        self.name = name
        self.spalten = spalten
        self.daten = []
        self._konsole_leeren()
        print(f"Tabelle '{name}' mit Spalten {spalten} erstellt.")

    def daten_hinzufuegen(self, werte):
        """Fügt eine neue Zeile mit Werten hinzu und zeigt die Tabelle an."""
        if len(werte) != len(self.spalten):
            print("Fehler: Anzahl der Werte stimmt nicht mit Anzahl der Spalten überein!")
            return

        self.daten.append(werte)
        self._konsole_leeren()
        self._tabelle_anzeigen()

    def _tabelle_anzeigen(self):
        """Gibt die Tabelle mit Rahmen und zentrierten Werten aus."""
        # Spaltenbreite berechnen
        spalten_breiten = [len(spalte) for spalte in self.spalten]
        for zeile in self.daten:
            for i, wert in enumerate(zeile):
                spalten_breiten[i] = max(spalten_breiten[i], len(str(wert)))

        # Hilfsfunktionen für Rahmen
        def rahmen_zeile():
            return "+" + "+".join("-" * (breite + 2) for breite in spalten_breiten) + "+"

        def zeile_formatieren(zeile):
            return "|" + "|".join(f" {str(wert).center(breite)} " for wert, breite in zip(zeile, spalten_breiten)) + "|"

        # Tabelle ausgeben
        print(self.name)
        print(rahmen_zeile())
        print(zeile_formatieren(self.spalten))
        print(rahmen_zeile())
        for zeile in self.daten:
            print(zeile_formatieren(zeile))
        print(rahmen_zeile())

    def _konsole_leeren(self):
        """Cleart die Konsole (für Windows, Linux, Mac)."""
        os.system('cls' if os.name == 'nt' else 'clear')

# Beispiel:
if __name__ == "__main__":
    import time

    tabelle = Tabelle()
    tabelle.tabelle_erstellen("Mitarbeiter", ["ID", "Name", "Position"])

    tabelle.daten_hinzufuegen([1, "Anna", "Manager"])
    time.sleep(2)  # Nur damit man sieht, was passiert
    tabelle.daten_hinzufuegen([2, "Ben", "Entwickler"])
    time.sleep(2)
    tabelle.daten_hinzufuegen([3, "Clara", "Designer"])
