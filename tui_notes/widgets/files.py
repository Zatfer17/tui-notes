from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DirectoryTree, TextArea
from widgets.note import NoteWidget


class FilesWidget(VerticalScroll):

    BORDER_TITLE = 'Files'

    def compose(self) -> ComposeResult:
        yield DirectoryTree('./notes/')

    def on_directory_tree_file_selected(self, message: DirectoryTree.FileSelected):
        if str(message.path).endswith('.md'):
            with open(message.path) as f:
                self.app.query_one(NoteWidget).note_path = str(message.path)
                self.app.query_one(TextArea).load_text(f.read())