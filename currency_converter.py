# ==========================================
# PROFESSIONAL CURRENCY CONVERTER PRO
# PART 1
# ==========================================

import customtkinter as ctk
import requests
import pandas as pd
import csv
import threading

from datetime import datetime
from tkinter import (
    ttk,
    messagebox,
    filedialog
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================
# APP CONFIG
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==========================================
# API CONFIG
# ==========================================

CSV_FILE = "history.csv"


# ==========================================
# CURRENCIES
# ==========================================

CURRENCIES = {
    "🇺🇸 USD": "USD",
    "🇪🇺 EUR": "EUR",
    "🇬🇧 GBP": "GBP",
    "🇧🇩 BDT": "BDT",
    "🇮🇳 INR": "INR",
    "🇵🇰 PKR": "PKR",
    "🇯🇵 JPY": "JPY",
    "🇨🇳 CNY": "CNY",
    "🇦🇺 AUD": "AUD",
    "🇨🇦 CAD": "CAD",
    "🇸🇬 SGD": "SGD",
    "🇦🇪 AED": "AED",
    "🇸🇦 SAR": "SAR",
    "🇲🇾 MYR": "MYR",
    "🇨🇭 CHF": "CHF"
}


# ==========================================
# CREATE CSV IF NOT EXISTS
# ==========================================

def create_csv():

    try:
        with open(CSV_FILE, "x", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Amount",
                "From",
                "To",
                "Rate",
                "Result"
            ])

    except FileExistsError:
        pass


create_csv()


# ==========================================
# MAIN APP
# ==========================================

