#Leia-me

# Compressor de Imagens em Python

Este programa permite **comprimir e redimensionar várias imagens automaticamente**, escolhendo:
- Largura máxima em pixels  
- Formato de saída (JPEG, PNG ou WEBP)  
- Qualidade da compressão  
- Tamanho mínimo do arquivo para aplicar compressão  

Imagens menores que o tamanho mínimo escolhido **não são comprimidas**, apenas copiadas para a pasta de saída.

---

## Requisitos

- Python 3.8 ou superior  
- Biblioteca Pillow

Instale o Pillow com:

pip install pillow

---

##  Estrutura de Pastas

Antes de executar, organize assim:

python_work/
├── Novo_compressor_de_imagens.py
├── IMAGENS/
│   ├── foto1.jpg
│   ├── foto2.png
│   └── ...
└── Imagens_Comprimidas/   # criada automaticamente

- **IMAGENS** → Coloque aqui todas as imagens originais  
- **Imagens_Comprimidas** → O programa cria automaticamente e salva os resultados

---

##  Como executar

No terminal, rode:

python "Novo compressor de imagens.py"

O programa fará perguntas:

1. Largura máxima em pixels  
2. Formato de saída (JPEG, PNG ou WEBP)  
3. Qualidade (para JPEG e WEBP)  
4. Tamanho mínimo em KB para aplicar compressão  

---

##  Como funciona

### Imagens MENORES que o tamanho mínimo
- Não são comprimidas  
- São apenas copiadas para a pasta Imagens_Comprimidas  
- Mantêm formato e tamanho originais  

### Imagens MAIORES ou IGUAIS ao tamanho mínimo
- Podem ser redimensionadas  
- Convertidas para o formato escolhido  
- Comprimidas com a qualidade definida  

---

## Redimensionamento

Se a imagem for maior que a largura máxima escolhida:
- Ela é reduzida proporcionalmente  
- A altura é ajustada automaticamente  
- Não ocorre distorção

---

## Formatos disponíveis

### Entrada aceita:
.jpg .jpeg .png .webp .bmp .tif .tiff

### Saída:
- JPEG → Melhor para fotos  
- PNG → Mantém transparência  
- WEBP → Alta compressão moderna

---

## Relatório no final

Ao terminar, o programa mostra:

- Quantas imagens foram comprimidas  
- Quantas foram copiadas sem compressão  
- Quantos erros ocorreram  
- Percentual total de compressão alcançado  

Exemplo:

COMPRIMIU: foto1.png -> foto1.webp | -62.4%
SEM COMPRESSÃO: logo.png -> copiada igual

Finalizado!
 - Comprimidas: 5
 - Copiadas sem compressão: 2
 - Erros: 0
 - Compressão total: -54.8%

---

## Dicas de uso

### Para fotos:
- Formato: JPEG ou WEBP  
- Qualidade: 70 a 85  
- Largura: 800 a 1920  

### Para logos com transparência:
- Formato: PNG ou WEBP  

---

## Problemas comuns

### Pasta IMAGENS não encontrada
Verifique se a pasta IMAGENS está no mesmo local do arquivo .py.

### Algumas imagens não comprimem
Arquivos pequenos são apenas copiados (regra do tamanho mínimo).

---

## Licença

Uso livre para estudos e projetos pessoais.

---

## Autor

Arthur Rocha Lima
Script desenvolvido como compressor de imagens em lote usando Python + Pillow.

