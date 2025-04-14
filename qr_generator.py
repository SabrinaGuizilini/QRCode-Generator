from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask

def gerar_qrcode_personalizado(data, cor, fundo, estilo, gradiente, caminho_logo):
    """
    Gera um QR Code personalizado com opções de estilo, cor sólida ou gradiente e logotipo central.
    
    Parâmetros:
    - data: Dados a serem codificados no QR Code.
    - cor: Cor do QR Code (frente).
    - fundo: Cor de fundo do QR Code.
    - estilo: Estilo dos módulos (Quadrado, Arredondado, Círculo).
    - gradiente: Booleano indicando se será aplicado gradiente.
    - caminho_logo: Caminho para o logotipo que será inserido no centro do QR Code (opcional).
    
    Retorna:
    - Imagem PIL do QR Code personalizado.
    """

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    modulo = {
        "Quadrado": SquareModuleDrawer(),
        "Arredondado": RoundedModuleDrawer(),
        "Círculo": CircleModuleDrawer()
    }.get(estilo, SquareModuleDrawer())

    color_mask = RadialGradiantColorMask(center_color=fundo, edge_color=cor) if gradiente else SolidFillColorMask(front_color=cor, back_color=fundo)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=modulo,
        color_mask=color_mask
    ).convert("RGBA")

    if caminho_logo:
        logo = Image.open(caminho_logo).convert("RGBA")
        basewidth = img.size[0] // 4
        wpercent = basewidth / float(logo.size[0])
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, logo)

    return img