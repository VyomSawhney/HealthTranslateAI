# download_models.py

from transformers import MarianMTModel, MarianTokenizer

def download_marian_model(src_lang, tgt_lang):
    language_pair = f"{src_lang}-{tgt_lang}"
    model_name = f"Helsinki-NLP/opus-mt-{language_pair}"
    cache_dir = f"models/marian/{language_pair}"

    # Download and save the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(cache_dir)

    model = MarianMTModel.from_pretrained(model_name)
    model.save_pretrained(cache_dir)

    print(f"Downloaded and saved {model_name} to {cache_dir}")

if __name__ == "__main__":
    # Download English to Spanish model
    download_marian_model('en', 'es')

    # Download Spanish to English model
    download_marian_model('es', 'en')
