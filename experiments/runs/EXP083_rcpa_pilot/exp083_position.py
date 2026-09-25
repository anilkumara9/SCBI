"""EXP083 (R1 RCPA kill pilot) — position-identification rule (§3.3, F4).

Structural, label-free. Law #7 prohibition (pre-registered): no
position-selection rule may inspect correctness labels, target/foil
strings, or benchmark metadata. Positions are template structure —
known a priori.

  ans_pos = T - 1, the final prompt token (the ":" of the terminal "Answer:").
  q_pos   = the token index of the "?" terminating the question span:
            search the prompt STRING for "? Answer:" (M3 — substring search
            operates on text, not token IDs), take the character offset of
            the "?", and map it to its token index.

This module implements the string search and the char-offset -> token-index
mapping given the tokenizer's offset table. Tokenization itself happens on
the GPU node; the mapping is pure and testable here.
"""

Q_ANCHOR = "? Answer:"


def q_char_offset(prompt):
    """Character offset of the "?" in the "? Answer:" anchor.

    Raises ValueError if the anchor is absent — a malformed prompt is an
    apparatus fault, never silently defaulted.
    """
    idx = prompt.find(Q_ANCHOR)
    if idx < 0:
        raise ValueError("position rule fault: '? Answer:' anchor absent "
                         "from prompt (Law #7: no label-derived fallback)")
    return idx  # the "?" is the first character of the anchor


def char_offset_to_token(char_offset, token_char_spans):
    """Map a character offset to its token index.

    token_char_spans: list of (char_start, char_end) per token, as produced
    by the tokenizer's offset mapping on the GPU node. Returns the index of
    the token whose span contains char_offset. Raises ValueError if no
    token contains the offset.
    """
    for i, (s, e) in enumerate(token_char_spans):
        if s <= char_offset < e:
            return i
    raise ValueError("position rule fault: char offset %d not covered by any "
                     "token span" % char_offset)


def locate_positions(prompt, token_char_spans):
    """(ans_pos, q_pos) for one item's prompt.

    ans_pos = T - 1 (final prompt token). q_pos = token index of the "?"
    of "? Answer:". Both are template structure — no labels touched.
    """
    t = len(token_char_spans)
    if t == 0:
        raise ValueError("position rule fault: empty tokenization")
    ans_pos = t - 1
    q_pos = char_offset_to_token(q_char_offset(prompt), token_char_spans)
    if not (0 <= q_pos < ans_pos):
        raise ValueError("position rule fault: q_pos=%d not strictly before "
                         "ans_pos=%d" % (q_pos, ans_pos))
    return ans_pos, q_pos
