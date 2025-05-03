# Changelog

## v0.3.0
- Make the x-part clickable and distinguishable to unselect tags.
Also backspace now unselects the focused tags. Enter and normal clicking will send
the `Tag.Selected` Event instead

## v0.2.1
- Fix error when trying to use ctrl+j/k on `Tag` when autocomplete menu was not displayed

## v0.2.0
- Fix the _populate_with_tags function
- Add `Tag.Focused` and `Tag.Hovered` messages that fire, if a `Tag` is hovered or focused

## v0.1.2
- fix duplication in Tags docstring

## v0.1.1
- fix bug, that already present tags can be added when `allow_new_tags=True`

## v0.1.0
- initial release
