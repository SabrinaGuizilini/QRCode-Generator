import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from PIL import Image
from tkinter.colorchooser import askcolor
from pybrcode.pix import generate_simple_pix
import re

from utils import hex_para_rgb, permitir_somente_numeros, formatar_valor_pix, formatar_chave_pix
from qr_generator import gerar_qrcode_personalizado

class QRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de QR Code Customizado")
        self.geometry("900x780")
        self.logo_path = None
        self.cor = "#000000"
        self.fundo = "#ffffff"
        self.quadro_cor_qr = None
        self.quadro_cor_fundo = None

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.build_ui()

    def build_ui(self):
        """
        Monta a interface com abas e campos de entrada.
        """

        # Abas
        frame_tabs = ctk.CTkFrame(self, height=300, width=600)
        frame_tabs.pack(pady=10, padx=20)
        frame_tabs.pack_propagate(False)

        self.tabview = ctk.CTkTabview(frame_tabs, width=500, corner_radius=8)
        self.tabview.pack(expand=True, fill="both")

        self.tabs = {
            "link": self.tabview.add("🔗 Link/Texto"),
            "wifi": self.tabview.add("📶 Wi-Fi"),
            "pix": self.tabview.add("💰 PIX"),
            "contato": self.tabview.add("📞 Contato")
        }

        # CAMPOS DE CADA ABA
        # ABA LINK
        ctk.CTkLabel(self.tabs["link"], text="Texto ou link:").pack(pady=5)
        self.entry_link = ctk.CTkEntry(self.tabs["link"], width=400)
        self.entry_link.pack(pady=5)

        # ABA WIFI
        ctk.CTkLabel(self.tabs["wifi"], text="Nome da rede (SSID):").pack(pady=5)
        self.entry_ssid = ctk.CTkEntry(self.tabs["wifi"], width=300)
        self.entry_ssid.pack(pady=5)

        ctk.CTkLabel(self.tabs["wifi"], text="Senha:").pack(pady=5)
        self.entry_senha = ctk.CTkEntry(self.tabs["wifi"], show="*", width=300)
        self.entry_senha.pack(pady=5)

        ctk.CTkLabel(self.tabs["wifi"], text="Tipo de segurança:").pack(pady=5)
        self.combo_tipo = ctk.CTkComboBox(self.tabs["wifi"], values=["WPA", "WEP", "nopass"], width=300, state="readonly")
        self.combo_tipo.set("WPA")
        self.combo_tipo.pack(pady=5)

        # ABA PIX
        frame_chave = ctk.CTkFrame(self.tabs["pix"], fg_color="transparent")
        frame_chave.pack(pady=5)

        ctk.CTkLabel(frame_chave, text="Tipo:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.combo_tipo_chave = ctk.CTkComboBox(
            frame_chave,
            values=["CPF", "CNPJ", "E-mail", "Telefone", "Aleatória"],
            width=100,
            state="readonly"
        )
        self.combo_tipo_chave.grid(row=1, column=0, padx=(0, 10))
        self.combo_tipo_chave.set("CPF")  # valor padrão
        self.combo_tipo_chave.bind("<<ComboboxSelected>>", self.atualizar_mascara_chave)

        ctk.CTkLabel(frame_chave, text="Chave PIX:").grid(row=0, column=1, sticky="w", padx=(0, 10))
        self.entry_pix = ctk.CTkEntry(frame_chave, width=200)
        self.entry_pix.grid(row=1, column=1, padx=(0, 10))
        self.entry_pix.bind("<KeyRelease>", self.atualizar_mascara_chave)

        ctk.CTkLabel(self.tabs["pix"], text="Nome do recebedor (até 25 letras):").pack(pady=5)
        self.entry_nome_pix = ctk.CTkEntry(self.tabs["pix"], width=320)
        self.entry_nome_pix.pack(pady=5)
        self.entry_nome_pix.bind("<KeyRelease>", self.limitar_nome_recebedor)

        ctk.CTkLabel(self.tabs["pix"], text="Valor em R$ (opcional):").pack(pady=5)
        self.entry_valor_pix = ctk.CTkEntry(self.tabs["pix"], width=320)
        self.entry_valor_pix.pack(pady=5)
        self.entry_valor_pix.bind("<KeyRelease>", self.aplicar_mascara_valor_pix)

        # ABA CONTATO
        ctk.CTkLabel(self.tabs["contato"], text="Nome:").pack(pady=5)
        self.entry_nome = ctk.CTkEntry(self.tabs["contato"], width=300)
        self.entry_nome.pack(pady=5)

        ctk.CTkLabel(self.tabs["contato"], text="Telefone:").pack(pady=5)
        vcmd = self.register(permitir_somente_numeros)
        self.entry_tel = ctk.CTkEntry(self.tabs["contato"], width=300, validate="key", validatecommand=(vcmd, "%P"))
        self.entry_tel.pack(pady=5)

        ctk.CTkLabel(self.tabs["contato"], text="Email (opcional):").pack(pady=5)
        self.entry_email = ctk.CTkEntry(self.tabs["contato"], width=300)
        self.entry_email.pack(pady=5)

        # ÁREA INFERIOR
        area_opcoes = ctk.CTkFrame(self)
        area_opcoes.pack(pady=20, padx=20, fill="both", expand=True)

        area_opcoes.columnconfigure((0, 1, 2), weight=1)

        # COLUNA ESQUERDA
        coluna_esquerda = ctk.CTkFrame(area_opcoes, fg_color="transparent")
        coluna_esquerda.grid(row=0, column=0, sticky="nsew", padx=10, pady=20)

        ctk.CTkLabel(coluna_esquerda, text="Estilo do QR Code:").pack(pady=(0, 1))
        self.combo_estilo = ctk.CTkComboBox(coluna_esquerda, values=["Quadrado", "Arredondado", "Círculo"], state="readonly", width=180)
        self.combo_estilo.set("Quadrado")
        self.combo_estilo.pack(pady=(2, 15))

        # Cor do QR
        frame_cor_qr = ctk.CTkFrame(coluna_esquerda, fg_color="transparent")
        frame_cor_qr.pack(pady=5)
        btn_cor_qr = ctk.CTkButton(frame_cor_qr, text="Selecionar cor do QR", width=150, command=lambda: self.selecionar_cor(True))
        btn_cor_qr.pack(side="left", padx=(0, 10))
        self.quadro_cor_qr = ctk.CTkLabel(frame_cor_qr, text="", width=20, height=20, fg_color=self.cor, corner_radius=4)
        self.quadro_cor_qr.pack(side="left")
        frame_cor_qr.pack_configure(anchor="center")

        # Cor de fundo
        frame_cor_fundo = ctk.CTkFrame(coluna_esquerda, fg_color="transparent")
        frame_cor_fundo.pack(pady=(10, 5))
        btn_cor_fundo = ctk.CTkButton(frame_cor_fundo, text="Selecionar cor de fundo", width=150, command=lambda: self.selecionar_cor(False))
        btn_cor_fundo.pack(side="left", padx=(0, 10))
        self.quadro_cor_fundo = ctk.CTkLabel(frame_cor_fundo, text="", width=20, height=20, fg_color=self.fundo, corner_radius=4)
        self.quadro_cor_fundo.pack(side="left")
        frame_cor_fundo.pack_configure(anchor="center")

        self.var_gradiente = ctk.BooleanVar()
        ctk.CTkCheckBox(coluna_esquerda, text="Usar gradiente", variable=self.var_gradiente).pack(pady=8)

        # Selecionar logo (opcional)
        frame_logo = ctk.CTkFrame(coluna_esquerda, fg_color="transparent")
        frame_logo.pack(pady=(15,0))
        btn_logo = ctk.CTkButton(frame_logo, text="Selecionar logo (opcional)", width=180, command=self.selecionar_logo)
        btn_logo.pack()
        frame_logo.pack_configure(anchor="center")

        # COLUNA CENTRAL (PRÉVIA)
        coluna_centro = ctk.CTkFrame(area_opcoes, fg_color="transparent")
        coluna_centro.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        ctk.CTkLabel(coluna_centro, text="Prévia do QR Code:", font=("Arial", 15)).pack(pady=(0, 10))
        self.qr_frame = ctk.CTkFrame(coluna_centro, width=200, height=200, fg_color="white", corner_radius=8)
        self.qr_frame.pack(pady=5)
        self.qr_frame.pack_propagate(False)

        self.preview = ctk.CTkLabel(self.qr_frame, text="")
        self.preview.pack(expand=True)

        # COLUNA DIREITA
        coluna_direita = ctk.CTkFrame(area_opcoes, fg_color="transparent")
        coluna_direita.grid(row=0, column=2, sticky="nsew", padx=10, pady=20)

        ctk.CTkButton(
            coluna_direita,
            text="Ver prévia",
            command=self.ver_previa,
            width=150,
            height=50
        ).pack(pady=(10, 10))

        ctk.CTkButton(coluna_direita, text="Salvar QR Code", command=self.salvar_qr, width=150, height=50).pack(pady=10)

        ctk.CTkLabel(coluna_direita, text="Tamanho da imagem:").pack(pady=(10, 5))

        self.opcao_tamanho = ctk.CTkComboBox(
            coluna_direita,
            values=["250x250", "500x500", "1000x1000"],
            state="readonly",
            width=150
        )
        self.opcao_tamanho.set("500x500")
        self.opcao_tamanho.pack(pady=(0, 20))

    def selecionar_cor(self, frente=True):
        cor = askcolor()[1]
        if cor:
            if frente:
                self.cor = cor
                if self.quadro_cor_qr:
                    self.quadro_cor_qr.configure(fg_color=cor)
            else:
                self.fundo = cor
                if self.quadro_cor_fundo:
                    self.quadro_cor_fundo.configure(fg_color=cor)


    def selecionar_logo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens PNG", "*.png"), ("Todos os arquivos", "*.*")])
        if caminho:
            self.logo_path = caminho
            messagebox.showinfo("Logo", f"Logo carregada:\n{caminho}")

    def aplicar_mascara_valor_pix(self, event=None):
        valor_original = self.entry_valor_pix.get()
        valor_formatado = formatar_valor_pix(valor_original)
        
        if valor_formatado != valor_original:
            self.entry_valor_pix.delete(0, "end")
            self.entry_valor_pix.insert(0, valor_formatado)

    def atualizar_mascara_chave(self, event=None):
        tipo = self.combo_tipo_chave.get()
        valor_original = self.entry_pix.get()
        valor_formatado = formatar_chave_pix(tipo, valor_original)

        if valor_formatado != valor_original:
            self.entry_pix.delete(0, "end")
            self.entry_pix.insert(0, valor_formatado)

    def limitar_nome_recebedor(self, event=None):
        nome = self.entry_nome_pix.get()
        if len(nome) > 25:
            self.entry_nome_pix.delete(0, "end")
            self.entry_nome_pix.insert(0, nome[:25])

    def validar_campos(self):
        aba = self.tabview.get()

        if aba == "🔗 Link/Texto":
            if not self.entry_link.get().strip():
                messagebox.showerror("Erro", "O campo de texto/link não pode estar vazio.")
                return False

        elif aba == "📶 Wi-Fi":
            ssid = self.entry_ssid.get().strip()
            senha = self.entry_senha.get().strip()
            tipo = self.combo_tipo.get()

            if not ssid:
                messagebox.showerror("Erro", "O campo 'Nome da rede (SSID)' não pode estar vazio.")
                return False

            if tipo != "nopass" and not senha:
                messagebox.showerror("Erro", "O campo 'Senha' não pode estar vazio para redes com segurança.")
                return False

        elif aba == "💰 PIX":
            chave = self.entry_pix.get().strip()
            if not chave:
                messagebox.showerror("Erro", "O campo de chave PIX não pode estar vazio.")
                return False
            if not self.entry_nome_pix.get().strip():
                messagebox.showerror("Erro", "O campo de nome do recebedor não pode estar vazio.")
                return False
            
            tipo = self.combo_tipo_chave.get()
            if tipo == "E-mail":
                if not re.match(r"[^@]+@[^@]+\.[^@]+", chave):
                    messagebox.showerror("Erro", "E-mail inválido.")
                    return False

            elif tipo == "Aleatória":
                if len(chave) != 36:
                    messagebox.showerror("Erro", "Chave aleatória deve conter 36 caracteres.")
                    return False

            elif tipo == "CPF":
                if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", chave):
                    messagebox.showerror("Erro", "CPF inválido.")
                    return False

            elif tipo == "CNPJ":
                if not re.match(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", chave):
                    messagebox.showerror("Erro", "CNPJ inválido.")
                    return False

            elif tipo == "Telefone":
                if not re.match(r"\(\d{2}\) \d{5}-\d{4}", chave):
                    messagebox.showerror("Erro", "Telefone inválido.")
                    return False

        elif aba == "📞 Contato":
            nome = self.entry_nome.get().strip()
            tel = self.entry_tel.get().strip()
            email = self.entry_email.get().strip()

            if not nome:
                messagebox.showerror("Erro", "O campo 'Nome' não pode estar vazio.")
                return False
            if not tel:
                messagebox.showerror("Erro", "O campo 'Telefone' não pode estar vazio.")
                return False
            if email != "" and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Erro", "O campo 'Email' deve conter um endereço válido.")
                return False

        return True
    
    def limpar_campos(self):
        # Aba Link/Texto
        self.entry_link.delete(0, "end")

        # Aba Wi-Fi
        self.entry_ssid.delete(0, "end")
        self.entry_senha.delete(0, "end")
        self.combo_tipo.set("WPA")

        # Aba PIX
        self.entry_pix.delete(0, "end")
        self.entry_nome_pix.delete(0, "end")
        self.entry_valor_pix.delete(0, "end")
        self.combo_tipo_chave.set("CPF")

        # Aba Contato
        self.entry_nome.delete(0, "end")
        self.entry_tel.delete(0, "end")
        self.entry_email.delete(0, "end")

        self.logo_path = None
        self.cor = "#000000"
        self.fundo = "#ffffff"
        self.quadro_cor_qr.configure(fg_color=self.cor)
        self.quadro_cor_fundo.configure(fg_color=self.fundo)
        self.var_gradiente.set(False)
        self.combo_estilo.set("Quadrado")
        self.opcao_tamanho.set("500x500")
        img = Image.new('RGB', (220, 220), color='white')
        ctk_img = CTkImage(light_image=img, size=(220, 220))
        self.preview.configure(image=ctk_img, text="")
        self.preview.image = ctk_img

    def montar_dado(self):
        tipo = self.tabview.get()

        if tipo == "🔗 Link/Texto":
            return self.entry_link.get()

        elif tipo == "📶 Wi-Fi":
            ssid = self.entry_ssid.get()
            senha = self.entry_senha.get()
            tipo_seguranca = self.combo_tipo.get()
            if tipo_seguranca == "nopass":
                return f"WIFI:T:nopass;S:{ssid};;"
            else:
                return f"WIFI:T:{tipo_seguranca};S:{ssid};P:{senha};;"

        elif tipo == "💰 PIX":
            chave = self.entry_pix.get()
            nome = self.entry_nome_pix.get().strip()
            valor = self.entry_valor_pix.get()
            valor = valor.replace(",", ".")
            if not valor:
                valor = 0.00
            pix = generate_simple_pix(
                fullname=nome,
                key=chave,
                city="Sao Paulo", 
                value=float(valor),
                mult_transaction=True
            )
            return str(pix)

        elif tipo == "📞 Contato":
            nome = self.entry_nome.get()
            tel = self.entry_tel.get()
            email = self.entry_email.get()
            vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{nome}\nTEL:{tel}\n"
            if email:
                vcard += f"EMAIL:{email}\n"
            vcard += "END:VCARD"
            return vcard
        
    def gerar_qr(self):
        if not self.validar_campos():
            return None
        data = self.montar_dado()
        if not data.strip():
            messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
            return None

        cor_rgb = hex_para_rgb(self.cor)
        fundo_rgb = hex_para_rgb(self.fundo)

        img = gerar_qrcode_personalizado(
            data=data,
            cor=cor_rgb,
            fundo=fundo_rgb,
            estilo=self.combo_estilo.get(),
            gradiente=self.var_gradiente.get(),
            caminho_logo=self.logo_path
        )

        return img
        
    def ver_previa(self):
        try:
            img = self.gerar_qr()
            if img is None:
                return

            img.thumbnail((220, 220))
            ctk_img = CTkImage(light_image=img, size=img.size)
            self.preview.configure(image=ctk_img, text="")
            self.preview.image = ctk_img
        except Exception as e:
            messagebox.showerror("Erro na prévia", str(e))

    def salvar_qr(self):
        try:
            img = self.gerar_qr()
            if img is None:
                return

            largura, altura = map(int, self.opcao_tamanho.get().split("x"))
            img = img.resize((largura, altura))

            salvar = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if salvar:
                img.save(salvar)
                messagebox.showinfo("Salvo", f"QR Code salvo em:\n{salvar}")
                self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro ao gerar QRCode", str(e))