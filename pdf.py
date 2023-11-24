
from os import path, getcwd
from random import randbytes
from fpdf import FPDF



def saveToPDF(_content = '', filename: str = ''):
    
    pdf_directory = path.join(getcwd(), 'audio_pdfs')
    filename = ( randbytes(8).hex() if filename == '' else filename ) + ".pdf"
    filepath = path.join(pdf_directory, filename)

    pdf = FPDF()
    pdf.add_font("Roboto", style="", fname="font/Roboto-Regular.ttf")
    pdf.add_font("Roboto", style="b", fname="font/Roboto-Bold.ttf")
    pdf.add_font("Roboto", style="i", fname="font/Roboto-Italic.ttf")
    pdf.add_font("Roboto", style="bi", fname="font/Roboto-BoldItalic.ttf")

    pdf.add_page()
    pdf.set_font('Roboto', size=16, style='B')
    pdf.cell(text="Ajayi Micheal Adekunle", center=True)
    pdf.ln()
    pdf.ln()
    pdf.set_font('Roboto', size=12)

    if (_content == ''):
        pdf.cell(text="Your provided content goes here")
        pdf.output(filepath)
        return filepath

    pdf.write(txt=_content)
    pdf.output(filepath)

    return filename;



if __name__ == '__main__':
    saveToPDF(_content = "qwertyuioplkjhgfdsazxcvbnm")
