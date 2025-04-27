from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input
from textual_tags import Tags

DEMO_TAGS = ["tag1", "tag2", "tag3", "tag4"]


class DemoApp(App):
    CSS_PATH = "assets/demo.tcss"

    def compose(self) -> ComposeResult:
        yield Tags(tag_values=DEMO_TAGS)
        yield Input(placeholder="Add more tags to widget", id="input_adder")

        return super().compose()

    @on(Input.Submitted, "#input_adder")
    def add_new_tag_to_widget(self, event: Input.Submitted):
        self.query_one(Tags).tag_values.add(event.input.value)
        event.input.clear()


def run_demo():
    app = DemoApp()
    app.run()
