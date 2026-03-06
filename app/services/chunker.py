import re
import tiktoken
from typing import List

# Setup the tokenizer using the standard encoding for modern LLMs.
encoding = tiktoken.get_encoding("cl100k_base")

# Hard constraint: chunks cannot exceed 512 tokens.
MAX_TOKENS = 512

def count_tokens(text: str) -> int:
    """Helper function to count tokens in a string."""
    return len(encoding.encode(text))

def chunk_markdown(markdown_text: str) -> List[str]:
    """
    Split a markdown string into chunks based on headers while strictly enforcing a token limit.
    
    Strategy:
    1. Iterate line by line.
    2. Respect Markdown Headers (H1-H3) as logical splitting points where possible.
    3. Accumulate lines into a buffer (current_chunk).
    4. If adding a line would exceed MAX_TOKENS, assume the current buffer is full and flush it.
    5. If a single line itself is larger than MAX_TOKENS, split that line into smaller pieces.
    
    Args:
        markdown_text (str): The input markdown string.
        
    Returns:
        List[str]: A list of chunk strings.
    """
    
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    # Split the text into lines to process structurally.
    lines = markdown_text.split('\n')
    
    for line in lines:
        # Calculate tokens for the line including the newline character we'll add back.
        line_tokens = count_tokens(line + '\n')
        
        # Check if the line is a Markdown header (Level 1-3).
        # Regex matches lines starting with 1 to 3 hashes followed by a space.
        is_header = re.match(r'^#{1,3}\s', line)
        
        # HEURISTIC: If we hit a header, and we already have some content in the current chunk,
        # we consider flushing the chunk to start a new "section" with the header.
        # This aligns chunks with the logical structure of the document.
        if is_header and current_chunk:
             chunk_text = '\n'.join(current_chunk)
             # Only create a chunk if there is actual content (prevent empty chunks)
             if current_tokens > 0:
                 chunks.append(chunk_text)
                 current_chunk = []
                 current_tokens = 0
        
        # CHECK: Will adding this line exceed the token limit?
        if current_tokens + line_tokens > MAX_TOKENS:
            # Yes, limits exceeded. First, flush whatever we validly have in the buffer.
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_tokens = 0
            
            # Now handle the current line.
            # Edge Case: The line *itself* is huge (larger than the limit).
            if line_tokens > MAX_TOKENS:
                # We need to split the line forcefully.
                # Since we can't iterate tokens easily, we use a character-based heuristic approximation.
                # Assuming ~4 characters per token is a safe upper bound, but we use a slice for simplicity
                # and verify against the token counter.
                line_text = line
                while count_tokens(line_text) > MAX_TOKENS:
                    # Take a slice of ~2000 chars (approx 500 tokens).
                    # This is a safety/fallback mechanism for very dense text blocks.
                    split_point = 2000
                    chunks.append(line_text[:split_point]) 
                    line_text = line_text[split_point:]
                    
                # Add the remainder of the line to the new buffer.
                current_chunk.append(line_text)
                current_tokens += count_tokens(line_text + '\n')
            else:
                # The line fits in an empty buffer, so just add it.
                current_chunk.append(line)
                current_tokens += line_tokens
        else:
            # No limit exceeded, just accumulate the line.
            current_chunk.append(line)
            current_tokens += line_tokens
            
    # Flush any remaining content in the buffer after the loop finishes.
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
        
    return chunks
