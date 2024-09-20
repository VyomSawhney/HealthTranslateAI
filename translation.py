# translation.py

from transformers import MarianMTModel, MarianTokenizer

def load_translation_models():
    models = {}
    for src_lang, tgt_lang in [('en', 'es'), ('es', 'en')]:
        language_pair = f"{src_lang}-{tgt_lang}"
        cache_dir = f"models/marian/{language_pair}"

        # Load tokenizer and model from local cache
        tokenizer = MarianTokenizer.from_pretrained(cache_dir)
        model = MarianMTModel.from_pretrained(cache_dir)

        models[(src_lang, tgt_lang)] = (tokenizer, model)
    return models

def translate_text(text, tokenizer, model):
    # Tokenize input text
    batch = tokenizer([text], return_tensors="pt", padding=True)

    # Generate translation
    generated_tokens = model.generate(**batch)

    # Decode translated tokens
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    print(f"Translated Text: {translated_text}")
    return translated_text