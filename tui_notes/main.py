from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, VerticalScroll
from textual.widgets import Footer, DirectoryTree, TextArea, Markdown, MarkdownViewer, Input
from ollama import chat


class FilesWidget(VerticalScroll):

    BORDER_TITLE = 'Files'

    def compose(self) -> ComposeResult:
        yield DirectoryTree('./notes/')

    def on_directory_tree_file_selected(self, message: DirectoryTree.FileSelected):
        if str(message.path).endswith('.md'):
            with open(message.path) as f:
                self.app.query_one(NoteWidget).note_path = str(message.path)
                self.app.query_one(TextArea).load_text(f.read())

class NoteWidget(HorizontalScroll):

    BORDER_TITLE = 'Note'

    def compose(self) -> ComposeResult:
        yield VerticalScroll(TextArea())
        yield VerticalScroll(MarkdownViewer(show_table_of_contents=False))
    
    def on_text_area_changed(self, message: TextArea.Changed) -> None:
        self.query_one(Markdown).update(message.text_area.text)

class AssistantWidget(VerticalScroll):

    BORDER_TITLE = 'Assistant'

    def compose(self) -> ComposeResult:
        yield Input(id='assistant')

    def on_input_submitted(self, message: Input.Submitted) -> None:
        response = chat(
            model='llama3.2:latest',
            messages=[{'role': 'user', 'content': f'Given this context: {self.app.query_one(TextArea).text}, please: {message.value}'}]
        )
        self.app.query_one(TextArea).clear()
        self.app.query_one(TextArea).load_text(response['message']['content'])

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
        yield AssistantWidget()
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