"""Thanks DK: Source, https://gist.github.com/ddkasa/0a60dcb1bd13e67bc79cc6f3b144aa8d"""

from __future__ import annotations

from operator import itemgetter
from typing import TYPE_CHECKING

from textual.box_model import BoxModel
from textual.css.styles import RenderStyles
from textual._resolve import resolve_box_models
from textual.geometry import (
    NULL_OFFSET,
    NULL_SIZE,
    Region,
    Size,
    Spacing,
)
from textual.layout import Layout, WidgetPlacement
from textual.widget import Widget

from math import floor

if TYPE_CHECKING:
    from textual.layout import ArrangeResult


class FlexBoxLayout(Layout):
    name = "flexbox"

    def arrange(
        self,
        parent: Widget,
        children: list[Widget],
        size: Size,
    ) -> ArrangeResult:
        """Generate a layout map that defines where the widgets will be drawn.
        Args:
            parent: Parent widget.
            children: A list of widgets to be placed.
            size: Size of container.
        Returns:
            An iterable of widget locations.
        """
        parent.pre_layout(self)
        viewport = parent.app.size

        styles = [child.styles for child in children]
        placements = [
            (
                style.get_rule("position") == "absolute",
                style.overlay == "screen",
            )
            for style in styles
        ]
        margins: list[Spacing] = [
            style.margin for style, (overlay, _) in zip(styles, placements) if overlay
        ]

        NewSize = Size
        if margins:
            resolve_margin = NewSize(
                sum(
                    [
                        max(margin1[1], margin2[3])
                        for margin1, margin2 in zip(margins, margins[1:])
                    ]
                )
                + (margins[0].left + margins[-1].right),
                max(
                    [
                        margin_top + margin_bottom
                        for margin_top, _, margin_bottom, _ in margins
                    ]
                ),
            )
        else:
            resolve_margin = NULL_SIZE

        regions = self._resolve_regions(
            parent,
            children,
            viewport,
            size,
            resolve_margin,
            placements,
            styles,
        )

        NewPlacement = WidgetPlacement

        return [
            NewPlacement(
                region=region,
                offset=style.offset.resolve(
                    NewSize(region.width, region.height),
                    viewport,
                )
                if style.has_rule("offset")
                else NULL_OFFSET,
                margin=box_model.margin,
                widget=widget,
                order=i,
                overlay=is_overlay,
                absolute=is_abs,
            )
            for i, (
                widget,
                (region, box_model),
                (is_abs, is_overlay),
                style,
            ) in enumerate(zip(children, regions, placements, styles, strict=False))
        ]

    def _resolve_regions(
        self,
        parent: Widget,
        children: list[Widget],
        viewport: Size,
        size: Size,
        margin: Size,
        placements: list[tuple[bool, bool]],
        styles: list[RenderStyles],
    ) -> list[tuple[Region, BoxModel]]:
        """Generate regions balanced rows from provided widgets.
        Args:
            parent: The parent container widget primarily for styles.
            children: Widgets to be layed out.
            viewport: Size of the of parent viewport.
            size: Given size of the container.
            margin: Initial size of margin for resolving box models.
            placements: Booleans for screening and absolute placement setting.
            styles: Styles of children expanded out beforehand.
        Returns:
            Tuples of regions and box models ready to be placed.
        """
        margin_width, margin_height = margin
        pwidth, pheight = viewport - margin
        sizes = [(style.width, style.height) for style in styles]

        parent_width = size.width

        resolved = resolve_box_models(
            list(map(itemgetter(0), sizes)),
            children,
            size,
            viewport,
            margin,
            resolve_dimension="width",
        )

        row_sizes: list[tuple[int | None, int, int, int]] = []
        """Tuples of row indexes. 1. Index 2. row_width 3. row-y-pos, 4. row_height"""
        add_row = row_sizes.append
        row_width, row_pos, max_height = 0, 0, 0
        for i, (
            widget,
            (width, height, box_margin),
            (is_abs, is_overlay),
        ) in enumerate(zip(children, resolved, placements, strict=True)):
            if is_abs or is_overlay:
                continue
            box_width = floor(width + box_margin.width)
            next_width = floor(row_width + box_width)
            if next_width > parent_width:
                add_row((i, row_width, row_pos, max_height))
                next_width = box_width
                row_pos += max_height
                max_height = 0
            next_height = floor(height + box_margin.height)
            max_height = max_height if max_height >= next_height else next_height
            row_width = next_width

        add_row((None, row_width, row_pos, max_height))
        halign, valign = parent.styles.align
        center_aligned = halign == "center"
        right_aligned = halign == "right"
        NewRegion = Region
        box_models: list[Region] = []
        add_region = box_models.append
        prev_index = None
        for i in range(len(row_sizes)):
            index, row_width, row_pos, max_height = row_sizes[i]
            if center_aligned:
                x = floor((parent_width - row_width) / 2)
            elif right_aligned:
                x = floor(parent_width - row_width)
            else:
                x = 0

            for widget, (width, height, box_margin), (is_abs, is_overlay) in zip(
                children[prev_index:index],
                resolved[prev_index:index],
                placements[prev_index:index],
                strict=True,
            ):
                add_region(
                    NewRegion(
                        x + box_margin.left,
                        row_pos + box_margin.top,
                        width := floor(width),
                        floor(height),
                    )
                )
                if not is_abs and not is_overlay:
                    x += width + box_margin.width

            prev_index = index

        return list(zip(box_models, resolved))


class FlexBoxContainer(Widget):
    """Container widget with predefined flexbox layout."""

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )

        self._layout = FlexBoxLayout()

    @property
    def layout(self) -> FlexBoxLayout:
        return self._layout
