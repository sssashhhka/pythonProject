import time
import utilities.log as log
import utilities.db_handler as db
from libs import customtkinter as ui

version: str = "Main v.0.9 alpha"

btn_text_color: tuple[str, str] = ("#202020", "#dddddd")
btn_hover_color: tuple[str, str] = ("#9bb1ba", "#3d464a")


class Tools:
    @staticmethod
    def exit():
        time.sleep(0.1)
        exit()


class MainWindow(ui.CTk):
    def __init__(self):
        super().__init__()
        logg.console_out(version, "Version")
        self.geometry("700x400+500+200")
        self.minsize(700, 400)
        self.title("Слышу ZOV - ебать Азов")
        self.settings_window = None
        self.login_window = None
        self.hi_font = ui.CTkFont("Segoe UI Variable", 25, "bold")

        # Account data
        self.account_username: str = "No login"

        # Widgets
        self.top_bar = ui.CTkFrame(self, corner_radius=0)
        self.bottom_bar = ui.CTkFrame(self, corner_radius=0)
        self.exit_b = ui.CTkButton(self.top_bar, text="Exit", width=40, command=Tools.exit, corner_radius=0,
                                   fg_color="transparent", text_color=btn_text_color,
                                   hover_color=btn_hover_color)
        self.user_b = ui.CTkButton(self.top_bar, text=self.account_username, corner_radius=0,
                                   fg_color="transparent", text_color=btn_text_color,
                                   hover_color=btn_hover_color)
        self.settings_b = ui.CTkButton(self.top_bar, text="Settings", width=70, corner_radius=0,
                                       fg_color="transparent", command=self.open_settings, text_color=btn_text_color,
                                       hover_color=btn_hover_color)
        self.about_b = ui.CTkButton(self.top_bar, text="About", width=50, corner_radius=0,
                                    fg_color="transparent", text_color=btn_text_color,
                                    hover_color=btn_hover_color)
        self.version = ui.CTkLabel(self.bottom_bar, text=f"{version};   {log.version};   {db.version}", text_color="#7a7a7a")
        self.warning = ui.CTkLabel(self.bottom_bar, text="You must to be logged in before proceeding", anchor="center")

        # Widgets placement
        self.top_bar.grid(row=0, column=0, sticky="new")
        self.bottom_bar.grid(row=10, column=0, sticky="sew")
        self.exit_b.grid(row=0, column=3, padx=0, sticky="e")
        self.user_b.grid(row=0, column=0, padx=0, sticky='w')
        self.settings_b.grid(row=0, column=1, padx=0, sticky="w")
        self.about_b.grid(row=0, column=2, padx=0, sticky="w")
        self.version.grid(row=0, column=1, padx=7, pady=2, sticky="es")
        self.warning.grid(row=0, column=0, padx=10, pady=0, sticky="sw")

        # Grid config
        self.rowconfigure(2, weight=1)
        self.columnconfigure("all", weight=1)
        self.top_bar.columnconfigure(3, weight=1)
        self.bottom_bar.columnconfigure(1, weight=1)

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
        self.geometry("400x600")
        self.title("Login")

        # Widgets
        self.label = ui.CTkLabel(self, text="Please log in", font=app.hi_font)
        self.entries_frame = ui.CTkFrame(self, corner_radius=0)
        self.username = ui.CTkEntry(self.entries_frame, placeholder_text="Username", corner_radius=2, border_width=0)
        self.password = ui.CTkEntry(self.entries_frame, placeholder_text="Password", corner_radius=2, border_width=0)

        # Widgets placement
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.entries_frame.grid(row=1, column=0, padx=0, pady=0, sticky="new")
        self.username.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="new")
        self.password.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="new")

        # Grid configure
        self.columnconfigure(0, weight=1)
        self.entries_frame.columnconfigure(0, weight=1)


if __name__ == "__main__":
    logg = log.Log()
    dbb = db.Database("users")
    app = MainWindow()
    if app.account_username == "No login":
        login_window = LoginWindow()
    app.mainloop()
