# Gerador de QRCodes Customizados

Este é um aplicativo de geração de QR Code com uma interface gráfica intuitiva desenvolvida em **Python** utilizando a biblioteca **CustomTkinter**. Ele permite criar QR Codes customizados para diferentes finalidades como links, PIX, Wi-Fi e contatos, com suporte a pré-visualização e personalização de cores, estilos e tamanho.

## 🎯 Funcionalidades

- Geração de QR Codes para:
  - Links e textos simples
  - Wi-Fi (com configuração de SSID, senha e tipo de segurança)
  - PIX (com ou sem valor definido)
  - Contatos (nome, telefone e email)
- Seleção de estilo do QR Code (quadrado, arredondado, círculo)
- Escolha de cores do QR Code e do fundo
- Opção de usar gradiente
- Opção de adicionar logo
- Pré-visualização do QR Code antes de salvar
- Salvar QR Code como imagem `.png`

## 🛠️ Bibliotecas Utilizadas

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [qrcode](https://pypi.org/project/qrcode/)
- [pybrcode](https://github.com/ViniciusFM/pybrcode)
- [Pillow (PIL)](https://pypi.org/project/Pillow/)

## 📂 Estrutura do Projeto

```bash
.
├── main.py              # Inicia a interface
├── gui.py               # Contém a classe QRApp e componentes gráficos
├── qr_generator.py      # Função de geração de QR Code
├── utils.py             # Funções auxiliares (formatação, máscaras, etc)
├── dist/                # .exe do aplicativo
└── README.md            # Este arquivo
```

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/SabrinaGuizilini/QRCode-Generator.git
   cd QRCode-Generator
   ```
2. Instale as dependências (Se preferir, crie um ambiente virtual (venv) para isolar as dependências.)
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o projeto
   ```bash
   python main.py
   ```

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