class CurrencyConverterApp:

    def __init__(self, root):

        self.root = root

        try:
            self.root.iconbitmap(
                "currency.ico"
            )

        except:
            pass
        
        self.root.title(
            "Professional Currency Converter Pro"
        )

        self.root.geometry("830x570")

        self.root.minsize(800, 500)

        self.current_rate = 0

        self.build_ui()

        self.load_history()


    # ======================================
    # BUILD UI
    # ======================================

    def build_ui(self):

        # --------------------------
        # HEADER
        # --------------------------

        self.title_label = ctk.CTkLabel(
            self.root,
            text="💱 PROFESSIONAL CURRENCY CONVERTER",
            font=("Arial", 30, "bold"),
             text_color="red"
        )

        self.title_label.pack(
            pady=5
        )

        # --------------------------
        # MAIN FRAME
        # --------------------------

        self.main_frame = ctk.CTkFrame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8
        )

        # --------------------------
        # LEFT PANEL
        # --------------------------

        self.left_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=6
        )

        # --------------------------
        # AMOUNT
        # --------------------------

        self.amount_label = ctk.CTkLabel(
            self.left_frame,
            text="Amount",
            font=("Arial", 14, "bold")
        )

        self.amount_label.pack(
            pady=(10, 5)
        )

        self.amount_entry = ctk.CTkEntry(
            self.left_frame,
            width=200,
            height=30,
            font=("Arial", 14, "bold" )
        )

        self.amount_entry.pack()

        # --------------------------
        # FROM
        # --------------------------

        self.from_label = ctk.CTkLabel(
            self.left_frame,
            text="From Currency",
            font=("Arial", 14, "bold")
        )

        self.from_label.pack(
            pady=(8, 5)
        )

        self.from_currency = ctk.CTkComboBox(
            self.left_frame,
            values=list(CURRENCIES.keys()),
            width=200
        )

        self.from_currency.pack()

        self.from_currency.set(
            "🇺🇸 USD"
        )

        self.from_currency.configure(
            command=lambda e:
            self.auto_convert()
        )

        # --------------------------
        # TO
        # --------------------------

        self.to_label = ctk.CTkLabel(
            self.left_frame,
            text="To Currency",
            font=("Arial", 14, "bold")
        )

        self.to_label.pack(
            pady=(8, 5)
        )

        self.to_currency = ctk.CTkComboBox(
            self.left_frame,
            values=list(CURRENCIES.keys()),
            width=200
        )

        self.to_currency.pack()

        self.to_currency.set(
            "🇧🇩 BDT"
        )

        self.to_currency.configure(
            command=lambda e:
            self.auto_convert()
        )

        # --------------------------
        # RESULT
        # --------------------------

        self.result_label = ctk.CTkLabel(
            self.left_frame,
            text="0.00",
            font=("Arial", 24, "bold"),
            text_color="red"
        )

        self.result_label.pack(
            pady=10
        )

        # --------------------------
        # RATE LABEL
        # --------------------------

        self.rate_label = ctk.CTkLabel(
            self.left_frame,
            text="Exchange Rate: --",
            font=("Arial", 20),
            text_color="green"
        )

        self.rate_label.pack()

        # =============
        # HISTORY TABLE
        # =============

        self.history_label = ctk.CTkLabel(
            self.main_frame,
            text="Conversion History",
            font=("Arial", 16, "bold")
        )

        self.history_label.pack(
            pady=(8, 5)
        )

        self.table_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "Date",
            "Amount",
            "From",
            "To",
            "Rate",
            "Result"
        )

        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=28,
            borderwidth=1,
            relief="solid"
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        self.history_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=4,
            style="Treeview"
        )

        for col in columns:

            self.history_table.heading(
                col,
                text=col
            )

            self.history_table.column(
                col,
                anchor="center",
                width=120
            )

        self.history_table.pack(
            fill="both",
            expand=True
        )

        self.history_table.tag_configure(
            "odd",
            background="#F0F0F0"
        )

        self.history_table.tag_configure(
            "even",
            background="#FFFFFF"
        )

        # -------------------------
        # BUTTONS FRAME
        # -------------------------

        self.button_frame = ctk.CTkFrame(
            self.left_frame
        )

        self.button_frame.pack(
            pady=10
        )

        self.convert_btn = ctk.CTkButton(
            self.button_frame,
            text="Convert",
            width=140,
            height=38,
            command=self.convert_thread
        )

        self.convert_btn.grid(
            row=0,
            column=0,
            padx=2
        )

        self.export_btn = ctk.CTkButton(
            self.button_frame,
            text="Export CSV",
            width=140,
            height=38,
            command=self.export_csv
        )

        self.export_btn.grid(
            row=1,
            column=0,
            pady=5,
            padx=2
        )

        self.swap_btn = ctk.CTkButton(
            self.button_frame,
            text="Swap",
            width=140,
            height=38,
            command=self.swap_currency
        )

        self.swap_btn.grid(
            row=0,
            column=1,
            padx=2
        )

        self.graph_btn = ctk.CTkButton(
            self.button_frame,
            text="Trend Graph",
            width=140,
            height=38,
            command=self.show_trend_graph
        )

        self.graph_btn.grid(
            row=2,
            column=0,
            pady=5,
            padx=2
        )

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear History",
            width=140,
            height=38,
            command=self.clear_history
        )

        self.clear_btn.grid(
            row=2,
            column=1,
            pady=5,
            padx=2
        )

        self.refresh_btn = ctk.CTkButton(
            self.button_frame,
            text="Refresh",
            width=140,
            height=38,
            command=self.refresh_app
        )

        self.refresh_btn.grid(
            row=1,
            column=1,
            pady=5,
            padx=2
        )

        # -------------------------
        # DARK MODE
        # -------------------------

        self.theme_switch = ctk.CTkSwitch(
            self.left_frame,
            text="Dark Mode",
            command=self.change_theme
        )

        self.theme_switch.select()

        self.theme_switch.pack(
            pady=2
        )

        # -------------------------
        # STATUS BAR
        # -------------------------

        self.status_label = ctk.CTkLabel(
            self.root,
            text="Ready",
            anchor="w"
        )

        self.status_label.pack(
            fill="x",
            padx=8,
            pady=3
        )


    # =============
    # AUTO CONVERT
    # =============
    def auto_convert(self, event=None):

        amount = self.amount_entry.get().strip()

        if amount == "":
            self.result_label.configure(text="0.00")
            return

        # শুধু preview
        self.status_label.configure(
            text="Ready to Convert"
        )

    # ===============
    # CONVERT THREAD
    # ===============
    def convert_thread(self):

        threading.Thread(
            target=self.convert,
            daemon=True
        ).start()

    
    # ========
    # CONVERT
    # ========

    def convert(self):

        try:

            amount = float(
                self.amount_entry.get().strip()
            )

            from_cur = CURRENCIES[
                self.from_currency.get()
            ]

            to_cur = CURRENCIES[
                self.to_currency.get()
            ]

            self.status_label.configure(
                text="Fetching live rate..."
            )

            try:

                response = requests.get(
                    f"https://open.er-api.com/v6/latest/{from_cur}",
                    timeout=10
                )

                data = response.json()

            except requests.exceptions.RequestException:

                messagebox.showerror(
                    "Network Error",
                    "Check Internet Connection"
                )
                return

            if data.get("result") != "success":
                raise Exception("API Error")

            rate = data["rates"][to_cur]

            result = amount * rate

            self.current_rate = rate

            self.result_label.configure(
                text=f"{result:,.2f} {to_cur}"
            )

            self.rate_label.configure(
                text=f"Exchange Rate : {rate:.2f}"
            )

            self.status_label.configure(
                text="Conversion completed"
            )

            self.save_history(
                amount,
                from_cur,
                to_cur,
                rate,
                result
            )

        except Exception as e:

            self.status_label.configure(
                text="Error fetching data"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )


    # =============
    # SAVE HISTORY
    # =============

    def save_history(
        self,
        amount,
        from_cur,
        to_cur,
        rate,
        result
    ):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                now,
                f"{amount:.2f}",
                from_cur,
                to_cur,
                f"{rate:.2f}",
                f"{result:.2f}"
            ])

        self.load_history()


    # =============
    # LOAD HISTORY
    # =============

    def load_history(self):

        for item in self.history_table.get_children():

            self.history_table.delete(item)

        try:

            df = pd.read_csv(
                CSV_FILE
            )

            for index, (_, row) in enumerate(df.tail(50).iterrows()):

                self.history_table.insert(
                    "",
                    "end",
                    values=(
                        row["Date"],
                        f"{float(row['Amount']):.2f}",
                        row["From"],
                        row["To"],
                        f"{float(row['Rate']):.2f}",
                        f"{float(row['Result']):.2f}"
                    ),
                    tags=("even" if index % 2 == 0 else "odd",)
                )

        except:
            pass

    # =====
    # SWAP
    # =====
    def swap_currency(self):

        from_cur = self.from_currency.get()

        to_cur = self.to_currency.get()

        self.from_currency.set(to_cur)

        self.to_currency.set(from_cur)

        if self.amount_entry.get().strip():

            self.convert_thread()
            
    # ===========
    # EXPORT CSV
    # ===========
    def export_csv(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not file_path:
            return

        df = pd.read_csv(CSV_FILE)

        df.to_csv(
            file_path,
            index=False
        )

        messagebox.showinfo(
            "Export",
            "CSV Export Successful"
        )


    # ======================================
    # CHANGE THEME
    # ======================================

    def change_theme(self):

        if self.theme_switch.get() == 1:

            ctk.set_appearance_mode(
                "dark"
            )

        else:

            ctk.set_appearance_mode(
                "light"
            )

    # =================
    # SHOW TREND GRAPH
    # =================

    def show_trend_graph(self):

        try:

            df = pd.read_csv(CSV_FILE)

            if len(df) < 2:

                messagebox.showwarning(
                    "No Data",
                    "Not enough history data."
                )

                return

            graph_window = ctk.CTkToplevel(
                self.root
            )

            graph_window.title(
                "Currency Conversion Trend"
            )

            graph_window.geometry(
                "600x400"
            )

            fig = plt.Figure(
                figsize=(9, 5),
                dpi=100
            )

            ax = fig.add_subplot(111)

            x_data = list(
                range(
                    1,
                    len(df) + 1
                )
            )

            y_data = df["Rate"]

            ax.plot(
                x_data,
                y_data,
                marker="o"
            )

            ax.set_title(
                "Exchange Rate Trend"
            )

            ax.set_xlabel(
                "Conversion Number"
            )

            ax.set_ylabel(
                "Rate"
            )

            ax.grid(True)

            canvas = FigureCanvasTkAgg(
                fig,
                master=graph_window
            )

            canvas.draw()

            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

        except Exception as e:

            messagebox.showerror(
                "Graph Error",
                str(e)
            )


    # ======================================
    # CLEAR HISTORY
    # ======================================

    def clear_history(self):

        answer = messagebox.askyesno(
            "Confirm",
            "Delete all history?"
        )

        if not answer:
            return

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Amount",
                "From",
                "To",
                "Rate",
                "Result"
            ])

        self.load_history()

        messagebox.showinfo(
            "Success",
            "History Cleared"
        )


    # ======================================
    # REFRESH
    # ======================================

    def refresh_app(self):

        self.amount_entry.delete(
            0,
            "end"
        )

        self.from_currency.set(
            "🇺🇸 USD"
        )

        self.to_currency.set(
            "🇧🇩 BDT"
        )

        self.result_label.configure(
            text="0.00"
        )

        self.rate_label.configure(
            text="Exchange Rate: --"
        )

        self.status_label.configure(
            text="Ready"
        )


    # ======================================
    # ABOUT
    # ======================================

    def about(self):

        messagebox.showinfo(
            "About",
            "Professional Currency Converter Pro\n\n"
            "Features:\n"
            "• Live Exchange Rate API\n"
            "• Currency Flags\n"
            "• Auto Convert\n"
            "• CSV History\n"
            "• Trend Graph\n"
            "• Dark / Light Mode\n"
            "• Professional UI"
        )

# ==========================================
# START APP
# ==========================================

if __name__ == "__main__":

    root = ctk.CTk()

    app = CurrencyConverterApp(root)

    root.mainloop()
    
