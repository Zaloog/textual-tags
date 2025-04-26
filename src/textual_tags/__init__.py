from textual.reactive import reactive
from textual.app import RenderResult
from textual.events import Key
from textual.message import Message
from textual.widgets import Input, Label

from textual_tags.flexbox import FlexBoxContainer


class TagInput(Input):
    DEFAULT_CSS = """
    TagInput {
    }
    """


class Tag(Label):
    DEFAULT_CSS = """
    Tag {
        background:$success;

        &:hover {
            background:$primary-darken-2;
            tint: 20%;
        }
        &:focus {
            background:$primary-darken-2;
            tint: 20%;
        }
    }
    """
    RIGHT_END = "\ue0b6"
    LEFT_END = "\ue0b4"

    can_focus = True

    class Removed(Message):
        def __init__(self, tag) -> None:
            self.tag = tag
            super().__init__()

        @property
        def control(self):
            return self.tag

    def render(self) -> RenderResult:
        background = self.styles.background.hex
        parent_background = self.colors[0].hex
        return (
            f"[{background} on {parent_background}]{self.RIGHT_END}[/]"
            + str(self.renderable)
            + f"[{background} on {parent_background}]{self.LEFT_END}[/]"
        )

    def on_click(self):
        self.post_message(self.Removed(self))

    def on_key(self, event: Key):
        if event.key == "enter":
            self.post_message(self.Removed(self))


class Tags(FlexBoxContainer):
    DEFAULT_CSS = """
    Tags {
    }
    """
    tag_list: reactive[list[str]] = reactive([])

    def __init__(self, tag_list: list = []) -> None:
        super().__init__()

    def on_mount(self):
        self.query_one(TagInput).placeholder = "Enter a tag:"

    def compose(self):
        TAG_ENTRIES = ["Textual", "is", "awesome", "Cool"]
        for entry in TAG_ENTRIES:
            yield Tag(entry)
        yield TagInput(id="input_tag")

    def on_tag_removed(self, event: Tag.Removed):
        self.notify(event.tag.renderable)
        event.tag.remove()

    def on_input_submitted(self, event: Input.Submitted):
        value = event.input.value
        if value:
            self.mount(Tag(value), before="#input_tag")
            self.query_one(Input).clear()
