import tiktoken

GPT_35_MAX_TOKEN = 4096


def discard_overlimit_messages(messages: list):
    """
    Discards messages that exceed the maximum number of tokens allowed by OpenAI.
    only for gpt-3.5 now
    :param messages:
    :return:
    """
    token_count = 0
    for i in range(len(messages) - 1, -1, -1):
        chat = messages[i]
        token_count += num_tokens_from_string(chat["content"], "cl100k_base")
        if token_count > GPT_35_MAX_TOKEN:
            return messages[i + 1:]

    return messages


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == '__main__':
    print(num_tokens_from_string("test", "cl100k_base"))
    print(discard_overlimit_messages(
        [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "test"}]))
