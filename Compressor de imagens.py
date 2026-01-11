from PIL import Image  # Biblioteca Pillow: abrir, editar e salvar imagens
import os              # Biblioteca padrão: lidar com pastas/caminhos do Windows
import shutil          # Biblioteca padrão: cópia de arquivos (não é essencial agora, mas pode ser útil)


# ----------------------------
# Funções para perguntar dados no terminal
# ----------------------------

def perguntar_int(msg, padrao):
    """
    Pergunta um número inteiro no terminal.
    Se o usuário só apertar Enter, usa o valor padrão.
    """
    entrada = input(f"{msg} (padrão: {padrao}): ").strip()
    return int(entrada) if entrada else padrao


def perguntar_str(msg, padrao):
    """
    Pergunta um texto no terminal.
    Se o usuário só apertar Enter, usa o valor padrão.
    Converte para MAIÚSCULO para facilitar validações (JPEG/PNG/WEBP).
    """
    entrada = input(f"{msg} (padrão: {padrao}): ").strip()
    return entrada.upper() if entrada else padrao


# ----------------------------
# Pastas do projeto
# ----------------------------

# __file__ é o caminho do arquivo .py atual
# os.path.abspath(__file__) transforma em caminho absoluto
# os.path.dirname(...) pega apenas a pasta onde o script está
base = os.path.dirname(os.path.abspath(__file__))

# Pasta de entrada e saída (ficam ao lado do script)
pasta_entrada = os.path.join(base, "IMAGENS")                 # os.path.join junta caminhos do jeito correto no Windows
pasta_saida = os.path.join(base, "Imagens_Comprimidas")

# Cria a pasta de saída caso não exista
os.makedirs(pasta_saida, exist_ok=True)

# Se a pasta de entrada não existir, para o programa
if not os.path.exists(pasta_entrada):
    print("ERRO: pasta não encontrada:", pasta_entrada)
    raise SystemExit


# ----------------------------
# Perguntas para configurar o processamento
# ----------------------------

largura_max = perguntar_int("Digite a LARGURA máxima em pixels (ex: 800)", 800)

formato = perguntar_str("Escolha o formato de saída: JPEG, PNG ou WEBP", "JPEG")
while formato not in ("JPEG", "PNG", "WEBP"):
    formato = perguntar_str("Formato inválido. Use JPEG, PNG ou WEBP", "JPEG")

qualidade = 80
if formato in ("JPEG", "WEBP"):
    qualidade = perguntar_int("Qualidade (0-100) para JPEG/WEBP", 80)

# Mantemos esse valor apenas para “referência/relatório”
# (agora NÃO pulemos mais imagens por causa dele)
limite_kb = perguntar_int("Limite em KB (apenas para relatório, NÃO pula mais imagens)", 0)


print("\nConfiguração escolhida:")
print(" - largura_max:", largura_max)
print(" - formato:", formato)
print(" - qualidade:", qualidade if formato in ("JPEG", "WEBP") else "(não se aplica)")
print(" - limite_kb (apenas relatório):", limite_kb)
print("\nProcessando...\n")


# ----------------------------
# Processamento das imagens
# ----------------------------

# Extensões que vamos aceitar como entrada
ext_validas = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")

# Contadores para o resumo final
processadas = 0
erros = 0
abaixo_limite = 0
acima_limite = 0

# Para calcular compressão total do lote
total_original = 0
total_final = 0

for nome in os.listdir(pasta_entrada):
    caminho = os.path.join(pasta_entrada, nome)

    # Ignora pastas dentro de IMAGENS
    if os.path.isdir(caminho):
        continue

    # Ignora arquivos que não são imagens suportadas
    if not nome.lower().endswith(ext_validas):
        print(f"PULOU (não é imagem suportada): {nome}")
        continue

    try:
        # Tamanho do arquivo original em bytes (os.path.getsize)
        tamanho_original = os.path.getsize(caminho)
        tamanho_original_kb = tamanho_original / 1024

        # Apenas para estatística/relatório
        if limite_kb > 0 and tamanho_original_kb < limite_kb:
            abaixo_limite += 1
        else:
            acima_limite += 1

        # Abre a imagem com Pillow:
        # with garante que o arquivo será fechado corretamente depois (importante no Windows)
        with Image.open(caminho) as img:
            # img.size retorna (largura, altura)
            w, h = img.size

            # Se a largura for maior que a desejada, redimensiona mantendo proporção
            if w > largura_max:
                # Mantém proporção: calcula nova altura pela regra de três
                nova_altura = int((largura_max / w) * h)

                # img.resize((largura, altura), filtro)
                # Image.LANCZOS é um filtro de alta qualidade para reduzir imagens
                img = img.resize((largura_max, nova_altura), Image.LANCZOS)

            # Monta nome base (sem extensão) e define o nome final com o formato escolhido
            nome_base = os.path.splitext(nome)[0]
            novo_nome = f"{nome_base}.{formato.lower()}"
            saida = os.path.join(pasta_saida, novo_nome)

            # Regras por formato de saída
            if formato == "JPEG":
                # JPEG NÃO suporta transparência (alpha).
                # Se a imagem tiver alpha (RGBA/LA), criamos um fundo branco.
                if img.mode in ("RGBA", "LA"):
                    fundo = Image.new("RGB", img.size, (255, 255, 255))  # cria imagem branca RGB
                    fundo.paste(img, mask=img.split()[-1])              # cola usando alpha como máscara
                    img = fundo
                else:
                    # Converte para RGB porque JPEG não usa modos como "P" ou "CMYK" em alguns casos
                    img = img.convert("RGB")

                # optimize=True tenta reduzir o tamanho do arquivo JPEG
                # quality controla a compressão: menor = mais compressão
                img.save(saida, "JPEG", quality=qualidade, optimize=True)

            elif formato == "WEBP":
                # WEBP costuma ser excelente para compressão moderna
                # Convertendo para RGB se estiver em um modo estranho
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")

                img.save(saida, "WEBP", quality=qualidade)

            else:  # PNG
                # PNG é lossless (sem perda) na maioria dos casos
                # optimize=True tenta reduzir um pouco o tamanho
                img.save(saida, "PNG", optimize=True)

        # Calcula tamanho final do arquivo gerado
        tamanho_final = os.path.getsize(saida)

        # Atualiza totais para compressão total
        total_original += tamanho_original
        total_final += tamanho_final

        # Calcula porcentagem de redução (pode ser negativo se aumentar)
        porcentagem = (1 - (tamanho_final / tamanho_original)) * 100

        if porcentagem >= 0:
            print(f"OK: {nome} -> {novo_nome} | reduziu {porcentagem:.1f}%")
        else:
            print(f"OK: {nome} -> {novo_nome} | aumentou {abs(porcentagem):.1f}%")

        processadas += 1

    except Exception as e:
        print(f"ERRO em {nome}: {e}")
        erros += 1


# ----------------------------
# Resumo final
# ----------------------------

print("\nFinalizado!")
print(f" - Processadas: {processadas}")
print(f" - Abaixo do limite (apenas relatório): {abaixo_limite}")
print(f" - Acima do limite (apenas relatório): {acima_limite}")
print(f" - Erros: {erros}")

if total_original > 0:
    economia_total = (1 - (total_final / total_original)) * 100
    if economia_total >= 0:
        print(f" - Compressão total do lote: reduziu {economia_total:.1f}%")
    else:
        print(f" - Compressão total do lote: aumentou {abs(economia_total):.1f}%")

print("Imagens salvas em:", pasta_saida)
