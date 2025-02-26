from googletrans import Translator
import re

class AutomatoFinitoDeterministico:
    def __init__(self, palavras_proibidas):
        self.estados = {}
        self.estado_final = "F"
        self.estado_inicial = "S"
        self.construir_automato(palavras_proibidas)
    
    def construir_automato(self, palavras):
        for palavra in palavras:
            estado_atual = self.estado_inicial
            for char in palavra:
                if (estado_atual, char) not in self.estados:
                    novo_estado = f"{estado_atual}_{char}"
                    self.estados[(estado_atual, char)] = novo_estado
                    estado_atual = novo_estado
                else:
                    estado_atual = self.estados[(estado_atual, char)]
            self.estados[(estado_atual, "")] = self.estado_final
    
    def reconhecer(self, texto):
        for i in range(len(texto)):
            estado_atual = self.estado_inicial
            for j in range(i, len(texto)):
                char = texto[j].lower()
                if (estado_atual, char) in self.estados:
                    estado_atual = self.estados[(estado_atual, char)]
                    if (estado_atual, "") in self.estados:
                        return True, texto[i:j+1]
                else:
                    break
        return False, ""

def limpar_texto(texto):
    return re.sub(r'[^\w\s]', '', texto)

def carregar_palavroes():
    try:
        with open('palavras.txt', 'r', encoding='utf-8') as file:
            return sorted(set(line.strip().lower() for line in file))
    except FileNotFoundError:
        return []

def salvar_palavroes(palavras):
    with open('palavras.txt', 'w', encoding='utf-8') as file:
        file.writelines(line + '\n' for line in palavras)

palavroes = carregar_palavroes()
salvar_palavroes(palavroes)
afd = AutomatoFinitoDeterministico(palavroes)

def traduzir_texto():
    print("Bem-vindo ao Tradutor! 🌎")
    translator = Translator()
    
    idiomas_disponiveis = {
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "it"
    }
    
    print("Escolha o idioma para tradução:")
    print("1 - Inglês (English)")
    print("2 - Espanhol (Español)")
    print("3 - Francês (Français)")
    print("4 - Alemão (Deutsch)")
    print("5 - Italiano (Italiano)")
    
    escolha = input("Digite o número correspondente ao idioma desejado: ")
    idioma_destino = idiomas_disponiveis.get(escolha, "en")
    print(f"Idioma escolhido: {idioma_destino}\n")
    
    while True:
        texto_original = input("\nDigite o texto para tradução (ou 'sair' para encerrar): ")
        if texto_original.lower() == "sair":
            print("Obrigado por usar o tradutor! 👋")
            break
        
        texto_limpo = limpar_texto(texto_original)
        palavrao_detectado, palavra = afd.reconhecer(texto_limpo)
        
        if palavrao_detectado:
            print(f"⚠️ Palavra inadequada detectada: {palavra}. Tradução bloqueada.")
            continue
        
        try:
            traducao = translator.translate(texto_limpo, src='pt', dest=idioma_destino).text
            print(f"Tradução: {traducao}")
        except Exception as e:
            print("⚠️ Erro ao traduzir! Tente novamente.")
            print(f"Detalhes do erro: {e}")

traduzir_texto()