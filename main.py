import time
from src import logger
from src import db_handler as db
from src import customtkinter as ui
from src import key
from src import sha3

version: str = "Main v.0.9 alpha"

btn_text_color: tuple[str, str] = ("#202020", "#dddddd")
btn_hover_color: tuple[str, str] = ("#9bb1ba", "#3d464a")


def std():
    time.sleep(0.1)
    quit()


def user_init():
    try:
        with open("public_key.bin", "rb") as pk:
            public_key: str = pk.read().decode("utf-8")
        user: str = db.db.get(table_name="users",
                              column="user",
                              where=("public_key",
                                     public_key))[0][0]
    except IndexError:
        return "No login"
    except FileNotFoundError:
        return "No login"
    else:
        log(f"Successfully logged in by [{user}]")
        return user


class MainWindow(ui.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400+500+200")
        self.minsize(700, 400)
        self.title("Слышу ZOV - ебать Азов")
        self.settings_window = None
        self.login_window = None
        self.hi_font = ui.CTkFont("Segoe UI Variable", 25, "bold")

        # Account data
        self.account_username: str = user_init()

        # Widgets
        self.top_bar = ui.CTkFrame(self, corner_radius=0)
        self.bottom_bar = ui.CTkFrame(self, corner_radius=0)
        self.exit_b = ui.CTkButton(self.top_bar, text="Exit", width=40, command=std, corner_radius=5,
                                   fg_color="transparent", text_color=btn_text_color,
                                   hover_color=btn_hover_color)
        self.user = ui.CTkLabel(self.top_bar, text=self.account_username, text_color=btn_text_color, corner_radius=5,
                                fg_color=btn_hover_color, anchor="w", padx=5)
        self.settings_b = ui.CTkButton(self.top_bar, text="Settings", width=70, corner_radius=5,
                                       fg_color="transparent", command=self.open_settings, text_color=btn_text_color,
                                       hover_color=btn_hover_color)
        self.about_b = ui.CTkButton(self.top_bar, text="About", width=50, corner_radius=5,
                                    fg_color="transparent", text_color=btn_text_color,
                                    hover_color=btn_hover_color)
        self.version = ui.CTkLabel(self.bottom_bar, text=f"{version};   {logger.version};   {db.version}",
                                   text_color="#7a7a7a")
        self.warning = ui.CTkLabel(self.bottom_bar, text="No problems", anchor="center")

        # Widgets placement
        self.top_bar.grid(row=0, column=0, sticky="new")
        self.bottom_bar.grid(row=10, column=0, sticky="sew")
        self.exit_b.grid(row=0, column=3, padx=5, sticky="e")
        self.user.grid(row=0, column=0, padx=(5, 2), pady=5, sticky='w')
        self.settings_b.grid(row=0, column=1, padx=2, sticky="w")
        self.about_b.grid(row=0, column=2, padx=2, sticky="w")
        self.version.grid(row=0, column=1, padx=10, pady=5, sticky="es")
        self.warning.grid(row=0, column=0, padx=10, pady=5, sticky="ws")

        # Grid config
        self.rowconfigure(2, weight=1)
        self.rowconfigure(10, weight=1)
        self.columnconfigure("all", weight=1)
        self.top_bar.columnconfigure(3, weight=1)
        self.bottom_bar.columnconfigure("all", weight=1)

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()

    def open_login(self):
        if self.login_window is None or not self.login_window.winfo_exists():
            self.login_window = LoginWindow(self)
        else:
            self.login_window.focus()


class SettingsWindow(ui.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Settings")

        self.appearance = ui.StringVar(value="Dark")

        self.appearance_picker = ui.CTkOptionMenu(self, values=["Light", "Dark"], command=self.appearance_switcher,
                                                  variable=self.appearance)

        self.appearance_picker.grid(row=0, column=0, padx=10, pady=10)

    def appearance_switcher(self, choice: str):
        ui.set_appearance_mode(choice)
        self.appearance.set(value=choice)


class LoginWindow(ui.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x250")
        self.resizable(False, False)
        self.title("Login")

        # Widgets
        self.label = ui.CTkLabel(self, text="Please log in", font=app.hi_font)
        self.entries_frame = ui.CTkFrame(self, corner_radius=0)
        self.username = ui.CTkEntry(self.entries_frame, placeholder_text="Username", corner_radius=2, border_width=0)
        self.password = ui.CTkEntry(self.entries_frame, placeholder_text="Password", corner_radius=2, border_width=0)
        self.exit_b = ui.CTkButton(self, text="Exit", command=std, corner_radius=2)
        self.login_b = ui.CTkButton(self, text="Log in", command=self.check_out, corner_radius=2)

        # Widgets placement
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan=2)
        self.entries_frame.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="new", columnspan=2)
        self.username.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="new")
        self.password.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="new")
        self.exit_b.grid(row=2, column=0, padx=10, pady=10, sticky="sw")
        self.login_b.grid(row=2, column=1, padx=10, pady=10, sticky="se")

        # Grid configure
        self.columnconfigure(0, weight=1)
        self.entries_frame.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def check_out(self):
        username = self.username.get()
        password = self.password.get()
        password = sha3.sha3_256(password)
        try:
            if db.db.get(table_name="users", column="pswd", where=("user", username))[0][0] == password:
                public_key = key.get_public_key().encode("utf-8")
                with open("public_key.bin", "wb") as pk:
                    pk.write(public_key)
                public_key = public_key.decode("utf-8")
                db.db.update(table_name="users", where=("user", username), public_key=public_key)
                app.account_username = username
                app.user.configure(text=username)
                login_window.withdraw()
                app.deiconify()
            else:
                log("Incorrect data has been entered", "Warning")
        except IndexError:
            log("Incorrect data has been entered", "Warning")


if __name__ == "__main__":
    log = logger.log
    app = MainWindow()
    if app.account_username == "No login":
        login_window = LoginWindow()
        app.iconify()
    app.mainloop()
