from __future__ import annotations

from textual.reactive import reactive
from textual.app import RenderResult
from textual.events import Key
from textual.message import Message
from textual.widgets import Input, Label
from textual_autocomplete import AutoComplete, DropdownItem, TargetState

from textual_tags.flexbox import FlexBoxContainer


class TagAutoComplete(AutoComplete):
    class Applied(Message):
        def __init__(self, autocomplete: TagAutoComplete) -> None:
            self.autocomplete = autocomplete
            super().__init__()

        @property
        def control(self):
            return self.autocomplete

    def post_completion(self):
        self.action_hide()
        self.post_message(self.Applied(autocomplete=self))


class TagInput(Input):
    DEFAULT_CSS = """
    TagInput {
    }
    """

    def on_focus(self):
        self.parent.query_one(TagAutoComplete).action_show()


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
        def __init__(self, tag: Tag) -> None:
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
    tag_values: reactive[set[str]] = reactive(set())

    def __init__(
        self, tag_values: list | set | None = None, allow_all: bool = False
    ) -> None:
        """An autocomplete widget for filesystem paths.

        Args:
            tag_values: The target input widget to autocomplete.
            allow_all: Allow adding any value as tag, not just predefined ones (default=False)
            id: The DOM node id of the widget.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled.
        """
        if isinstance(tag_values, list):
            tag_values_set = set(tag_values)

        super().__init__()
        self.tag_values = tag_values_set

    def on_mount(self):
        self.query_one(TagInput).placeholder = "Enter a tag..."

    def compose(self):
        tag_input = TagInput(id="input_tag")
        yield tag_input

        yield TagAutoComplete(
            target=tag_input, candidates=self.update_autocomplete_candidates
        )

    async def _on_tag_removed(self, event: Tag.Removed):
        await event.tag.remove()

    def update_autocomplete_candidates(self, state: TargetState) -> list[DropdownItem]:
        return [DropdownItem(unselected_tag) for unselected_tag in self.unselected_tags]

    async def _on_tag_auto_complete_applied(self, event: TagAutoComplete.Applied):
        await event.autocomplete.target.action_submit()

    def on_input_submitted(self, event: Input.Submitted):
        value = event.input.value
        if value in self.tag_values:
            self.mount(Tag(value), before="#input_tag")
            self.query_one(Input).clear()

    def clear_tags(self):
        self.query(Tag).remove()

    @property
    def selected_tags(self) -> set[str]:
        return {tag.renderable for tag in self.query(Tag)}

    @property
    def unselected_tags(self) -> set[str]:
        return self.tag_values.difference(self.selected_tags)
