from enum import Enum


class Errors(Enum):
    SOMETHING_WRONG = "ChatGptWebServerError:SomethingWrong"
    NOT_COMPLY_POLICY = "ChatGptWebServerError:NotComplyPolicy"
    PROMPT_IS_EMPTY = "ChatGptWebServerError:PromptIsEmpty"
