import re

def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= chunk_size:
            chunk_text = " ".join(current_chunk)
            if len(current_chunk) < chunk_size:
                chunks.append(chunk_text)
                current_chunk = []
            else:
                # Ensure the chunk ends with a complete sentence
                last_punctuation = max(chunk_text.rfind('.'), chunk_text.rfind('?'), chunk_text.rfind('!'))
                if last_punctuation != -1:
                    chunks.append(chunk_text[:last_punctuation+1])
                    remaining_text = chunk_text[last_punctuation+1:].strip()
                    current_chunk = remaining_text.split()
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
