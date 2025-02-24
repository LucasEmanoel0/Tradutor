from translate import Translator

def traduzir_texto():
    print("Bem-vindo ao Tradutor! 🌎")
    
    translator = Translator(from_lang="pt", to_lang="en")

    while True:
        # Entrada do usuário
        texto_original = input("\nDigite o texto para tradução (ou 'sair' para encerrar): ")
        if texto_original.lower() == "sair":
            print("Obrigado por usar o tradutor! 👋")
            break

        try:
            # Tradução
            traducao = translator.translate(texto_original)
            print(f"Tradução: {traducao}")
        except Exception as e:
            print("⚠️ Erro ao traduzir! Tente novamente.")
            print(f"Detalhes do erro: {e}")

# Executar o tradutor
traduzir_texto()
