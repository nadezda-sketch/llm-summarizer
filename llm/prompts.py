SYSTEM_PROMPT = (
    "Ты — ассистент-суммаризатор. Отвечай только кратким пересказом "
    "на русском языке, без вводных фраз и markdown."
)

def build_messages(text: str, max_sentences: int) -> list[dict]:
    user = (
        f"Сделай суммаризацию не длиннее {max_sentences} предложений.\n\n"
        f"Текст:\n{text}"
    )
    return [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": user}
    ]