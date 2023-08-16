from shiny import *
import time
import sys
from pathlib import Path

# Helper functions
def min_to_sec(minutes):
    return minutes * 60

def get_current_date():
    curr_date = time.strftime("%a - %b %d, %Y", time.localtime())
    # replace comma with a dash
    return curr_date

def fmt_seconds(time_in_seconds):
    return time.strftime("%H:%M:%S", time.gmtime(time_in_seconds))


# Declare paths to static assets
css_file = Path(__file__).parent / "www" / "styles.css"

# Define the app 
app_ui = ui.page_fluid(
    ui.include_css(css_file),
    ui.h1("Pomotimer-py 🍅", class_ = "main_title"),
    ui.br(),
    ui.div(
        ui.input_action_button("pomo", "Pomo", class_="btn-red"),
        ui.input_action_button(
            "short_break", "Short Break", class_="btn-purple"),
        ui.input_action_button("long_break", "Long Break", class_="btn-blue"),
        class_ = "time-btns",
    ),
    ui.h6(ui.output_text("current_date")),
    ui.h2(ui.output_text("time_left")),
    ui.br(),
    ui.div(
        ui.input_action_button("start", "Start/Stop", class_="btn-primary"),
        ui.input_action_button(
            "reset", "Reset", class_="btn-warning"),
        class_ = "main-btns",
    ),
    ui.br(),
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
        remaining_time.set(25*60)

    @reactive.Effect
    @reactive.event(input.short_break)
    def set_pomo_short():
        remaining_time.set(int(5*60))

    @reactive.Effect
    @reactive.event(input.long_break)
    def set_pomo_long():
        remaining_time.set(10*60)

    # Reset the timer
    @reactive.Effect
    @reactive.event(input.reset)
    def reset_stop_time():
        remaining_time.set(0)

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

