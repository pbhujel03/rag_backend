from typing import List


def fixed_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> List[str]:

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def recursive_chunking(
    text: str,
    chunk_size: int = 500
) -> List[str]:

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        if len(current_chunk) + len(paragraph) < chunk_size:
            current_chunk += paragraph + "\n\n"

        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks