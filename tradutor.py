from translate import Translator

# Criando um tradutor para português
translator = Translator(from_lang="pt", to_lang="en")

# Texto para traduzir
texto_original = input("digite seu texto :")

# Traduzindo
traducao = translator.translate(texto_original)

print(traducao)  # Saída: Olá, como você está?
