"""Phonétique française (IPA) d'un mot ou d'un groupe de mots, via espeak-ng (pip install espeakng-loader phonemizer-fork).
Sert à imposer à la voix la prononciation exacte d'une élision (l'effort -> lefɔʁ) au lieu de coller l'apostrophe, qui a fait lire
« le fort » et « tain apporter » (2026-11-20). Retourne None si l'outil n'est pas installé."""
def ipa(text):
    try:
        import espeakng_loader
        from phonemizer import phonemize
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        EspeakWrapper.set_library(espeakng_loader.get_library_path())
        EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
        return phonemize(text, language="fr-fr", backend="espeak", strip=True)
    except Exception:
        return None
