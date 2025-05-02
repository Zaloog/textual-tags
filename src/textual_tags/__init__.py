from __future__ import annotations
from typing import Iterable

from textual.binding import Binding
from textual.reactive import reactive
from textual.app import RenderResult
from textual.events import Key
from textual.message import Message
from textual.widgets import Input, Label
from textual_autocomplete import (
    AutoComplete,
    DropdownItem,
    TargetState,
    AutoCompleteList,
)

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
        margin:0;
        padding:0;
        height: auto;
        width: auto;
        min-width:20;
        border:none;

        & > :focus {
            border:none;
        }
    }
    """

    def on_focus(self):
        self.parent.query_one(TagAutoComplete).action_show()

    async def on_key(self, event: Key):
        if event.key == "backspace":
            if not self.value:
                await self.parent.reset_last_tag()


class Tag(Label):
    DEFAULT_CSS = """
    Tag {
        margin:0 1 0 0 ;
        color:$primary-lighten-2;
        background:$panel;

        &:hover {
            background:$primary-darken-2;
            tint: 10%;
        }
        &:focus {
            background:$primary-darken-2;
            tint: 10%;
        }

    }
    """
    RIGHT_END = "\ue0b4"
    LEFT_END = "\ue0b6"

    show_x: reactive[bool] = reactive(False)
    can_focus = True

    class Removed(Message):
        def __init__(self, tag: Tag) -> None:
            self.tag = tag
            super().__init__()

        @property
        def control(self):
            return self.tag

    class Focused(Message):
        def __init__(self, tag: Tag) -> None:
            self.tag = tag
            super().__init__()

        @property
        def control(self):
            return self.tag

    class Hovered(Message):
        def __init__(self, tag: Tag) -> None:
            self.tag = tag
            super().__init__()

        @property
        def control(self):
            return self.tag

    def render(self) -> RenderResult:
        background = self.styles.background.hex
        parent_background = self.colors[0].hex
        # Add extra padding with single space if self.show_x == False
        # To prevent layout change if its toggled
        left_round_part = f"[{background} on {parent_background}]{self.LEFT_END}[/]"
        right_round_part = f"[{background} on {parent_background}]{self.RIGHT_END}[/]"
        label_part = f"{self.value}" if self.show_x else f" {self.value}"
        x_part = " x" if self.show_x else " "
        return left_round_part + label_part + x_part + right_round_part

    def on_click(self):
        self.remove()

    def on_key(self, event: Key):
        if event.key == "enter":
            self.remove()
            event.prevent_default()
            event.stop()

    def watch_show_x(self):
        self.render()

    def on_prune(self):
        self.post_message(self.Removed(self))

    def on_focus(self):
        self.post_message(self.Focused(self))

    def on_enter(self):
        self.post_message(self.Hovered(self))

    @property
    def value(self):
        return self.renderable


class Tags(FlexBoxContainer):
    DEFAULT_CSS = """
    Tags {
        padding:0 0 0 1 ;
        height:auto;
        min-height:3;
    }
    """

    BINDINGS = [
        Binding("ctrl+j", "next_hightlight", priority=True),
        Binding("ctrl+k", "previous_hightlight", priority=True),
        Binding("ctrl+o", "clear_tags", priority=True),
    ]

    tag_values: reactive[set[str]] = reactive(set())
    show_x: reactive[bool] = reactive(False)
    allow_new_tags: reactive[bool] = reactive(False)
    selected_tags: reactive[set[str]] = reactive(set())

    def __init__(
        self,
        tag_values: list | set,
        show_x: bool = False,
        start_with_tags_selected: bool = True,
        allow_new_tags: bool = False,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """A tags widget to select/unselect predefined Tags or add new ones.

        Args:
            tag_values: The available tags for this widget, will be turned into a set internally, if a list is provided
            show_x: Puts a `X` behind the actual tag-label (default=False)
            start_with_tags_selected: All Tags will be selected on initialisation (default=True)
            allow_new_tags: Allow adding any value as tag, not just predefined ones (default=False)
            id: The DOM node id of the widget.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled.
        """
        # Use a set to remove duplicate tags
        if isinstance(tag_values, list):
            tag_values_set = set(tag_values)

        super().__init__(id=id, classes=classes, disabled=disabled)
        self.tag_values = tag_values_set
        self.show_x = show_x
        self.allow_new_tags = allow_new_tags
        self.start_with_tags_selected = start_with_tags_selected

    async def on_mount(self):
        self.query_one(TagInput).placeholder = "Enter a tag..."
        if self.start_with_tags_selected:
            await self._populate_with_tags()

    def compose(self):
        tag_input = TagInput(id="input_tag")
        yield tag_input

        yield TagAutoComplete(
            target=tag_input,
            candidates=self.update_autocomplete_candidates,
        )

    def _on_tag_removed(self, event: Tag.Removed):
        self.selected_tags.remove(event.tag.value)
        self.mutate_reactive(Tags.selected_tags)

    def update_autocomplete_candidates(self, state: TargetState) -> list[DropdownItem]:
        return [DropdownItem(unselected_tag) for unselected_tag in self.unselected_tags]

    async def _on_tag_auto_complete_applied(self, event: TagAutoComplete.Applied):
        await event.autocomplete.target.action_submit()

    async def on_input_submitted(self, event: Input.Submitted):
        value = event.input.value.strip()
        # Prevent empty Tags
        if not value:
            return
        # Prevent non pre-defined entries if not allowed
        if (value not in self.tag_values) and (not self.allow_new_tags):
            # self.notify(
            #     title='Invalid Tag',
            #     message='Adding new tags is not allowed',
            #     severity='warning',
            #     timeout=2
            # )
            return

        # Prevent already selected tags
        if value in self.selected_tags:
            # self.notify(
            #     title='Invalid Tag',
            #     message='Tag already present',
            #     severity='warning',
            #     timeout=2
            # )
            return

        await self.add_new_tag(value=value)
        self.query_one(Input).clear()

    async def _populate_with_tags(self):
        for tag in self.tag_values:
            if tag not in self.selected_tags:
                await self.add_new_tag(value=tag)

    async def add_new_tag(self, value: str):
        """Adds a new Tag and updates self.tag_values if tag is not present"""
        await self.mount(Tag(value).data_bind(Tags.show_x), before="#input_tag")
        self.selected_tags.add(value)

        if value not in self.tag_values:
            self.tag_values.add(value)

        self.mutate_reactive(Tags.tag_values)
        self.mutate_reactive(Tags.selected_tags)

    async def action_clear_tags(self):
        await self.unselect_all_tags()
        self._put_focus_back_on_input()

    async def unselect_all_tags(self):
        """Removes all Tags"""
        await self.query(Tag).remove()

    def _put_focus_back_on_input(self):
        """Focus back on input after tag clear"""
        self.query_one(TagInput).cursor_position = 0
        self.query_one(TagInput).focus()

    def add_tag_values(self, new_values: str | Iterable[str]):
        """Add new tags to self.tag_values which holds all available Tags for this widget"""
        if isinstance(new_values, str):
            self.tag_values.add(new_values)
        else:
            self.tag_values.update(new_values)
        self.mutate_reactive(Tags.tag_values)

    async def reset_last_tag(self):
        if not self.allow_new_tags:
            return
        last_tag = self.query(Tag).last()
        self.tag_values.remove(last_tag.value)
        await last_tag.remove()
        self.query_one(TagInput).value = last_tag.value
        self.query_one(TagInput).cursor_position = len(last_tag.value)

    def action_next_hightlight(self):
        """go to next hightlight in completion option list"""
        option_list = self.query_one(TagAutoComplete).option_list
        displayed = self.query_one(TagAutoComplete).display
        highlighted = option_list.highlighted

        if displayed:
            highlighted = (highlighted + 1) % option_list.option_count
        else:
            self.query_one(TagAutoComplete).display = True
            highlighted = 0

        option_list.highlighted = highlighted

    def action_previous_hightlight(self):
        """go to previous hightlight in completion option list"""
        option_list = self.query_one(AutoCompleteList)
        displayed = self.query_one(TagAutoComplete).display
        highlighted = option_list.highlighted

        if displayed:
            highlighted = (highlighted - 1) % option_list.option_count
        else:
            self.query_one(TagAutoComplete).display = True
            highlighted = 0

        option_list.highlighted = highlighted

    async def watch_selected_tags(self):
        """hide input if all tags are selected and no new tags are allowed"""
        if self.allow_new_tags:
            return
        if not self.unselected_tags:
            self.query_one(TagInput).styles.display = "none"
        else:
            self.query_one(TagInput).styles.display = "block"

    async def watch_allow_new_tags(self):
        if self.allow_new_tags:
            self.query_one(TagInput).styles.display = "block"
        else:
            await self.watch_selected_tags()

    async def watch_tag_values(self):
        await self.watch_allow_new_tags()

    @property
    def unselected_tags(self) -> set[str]:
        return self.tag_values.difference(self.selected_tags)
