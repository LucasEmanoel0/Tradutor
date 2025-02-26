# Importação das bibliotecas necessárias
from googletrans import Translator  # Biblioteca para tradução de textos
import re  # Biblioteca para expressões regulares
import asyncio  # Biblioteca para programação assíncrona

# Definição da classe AutomatoFinitoDeterministico
class AutomatoFinitoDeterministico:
    def __init__(self, palavras_proibidas):
        # Inicialização dos estados do autômato
        self.estados = {}
        # Definição do estado final e inicial
        self.estado_final = "F"
        self.estado_inicial = "S"
        # Construção do autômato com as palavras proibidas
        self.construir_automato(palavras_proibidas)
    
    # Método para construir o autômato com base nas palavras proibidas
    def construir_automato(self, palavras):
        for palavra in palavras:
            estado_atual = self.estado_inicial
            for char in palavra:
                # Verifica se a transição (estado_atual, char) já existe
                if (estado_atual, char) not in self.estados:
                    # Cria um novo estado para a transição
                    novo_estado = f"{estado_atual}_{char}"
                    self.estados[(estado_atual, char)] = novo_estado
                    estado_atual = novo_estado
                else:
                    # Se a transição já existe, move para o próximo estado
                    estado_atual = self.estados[(estado_atual, char)]
            # Define o estado final para a palavra
            self.estados[(estado_atual, "")] = self.estado_final
    
    # Método para reconhecer palavras proibidas no texto
    def reconhecer(self, texto):
        for i in range(len(texto)):
            estado_atual = self.estado_inicial
            for j in range(i, len(texto)):
                char = texto[j].lower()
                # Verifica se a transição (estado_atual, char) existe
                if (estado_atual, char) in self.estados:
                    estado_atual = self.estados[(estado_atual, char)]
                    # Verifica se chegou ao estado final
                    if (estado_atual, "") in self.estados:
                        return True, texto[i:j+1]
                else:
                    break
        return False, ""

# Função para limpar o texto, removendo caracteres especiais
def limpar_texto(texto):
    return re.sub(r'[^\w\s]', '', texto)

# Função para carregar as palavras proibidas de um arquivo
def carregar_palavroes():
    try:
        with open('palavras.txt', 'r', encoding='utf-8') as file:
            # Lê as palavras do arquivo, remove duplicatas e ordena
            return sorted(set(line.strip().lower() for line in file))
    except FileNotFoundError:
        # Retorna uma lista vazia se o arquivo não for encontrado
        return []

# Função para salvar as palavras proibidas em um arquivo
def salvar_palavroes(palavras):
    with open('palavras.txt', 'w', encoding='utf-8') as file:
        # Escreve cada palavra no arquivo
        file.writelines(line + '\n' for line in palavras)

# Carrega as palavras proibidas do arquivo e salva novamente (para garantir ordenação e unicidade)
palavroes = carregar_palavroes()
salvar_palavroes(palavroes)

# Cria uma instância do autômato com as palavras proibidas
afd = AutomatoFinitoDeterministico(palavroes)

# Função assíncrona para traduzir texto
async def traduzir_texto():
    print("Bem-vindo ao Tradutor! 🌎")
    translator = Translator()
    
    # Dicionário de idiomas disponíveis para tradução
    idiomas_disponiveis = {
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "it"
    }
    
    # Exibe as opções de idiomas para o usuário
    print("Escolha o idioma para tradução:")
    print("1 - Inglês (English)")
    print("2 - Espanhol (Español)")
    print("3 - Francês (Français)")
    print("4 - Alemão (Deutsch)")
    print("5 - Italiano (Italiano)")
    
    # Solicita ao usuário que escolha um idioma
    escolha = input("Digite o número correspondente ao idioma desejado: ")
    idioma_destino = idiomas_disponiveis.get(escolha, "en")  # Define o idioma de destino
    print(f"Idioma escolhido: {idioma_destino}\n")
    
    # Loop para traduzir textos até que o usuário decida sair
    while True:
        texto_original = input("\nDigite o texto para tradução (ou 'sair' para encerrar): ")
        if texto_original.lower() == "sair":
            print("Obrigado por usar o tradutor! 👋")
            break
        
        # Limpa o texto de caracteres especiais
        texto_limpo = limpar_texto(texto_original)
        # Verifica se o texto contém palavras proibidas
        palavrao_detectado, palavra = afd.reconhecer(texto_limpo)
        
        # Se uma palavra proibida for detectada, bloqueia a tradução
        if palavrao_detectado:
            print(f"⚠️ Palavra inadequada detectada: {palavra}. Tradução bloqueada.")
            continue
        
        # Tenta traduzir o texto
        try:
            traducao = await translator.translate(texto_limpo, src='pt', dest=idioma_destino)
            print(f"Tradução: {traducao.text}")
        except Exception as e:
            # Em caso de erro, exibe uma mensagem de erro
            print("⚠️ Erro ao traduzir! Tente novamente.")
            print(f"Detalhes do erro: {e}")

# Executa a função assíncrona de tradução
asyncio.run(traduzir_texto())
