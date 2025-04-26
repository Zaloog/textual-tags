from textual.app import App, ComposeResult
from textual_tags import Tags

DEMO_TAGS = ["tag1", "tag2", "tag3"]


class DemoApp(App):
    CSS_PATH = "assets/demo.tcss"

    def compose(self) -> ComposeResult:
        yield Tags()
        return super().compose()


def run_demo():
    app = DemoApp()
    app.run(inline=True)
