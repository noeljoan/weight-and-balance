"""
Tkinter-basierte grafische Oberfläche für Cessna-172 Weight & Balance Berechnung.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .item import WeightItem
from .calculator import WeightAndBalance

# Typische Arm-Positionen für Cessna-172 (aus POH)
ARM_VALUES = {
    "Pilot": 36.0,
    "Copilot": 36.0,
    "Beifahrzeuge vorne": 73.0,
    "Beifahrzeuge hinten": 84.0,
    "Gepäck (vorne)": 95.0,
    "Gepäck (hinten)": 115.0,
    "Kraftstoff": 48.0,
}


class WeightBalanceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Cessna-172 Weight & Balance Calculator")
        master.geometry("500x600")
        master.resizable(True, True)

        self.entries = {}

        # Haupt-Frame
        main_frame = ttk.Frame(master, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Konfiguriere Grid-Gewichtung
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Überschrift
        ttk.Label(main_frame, text="Gewicht und Schwerpunkt - Cessna 172",
                  font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 10))

        # Eingabefelder für jeden Posten
        row = 1
        for name, default_arm in ARM_VALUES.items():
            ttk.Label(main_frame, text=f"{name}:").grid(
                row=row, column=0, sticky=tk.W, pady=3)

            weight_var = tk.DoubleVar(value=0.0)
            weight_entry = ttk.Entry(main_frame, textvariable=weight_var, width=10)
            weight_entry.grid(row=row, column=1, sticky=tk.W, padx=5)

            ttk.Label(main_frame, text="lb").grid(
                row=row, column=2, sticky=tk.W)

            self.entries[name] = {
                "weight_var": weight_var,
                "arm": default_arm
            }
            row += 1

        # Berechnen-Button
        ttk.Button(main_frame, text="Berechnen", command=self.calculate).grid(
            row=row, column=0, columnspan=3, pady=15)
        row += 1

        # Ergebnis-Frame
        result_frame = ttk.LabelFrame(main_frame, text="Ergebnis", padding=10)
        result_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E))
        row += 1

        self.result_text = tk.Text(result_frame, width=55, height=12,
                                   font=("Consolas", 10))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.result_text.configure(state="disabled")

        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical",
                                   command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text["yscrollcommand"] = scrollbar.set

        # Statuszeile
        self.status_var = tk.StringVar(value="Bereit")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E),
                          pady=(10, 0))

        # Grid-Konfiguration für Ergebnisfeld
        main_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

    def calculate(self):
        """Berechnet das Ergebnis basierend auf den Eingaben."""
        items = []

        for name, entry in self.entries.items():
            weight = entry["weight_var"].get()
            if weight > 0:
                items.append(WeightItem(name, weight, entry["arm"]))

        if not items:
            messagebox.showwarning("Warnung", "Bitte geben Sie mindestens ein Gewicht ein.")
            return

        try:
            wb = WeightAndBalance(items)
            report = wb.report()

            self.result_text.configure(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, report)
            self.result_text.configure(state="disabled")

            ok, _ = wb.is_within_limits()
            if ok:
                self.status_var.set("✓ Alle Parameter innerhalb der Grenzen")
            else:
                self.status_var.set("✗ Außerhalb der zulässigen Grenzen!")

        except Exception as e:
            messagebox.showerror("Fehler", str(e))


def main():
    root = tk.Tk()
    app = WeightBalanceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()