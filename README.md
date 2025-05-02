<!-- Icons -->
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI-Server](https://img.shields.io/pypi/v/textual-tags.svg)](https://pypi.org/project/textual-tags/)
[![Pyversions](https://img.shields.io/pypi/pyversions/textual-tags.svg)](https://pypi.python.org/pypi/textual-tags)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/textual-tags)](https://pepy.tech/project/textual-tags)
[![Coverage Status](https://coveralls.io/repos/github/Zaloog/textual-tags/badge.svg?branch=main)](https://coveralls.io/github/Zaloog/textual-tags?branch=main)

# textual-tags

![demo_image](https://raw.githubusercontent.com/Zaloog/textual-tags/main/images/textual_tags_image.png)

This library provides a custom tags widget called `Tags`,
which can be easily added into your existing [textual] application.

Requires a Nerdfont to render the round corners of the Tag labels.

## Features
- Can be initiated with a predefined set/list of tags, similar entries will be ignored
- Consists of a TagInput, with autocompletion powered by [textual-autocomplete] for existing tags
and displayed tags wrapped in a flexbox-like container
- Two different ways to display the tags (with `x` at the end or without)
- Option to also add new not predefined tags, which are then also available for autocompletion
- vim-like completion control

## Installation
textual-tags is hosted on [PyPi] and can be installed with:

```bash
pip install textual-tags
```

or add it to your project using [uv] with:

```bash
uv add textual-tags
```
## Demo App
You can run the demo app after installation with `textual-tags` or using [uv] with:

```bash
uvx textual-tags
```

## Usage
Here is an exampke usage of the `Tags`-widget in a textual App. You can also check the demo app
[here](https://github.com/Zaloog/textual-tags/blob/main/src/textual_tags/demo.py).

```python
from textual.app import App

from textual_tags import Tags

PRE_DEFINED_TAGS = [
    "uv",
    "Terminal",
    "tcss",
    "Textual",
    "Tags",
    "Widget",
    "Python",
    "TUI",
    "Highlander"
]

class TagsApp(App):
    DEFAULT_CSS = """
    Tags {
        width:50;
    }
    """
    def compose(self):
        yield Tags(
            # list/set of tags to start with
            tag_values=PRE_DEFINED_TAGS,
            # Show Tag-Labels as `TAG x` instead of ' TAG '
            show_x=False,
            # All tags are selected on startup
            start_with_tags_selected=True,
            # Allow to enter custom new tags and dont hide TagInput if all tags are selected
            # Also allows delete/edit of last tag when pressing `backspace` on empty input
            allow_new_tags=False,
        )

def main():
    app = TagsApp()
    app.run()

if __name__ == '__main__':
    main()
```

## Messages
Tags sends two messages:
- `Tag.Removed`, send when a tag is removed in any way
- `Tag.Focused`, send when a tag is focused
- `Tag.Hovered`, send when a tag is hovered
- `TagAutoComplete.Applied`, send when a completion option is applied

## Issues/Feedback
Feel free to reach out and share your feedback, or open an [Issue],
if something doesnt work as expected. Also check the [Changelog] for new updates.

<!-- Repo Links -->
[Changelog]: https://github.com/Zaloog/textual-tags/blob/main/CHANGELOG.md
[Issue]: https://github.com/Zaloog/textual-tags/issues


<!-- external Links Python -->
[textual]: https://textual.textualize.io
[pipx]: https://github.com/pypa/pipx
[PyPi]: https://pypi.org/project/textual-tags/
[textual-autocomplete]: https://github.com/darrenburns/textual-autocomplete

<!-- external Links Others -->
[uv]: https://docs.astral.sh/uv
