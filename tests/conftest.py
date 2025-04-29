import pytest
from textual.app import App

from textual_tags import Tags

TEST_TAGS = ["Tag1", "Tag2", "Tag3"]


class TestApp(App):
    def compose(self):
        self.tags_widget = Tags(tag_values=TEST_TAGS)
        yield self.tags_widget


@pytest.fixture
def test_app():
    return TestApp()
