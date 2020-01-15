from django.utils.text import wrap


def format_reply(sender, body):
    """
    Wraps text at 55 chars and prepends each
    line with `> `.
    Used for quoting messages in replies.
    """
    lines = wrap(body, 55).split('\n')
    for i, line in enumerate(lines):
        lines[i] = f"> {line}"
    quote = '\n'.join(lines)
    return f"{sender} wrote:\n{quote}"
