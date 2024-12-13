from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import TextArea, Input
from ollama import chat


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