from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll
from textual.widgets import Footer, TextArea
from tui_notes.widgets.files import FilesWidget
from tui_notes.widgets.note import NoteWidget
from tui_notes.widgets.assistant import AssistantWidget


class NotesApp(App):

    BORDER_TITLE = 'Notes app'
    CSS_PATH = "static/style.tcss"
    BINDINGS = {
        ("ctrl+shift+s", "save_note", "Save note"),
        ("ctrl+shift+w", "close_note", "Close note"),
    }

    def compose(self) -> ComposeResult:
        with HorizontalScroll(id='main_view'):
            yield FilesWidget(can_focus=False)
            yield NoteWidget(can_focus=False)
        #yield AssistantWidget()
        yield Footer()

    def action_save_note(self) -> None:
        with open(self.app.query_one(NoteWidget).note_path, 'w') as file:
            file.write(self.query_one(TextArea).text)

    def action_close_note(self) -> None:
        self.query_one(TextArea).clear()
        self.query_one(NoteWidget).note_path = None

def notes_app() -> None:
    app = NotesApp()
    app.run()   

notes_app()