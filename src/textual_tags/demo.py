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
        switch_x = Switch(id="switch_x", classes="switch-toggles")
        switch_x.border_title = "Show X at end of each tag"
        switch_new = Switch(id="switch_new", classes="switch-toggles")
        switch_new.border_title = "Allow New Tags"
        yield input
        yield switch_x
        yield switch_new

        return super().compose()

    @on(Input.Submitted, "#input_adder")
    def add_new_tag_to_widget(self, event: Input.Submitted):
        self.query_one(Tags).tag_values.add(event.input.value)
        event.input.clear()

    @on(Switch.Changed, "#switch_x")
    def update_show_x(self, event: Switch.Changed):
        self.query_one(Tags).show_x = event.switch.value

    @on(Switch.Changed, "#switch_new")
    def update_allow_new_tags(self, event: Switch.Changed):
        self.query_one(Tags).allow_new_tags = event.switch.value


def run_demo():
    app = DemoApp()
    app.run()
