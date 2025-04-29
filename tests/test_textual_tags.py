from textual.app import App


async def test_tag_values(test_app: App):
    async with test_app.run_test() as pilot:
        assert len(pilot.app.tags_widget.tag_values) == 3
