from textual.app import ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.widgets import TextArea, Markdown, MarkdownViewer


class NoteWidget(HorizontalScroll):

    BORDER_TITLE = 'Note'

    def compose(self) -> ComposeResult:
        yield VerticalScroll(TextArea())
        yield VerticalScroll(MarkdownViewer(show_table_of_contents=False))
    
    def on_text_area_changed(self, message: TextArea.Changed) -> None:
        self.query_one(Markdown).update(message.text_area.text)