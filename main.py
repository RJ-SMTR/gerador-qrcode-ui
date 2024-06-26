from pathlib import Path

import io
import zipfile

import streamlit as st
import jinja2
import qrcode

st.set_page_config(page_title="Gerador de QRCode - SMTR", page_icon='./favicon.ico')

CHARSET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
LENGTH: int = 4
OUTPUT_DIR: Path = Path("output")
URL_TEMPLATE: jinja2.Template = jinja2.Template(
    "https://mobilidade.rio/{{ code }}")

def generate_url(code: str) -> str:
    return URL_TEMPLATE.render(code=code)


def generate_qr(code: str) -> str:
    img = qrcode.make(generate_url(code))
    # img.save(OUTPUT_DIR / f"{code}.png")

def gera_qrcodes(lista_codigos):
    lista_imagens = []
    for codigo in lista_codigos:
        img_byte_arr = io.BytesIO()
        img = qrcode.make(generate_url(codigo))
        img.save(img_byte_arr, format='PNG')
        lista_imagens.append(img_byte_arr)
    return lista_imagens

def get_zipfile(codigos):
    lista_codigos = list(filter(None, codigos.split(',')))
    lista_imagens = gera_qrcodes(lista_codigos)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
        for codigo, imagem in zip(lista_codigos, lista_imagens):
            zip_file.writestr(f'{codigo}.png', imagem.getvalue())
    return zip_buffer.getvalue()
        
def main():
    codigos = st.text_area('Preencha os códigos que quer gerar aqui separados por vírgula:', placeholder='https://mobilidade.rio/,https://www.google.com/')
    col1, col2= st.columns([1,1])
    with col1:
        # st.button('Gerar QRCodes!')
        if st.button('Gerar QRCodes na página'):
            if codigos:
                lista_codigos = list(filter(None, codigos.split(',')))
                lista_imagens = gera_qrcodes(lista_codigos)
                for codigo, imagem in zip(lista_codigos, lista_imagens):
                    st.image(image=imagem.getvalue(), caption=codigo)             
            else:
                st.text('Nenhum código para ser gerado')

    with col2:
        st.download_button('Baixar em formato .zip', file_name='qrcodes.zip', data=get_zipfile(codigos), disabled=True if not codigos else False)

if __name__ == "__main__":   
    main()
