from app.kb.chunker import chunk_text


def test_chunking_with_overlap():
    text = "a" * 2100
    chunks = chunk_text(text, chunk_size=800, overlap=100)
    assert len(chunks) == 3
    assert len(chunks[0]) == 800
    assert len(chunks[1]) == 800
    assert len(chunks[2]) > 0

