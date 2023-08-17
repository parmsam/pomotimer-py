from shiny import *
import time
import sys
from pathlib import Path
from typing import List
from shiny.types import NavSetArg
# import htmltools

# Helper functions
def min_to_sec(minutes):
    return minutes * 60

def get_current_date():
    curr_date = time.strftime("%a - %b %d, %Y", time.localtime())
    return curr_date

def fmt_seconds(time_in_seconds):
    return time.strftime("%H:%M:%S", time.gmtime(time_in_seconds))


# Declare paths to static assets
css_file = Path(__file__).parent / "www" / "styles.css"
js_file = Path(__file__).parent / "www" / "script.js"

long_break_image = "https://thumbs.gfycat.com/BriskLankyCopperhead-size_restricted.gif"
pomo_image = "https://cdn.dribbble.com/users/1341046/screenshots/3993533/media/d5d7198e3cd99068106a19679b4d7ee5.gif"
short_break_image = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExemt1NmJnZGRsNGRvYmY5NThld2N1dzJpYWdudGQwazFzN2UxdTR6NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MfeD9WGuYxVUk/giphy.gif"

app_link = "https://github.com/parmsam/pomotimer-py",

mp3_link = "https://github.com/JanLoebel/MMM-TouchAlarm/blob/master/sounds/alarm.mp3?raw=true"

# Declare navbar for app
def nav_controls(prefix: str) -> List[NavSetArg]:
    return [
        ui.nav("timer",
               ui.div(
                   ui.input_action_button("pomo", "pomo", class_="btn-red"),
                   ui.input_action_button(
                       "short_break", "short break", class_="btn-purple"),
                   ui.input_action_button(
                       "long_break", "long break", class_="btn-blue"),
                   class_="time-btns",
               ),
               ui.h6(ui.output_text("current_date")),
               ui.h2(ui.output_text("time_left")),
               ui.br(),
               ui.div(
                   ui.input_action_button(
                       "start", "start/stop", class_="btn-primary"),
                   ui.input_action_button(
                       "reset", "reset", class_="btn-warning"),
                   class_="main-btns",
               ),
               ui.br(),
        ),
        ui.nav("settings",
               ui.div(
                   ui.input_checkbox("include_images", "include gifs", value=False),
                   ui.input_numeric(
                        "pomo_length", "pomo (min)", 
                        value=25,
                        width='45%'),
                   ui.input_numeric(
                        "short_break_length",
                        "short break (min)", 
                        value=5,
                        width='45%'),
                   ui.input_numeric(
                       "long_break_length", 
                       "long break (min)", 
                       value=10,
                       width='45%'),
                   class_="settings",
               ),
        ),
        ui.nav_control(
            ui.a(
                "github",
                href= str(app_link),
                target="_blank",
            ),
        ),
    ]

# Define the app 
app_ui = ui.page_fluid(
    ui.include_js(str(js_file)),
    ui.include_css(str(css_file)),
    ui.h1("pomotimer-py 🍅", class_ = "main_title"),
    ui.navset_pill_card(*nav_controls("_")),
)

def server(input, output, session):
    # Update the current time every second
    curr_time = reactive.Value(time.time())
    timer_active = reactive.Value(False)
    remaining_time = reactive.Value(-1)

    # Track the remaining pomo minutes 
    @reactive.Effect
    def _():
        reactive.invalidate_later(1)
        if (timer_active.get() == True):
            curr_time.set(time.time())
            with reactive.isolate():
                remaining_time.set(remaining_time.get() - 1)
                if(remaining_time.get() == 0):
                    timer_active.set(False)
                    m = ui.modal(
                        "Time is up.",
                        title="Nicely done!",
                        easy_close=True,
                        footer="Pomotimer-py",
                    )
                    ui.modal_show(m)  

    @reactive.Effect
    @reactive.event(input.pomo)
    def set_pomo_reg():
        remaining_time.set(input.pomo_length()*60)
        if(input.include_images()):
            ui.remove_ui(selector="div.running_img")
            ui.insert_ui(
                ui.div(
                    ui.br(),
                    ui.img(src = pomo_image),
                    class_="running_img",
                ),
                selector="#reset",
                where="afterEnd",
            )

    @reactive.Effect
    @reactive.event(input.short_break)
    def set_pomo_short():
        remaining_time.set(int(input.short_break_length()*60))
        if(input.include_images()):
            ui.remove_ui(selector="div.running_img")
            ui.insert_ui(
                ui.div(
                    ui.br(),
                    ui.img(src=short_break_image),
                    class_="running_img",
                ),
                selector="#reset",
                where="afterEnd",
            )

    @reactive.Effect
    @reactive.event(input.long_break)
    def set_pomo_long():
        remaining_time.set(input.long_break_length()*60)
        if(input.include_images()):
            ui.remove_ui(selector="div.running_img")
            ui.insert_ui(
                ui.div(
                    ui.br(),
                    ui.img(src=long_break_image),
                    class_="running_img",
                ),
                selector="#reset",
                where="afterEnd",
            )

    # Reset the timer
    @reactive.Effect
    @reactive.event(input.reset)
    def reset_stop_time():
        remaining_time.set(0)
        ui.remove_ui(selector="div.running_img")

    # Start/stop the timer
    @reactive.Effect
    @reactive.event(input.start)
    def stop_timer():
        timer_active.set(
            not (timer_active.get())
        )

    # Update the time left
    @output
    @render.text
    def time_left():
        if (remaining_time.get() == 0):
            remaining_time.set(0)
            return "Select a timer"
        print(remaining_time.get())
        if (remaining_time.get()) > 0:
            return fmt_seconds(remaining_time.get())
        remaining_time.set(0)

        return "Time's up!"
    
    # Update the current date
    @output
    @render.text
    def current_date():
        return get_current_date()


app = App(app_ui, server, debug=False)
