import csv
import os
from datetime import datetime
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# --- Theme & Branding ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

ACCOUNTS_FILE = "accounts.csv"
TRANSACTIONS_FILE = "transaction.csv"


def initialize_files():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["AccountNo", "PIN", "Name", "Balance"])
            writer.writerow(["1001", "1234", "MOMIN", "5000.0"])
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Timestamp", "AccountNo", "Type", "Amount", "NewBalance"]
            )


class GreenBankApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("GreenBank | Premium FinTech")
        self.geometry("480x780")
        self.configure(fg_color="#0F0F0F")  # Deep black background
        self.current_user = None
        initialize_files()
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # --- Utility: In-App Toast/Notification ---
    def show_toast(self, message, is_error=False):
        toast = ctk.CTkFrame(
            self,
            fg_color="#C0392B" if is_error else "#27AE60",
            corner_radius=10,
        )
        toast.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.85)

        lbl = ctk.CTkLabel(
            toast,
            text=message,
            text_color="white",
            font=("Roboto", 12, "bold"),
            wraplength=350,
        )
        lbl.pack(pady=10, padx=15)

        # Auto dismiss after 2.5 seconds
        self.after(2500, toast.destroy)

    # --- Modern Login UI ---
    def show_login(self):
        self.clear()

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(50, 20))

        ctk.CTkLabel(
            header_frame,
            text="G",
            text_color="#2ECC71",
            font=("Roboto", 60, "bold"),
        ).pack(side="left")
        ctk.CTkLabel(
            header_frame,
            text="reenBank",
            text_color="white",
            font=("Roboto", 40, "bold"),
        ).pack(side="left")

        login_frame = ctk.CTkFrame(
            self,
            fg_color="#1A1A1A",
            corner_radius=20,
            border_width=1,
            border_color="#333333",
        )
        login_frame.pack(pady=10, padx=40, fill="both", expand=True)

        ctk.CTkLabel(
            login_frame,
            text="Secure Access",
            font=("Roboto", 18, "bold"),
            text_color="#AAAAAA",
        ).pack(pady=(25, 15))

        self.acc_ent = ctk.CTkEntry(
            login_frame,
            placeholder_text="Account Number",
            height=45,
            fg_color="#0F0F0F",
            border_color="#2ECC71",
        )
        self.acc_ent.pack(pady=10, padx=30, fill="x")

        self.pin_ent = ctk.CTkEntry(
            login_frame,
            placeholder_text="PIN Code",
            show="*",
            height=45,
            fg_color="#0F0F0F",
            border_color="#2ECC71",
        )
        self.pin_ent.pack(pady=10, padx=30, fill="x")

        ctk.CTkButton(
            login_frame,
            text="SIGN IN",
            font=("Roboto", 14, "bold"),
            height=45,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            text_color="black",
            command=self.login,
        ).pack(pady=25, padx=30, fill="x")

        ctk.CTkButton(
            self,
            text="Create New Account",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#2ECC71",
            command=self.show_register_modal,
        ).pack(pady=20)

    def login(self):
        try:
            acc_val = int(self.acc_ent.get().strip())
            pin_val = int(self.pin_ent.get().strip())

            df = pd.read_csv(ACCOUNTS_FILE)
            user = df[(df["AccountNo"] == acc_val) & (df["PIN"] == pin_val)]
            if not user.empty:
                self.current_user = acc_val
                self.show_dash(user.iloc[0]["Name"])
            else:
                self.show_toast(
                    "Account Number or PIN is incorrect.", is_error=True
                )
        except ValueError:
            self.show_toast(
                "Inputs must be valid numeric values.", is_error=True
            )

    # --- Native Registration Overlay ---
    def show_register_modal(self):
        overlay = ctk.CTkFrame(self, fg_color="#000000")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = ctk.CTkFrame(
            overlay,
            fg_color="#1A1A1A",
            corner_radius=20,
            border_width=1,
            border_color="#333333",
        )
        card.pack(pady=80, padx=30, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text="Open New Account",
            font=("Roboto", 20, "bold"),
            text_color="white",
        ).pack(pady=(25, 20))

        name_ent = ctk.CTkEntry(
            card,
            placeholder_text="Legal Full Name",
            height=45,
            fg_color="#0F0F0F",
            border_color="#2ECC71",
        )
        name_ent.pack(pady=10, padx=25, fill="x")

        acc_ent = ctk.CTkEntry(
            card,
            placeholder_text="Desired Account ID (Numeric)",
            height=45,
            fg_color="#0F0F0F",
            border_color="#2ECC71",
        )
        acc_ent.pack(pady=10, padx=25, fill="x")

        pin_ent = ctk.CTkEntry(
            card,
            placeholder_text="4-Digit PIN",
            show="*",
            height=45,
            fg_color="#0F0F0F",
            border_color="#2ECC71",
        )
        pin_ent.pack(pady=10, padx=25, fill="x")

        def submit():
            name = name_ent.get().strip()
            acc_str = acc_ent.get().strip()
            pin_str = pin_ent.get().strip()

            if not name or not acc_str or not pin_str:
                self.show_toast("Please fill in all fields.", is_error=True)
                return

            try:
                acc = int(acc_str)
                pin = int(pin_str)
            except ValueError:
                self.show_toast(
                    "Account ID & PIN must be numbers.", is_error=True
                )
                return

            df = pd.read_csv(ACCOUNTS_FILE)
            if acc in df["AccountNo"].values:
                self.show_toast("Account ID already registered.", is_error=True)
                return

            new_user = pd.DataFrame(
                [[acc, pin, name, 0.0]], columns=df.columns
            )
            pd.concat([df, new_user]).to_csv(ACCOUNTS_FILE, index=False)
            overlay.destroy()
            self.show_toast("Account created! Please sign in.")

        ctk.CTkButton(
            card,
            text="CREATE ACCOUNT",
            font=("Roboto", 13, "bold"),
            height=45,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            text_color="black",
            command=submit,
        ).pack(pady=(20, 10), padx=25, fill="x")

        ctk.CTkButton(
            card,
            text="Cancel",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#888888",
            command=overlay.destroy,
        ).pack(pady=5)

    # --- Dashboard UI ---
    def show_dash(self, name):
        self.clear()
        df = pd.read_csv(ACCOUNTS_FILE)
        bal = df.loc[df["AccountNo"] == self.current_user, "Balance"].values[0]

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", pady=(30, 10), padx=30)
        ctk.CTkLabel(
            top_bar,
            text="Welcome back,",
            font=("Roboto", 14),
            text_color="#888888",
        ).pack(side="left")
        ctk.CTkLabel(
            top_bar,
            text=f" {name}",
            font=("Roboto", 16, "bold"),
            text_color="#2ECC71",
        ).pack(side="left")

        # Balance Card
        card = ctk.CTkFrame(
            self, fg_color="#1B5E20", corner_radius=25, height=180
        )
        card.pack(pady=20, padx=30, fill="x")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="AVAILABLE BALANCE",
            text_color="#A5D6A7",
            font=("Roboto", 12, "bold"),
        ).pack(pady=(35, 5))
        ctk.CTkLabel(
            card,
            text=f"${bal:,.2f}",
            text_color="white",
            font=("Roboto", 44, "bold"),
        ).pack()

        # Action Grid
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(pady=10, padx=30, fill="x")

        self.action_btn(
            actions_frame,
            "Deposit Money",
            "#2ECC71",
            lambda: self.show_transact_modal("Deposit"),
        ).pack(pady=8, fill="x")
        self.action_btn(
            actions_frame,
            "Withdraw Money",
            "#F1C40F",
            lambda: self.show_transact_modal("Withdraw"),
        ).pack(pady=8, fill="x")
        self.action_btn(
            actions_frame,
            "Transfer Funds",
            "#3498DB",
            self.show_transfer_modal,
        ).pack(pady=8, fill="x")

        # Analytics Button
        ctk.CTkButton(
            self,
            text="VIEW FINANCIAL INSIGHTS",
            font=("Roboto", 13, "bold"),
            height=55,
            fg_color="#1A1A1A",
            border_width=2,
            border_color="#2ECC71",
            hover_color="#222222",
            command=self.view_graph,
        ).pack(pady=(30, 10), padx=30, fill="x")

        ctk.CTkButton(
            self,
            text="Logout Securely",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#E74C3C",
            command=self.show_login,
        ).pack(side="bottom", pady=20)

    def action_btn(self, master, text, color, cmd):
        return ctk.CTkButton(
            master,
            text=text,
            font=("Roboto", 13, "bold"),
            height=50,
            fg_color=color,
            hover_color="#555555",
            text_color="black",
            command=cmd,
        )

    # --- Native In-App Transaction Modal ---
    def show_transact_modal(self, mode):
        overlay = ctk.CTkFrame(self, fg_color="#000000")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = ctk.CTkFrame(
            overlay,
            fg_color="#1A1A1A",
            corner_radius=20,
            border_width=1,
            border_color="#333333",
        )
        card.pack(pady=180, padx=30, fill="x")

        ctk.CTkLabel(
            card,
            text=f"{mode} Funds",
            font=("Roboto", 20, "bold"),
            text_color="white",
        ).pack(pady=(25, 15))

        amt_ent = ctk.CTkEntry(
            card,
            placeholder_text="Enter Amount ($)",
            height=45,
            fg_color="#0F0F0F",
            border_color="#2ECC71",
        )
        amt_ent.pack(pady=10, padx=25, fill="x")

        def submit():
            try:
                amt = float(amt_ent.get().strip())
                if amt <= 0:
                    raise ValueError
            except ValueError:
                self.show_toast(
                    "Please enter a valid positive amount.", is_error=True
                )
                return

            df = pd.read_csv(ACCOUNTS_FILE)
            idx = df.index[df["AccountNo"] == self.current_user][0]
            curr = df.at[idx, "Balance"]

            if mode == "Withdraw" and amt > curr:
                self.show_toast("Insufficient account balance.", is_error=True)
                return

            new_bal = curr + amt if mode == "Deposit" else curr - amt
            df.at[idx, "Balance"] = new_bal
            df.to_csv(ACCOUNTS_FILE, index=False)

            with open(TRANSACTIONS_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        datetime.now().strftime("%H:%M"),
                        self.current_user,
                        mode,
                        amt,
                        new_bal,
                    ]
                )

            overlay.destroy()
            self.show_dash(df.at[idx, "Name"])
            self.show_toast(f"Successfully {mode.lower()}ed ${amt:,.2f}")

        ctk.CTkButton(
            card,
            text=f"CONFIRM {mode.upper()}",
            font=("Roboto", 13, "bold"),
            height=45,
            fg_color="#2ECC71" if mode == "Deposit" else "#F1C40F",
            hover_color="#27AE60" if mode == "Deposit" else "#D4AC0D",
            text_color="black",
            command=submit,
        ).pack(pady=(20, 10), padx=25, fill="x")

        ctk.CTkButton(
            card,
            text="Cancel",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#888888",
            command=overlay.destroy,
        ).pack(pady=(0, 20))

    # --- Native In-App Transfer Modal ---
    def show_transfer_modal(self):
        overlay = ctk.CTkFrame(self, fg_color="#000000")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = ctk.CTkFrame(
            overlay,
            fg_color="#1A1A1A",
            corner_radius=20,
            border_width=1,
            border_color="#333333",
        )
        card.pack(pady=150, padx=30, fill="x")

        ctk.CTkLabel(
            card,
            text="Transfer Funds",
            font=("Roboto", 20, "bold"),
            text_color="white",
        ).pack(pady=(25, 15))

        target_ent = ctk.CTkEntry(
            card,
            placeholder_text="Recipient Account ID",
            height=45,
            fg_color="#0F0F0F",
            border_color="#3498DB",
        )
        target_ent.pack(pady=10, padx=25, fill="x")

        amt_ent = ctk.CTkEntry(
            card,
            placeholder_text="Transfer Amount ($)",
            height=45,
            fg_color="#0F0F0F",
            border_color="#3498DB",
        )
        amt_ent.pack(pady=10, padx=25, fill="x")

        def submit():
            try:
                target = int(target_ent.get().strip())
                amt = float(amt_ent.get().strip())
                if amt <= 0:
                    raise ValueError
            except ValueError:
                self.show_toast(
                    "Enter valid numeric values for Account & Amount.",
                    is_error=True,
                )
                return

            if target == self.current_user:
                self.show_toast(
                    "Cannot transfer money to yourself.", is_error=True
                )
                return

            df = pd.read_csv(ACCOUNTS_FILE)
            if target not in df["AccountNo"].values:
                self.show_toast(
                    "Recipient Account ID not found.", is_error=True
                )
                return

            s_idx = df.index[df["AccountNo"] == self.current_user][0]
            r_idx = df.index[df["AccountNo"] == target][0]

            if amt > df.at[s_idx, "Balance"]:
                self.show_toast("Insufficient balance.", is_error=True)
                return

            df.at[s_idx, "Balance"] -= amt
            df.at[r_idx, "Balance"] += amt
            df.to_csv(ACCOUNTS_FILE, index=False)

            t = datetime.now().strftime("%H:%M")
            with open(TRANSACTIONS_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        t,
                        self.current_user,
                        f"To {target}",
                        amt,
                        df.at[s_idx, "Balance"],
                    ]
                )
                writer.writerow(
                    [
                        t,
                        target,
                        f"From {self.current_user}",
                        amt,
                        df.at[r_idx, "Balance"],
                    ]
                )

            overlay.destroy()
            self.show_dash(df.at[s_idx, "Name"])
            self.show_toast(f"Transferred ${amt:,.2f} to Account {target}")

        ctk.CTkButton(
            card,
            text="CONFIRM TRANSFER",
            font=("Roboto", 13, "bold"),
            height=45,
            fg_color="#3498DB",
            hover_color="#2980B9",
            text_color="white",
            command=submit,
        ).pack(pady=(20, 10), padx=25, fill="x")

        ctk.CTkButton(
            card,
            text="Cancel",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#888888",
            command=overlay.destroy,
        ).pack(pady=(0, 20))

    # --- Analytics Window ---
    def view_graph(self):
        try:
            df = pd.read_csv(TRANSACTIONS_FILE, on_bad_lines="skip")
            df.columns = df.columns.str.strip()
            data = df[df["AccountNo"] == self.current_user]

            if data.empty:
                self.show_toast(
                    "No transaction history available.", is_error=True
                )
                return

            win = ctk.CTkToplevel(self)
            win.title("Financial Analysis Dashboard")
            win.geometry("950x550")

            plt.style.use("dark_background")
            fig = plt.figure(figsize=(14, 6), facecolor="#0F0F0F")

            ax1 = fig.add_subplot(131)
            ax1.plot(
                data["Timestamp"],
                data["NewBalance"],
                marker="o",
                color="#2ECC71",
            )
            ax1.set_title("Balance Trend")
            plt.setp(ax1.get_xticklabels(), rotation=45)

            ax2 = fig.add_subplot(132)
            summary = data.groupby("Type")["Amount"].sum()
            ax2.bar(
                summary.index,
                summary.values,
                color=["#2ECC71", "#F1C40F", "#3498DB"],
            )
            ax2.set_title("Volume Split")

            ax3 = fig.add_subplot(133)
            counts = data["Type"].value_counts()
            ax3.pie(
                counts,
                labels=counts.index,
                autopct="%1.1f%%",
                colors=["#1B5E20", "#D4AC0D", "#2980B9"],
            )
            ax3.set_title("Activity Split")

            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=win)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            self.show_toast(f"Failed to load insights: {e}", is_error=True)


if __name__ == "__main__":
    app = GreenBankApp()
    app.mainloop()