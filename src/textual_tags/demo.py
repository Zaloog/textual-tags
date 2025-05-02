from textual import on
from textual.app import App, ComposeResult
from textual.content import Content
from textual.widgets import Input, Switch, Label, Rule, Button
from textual_tags import Tags, Tag

DEMO_TAGS = [
    "uv",
    "Terminal",
    "tcss",
    "Textual",
    "Tags",
    "Widget",
    "Python",
    "TUI",
    "Highlander",
]


class DemoApp(App):
    CSS_PATH = "assets/demo.tcss"

    def compose(self) -> ComposeResult:
        yield Tags(
            tag_values=DEMO_TAGS,
            show_x=False,
            start_with_tags_selected=True,
            allow_new_tags=False,
        )
        input = Input(
            placeholder="Add more tags to internal widget list",
            id="input_adder",
            classes="demo-widgets",
        )
        input.border_title = "Add more Tags here"
        switch_x = Switch(id="switch_x", classes="demo-widgets")
        switch_x.border_title = "Show X at end of each tag [$warning](default=False)[/]"
        switch_new = Switch(id="switch_new", classes="demo-widgets")
        switch_new.border_title = "Allow New Tags [$warning](default=False)[/]"
        button_all = Button("Mount All", id="button_all", variant="success")

        yield Rule(classes="description")
        yield Label(
            Content.from_markup(
                "You can display and navigate completion options with [$success]ctrl+j/k[/] or [$success]up/down[/]"
            ),
            classes="description",
        )

        yield Rule(classes="description")
        yield Label(
            Content.from_markup(
                "Click or press enter while a tag is focused to unselect Tag, [$success]ctrl+o[/] on the tags widget unselects all"
            ),
            classes="description",
        )
        yield Rule(classes="description")
        yield input
        yield switch_x
        yield switch_new
        yield button_all

        return super().compose()

    @on(Input.Submitted, "#input_adder")
    def add_new_tag_to_widget(self, event: Input.Submitted):
        self.query_one(Tags).add_tag_values(event.input.value)
        event.input.clear()

    def on_switch_changed(self, event: Switch.Changed):
        match event.switch.id:
            case "switch_x":
                self.query_one(Tags).show_x = event.switch.value
            case "switch_new":
                self.query_one(Tags).allow_new_tags = event.switch.value

    def on_button_pressed(self, event: Button.Pressed):
        self.notify("All Tags mounted")
        tags = self.query_one(Tags)
        tags.call_later(tags._populate_with_tags)

    def on_tag_focused(self, event: Tag.Focused):
        self.notify(f"Tag {event.tag.value} focused", timeout=1)

    def on_tag_hovered(self, event: Tag.Hovered):
        self.notify(f"Tag {event.tag.value} hovered", timeout=1)


def run_demo():
    app = DemoApp()
    app.run()
