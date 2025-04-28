from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Switch
from textual_tags import Tags

DEMO_TAGS = ["UV", "Terminal", "TCSS", "Textual", "Tags", "Widget", "Python"]


class DemoApp(App):
    CSS_PATH = "assets/demo.tcss"

    def compose(self) -> ComposeResult:
        yield Tags(tag_values=DEMO_TAGS)
        input = Input(
            placeholder="Add more tags to internal widget list", id="input_adder"
        )
        input.border_title = "Add more Tags here"
        switch = Switch(id="switch_x")
        switch.border_title = "Show X at end of each tag"
        yield input
        yield switch

        return super().compose()

    @on(Input.Submitted, "#input_adder")
    def add_new_tag_to_widget(self, event: Input.Submitted):
        self.query_one(Tags).tag_values.add(event.input.value)
        event.input.clear()

    def on_switch_changed(self, event: Switch.Changed):
        self.query_one(Tags).show_x = event.switch.value


def run_demo():
    app = DemoApp()
    app.run()
