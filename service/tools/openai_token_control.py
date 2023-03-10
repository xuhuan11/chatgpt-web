import tiktoken

GPT_35_MAX_TOKEN = 4096


def discard_overlimit_messages(messages: list):
    """
    Discards messages that exceed the maximum number of tokens allowed by OpenAI.
    only for gpt-3.5 now
    :param messages:
    :return:
    """

    token_count = num_tokens_from_messages(messages)
    if token_count <= GPT_35_MAX_TOKEN:
        return messages

    token_count = 0
    for i in range(len(messages) - 1, -1, -1):
        chat = messages[i]
        token_count += num_tokens_from_string(chat["content"], "gpt-3.5-turbo-0301")
        if token_count > GPT_35_MAX_TOKEN:
            return messages[i + 1:]

    return messages


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


if __name__ == '__main__':
    print(num_tokens_from_string("test", "cl100k_base"))
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "test"}]
    print(num_tokens_from_messages(messages, "gpt-3.5-turbo-0301"))
    print(discard_overlimit_messages(
        [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "test"}]))
