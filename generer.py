from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

class FacturePDF(FPDF):
    def header(self):
        self.image("logo.png", x=10, y=8, w=40)
        self.set_font("Arial", "B", 14)
        self.set_xy(10, 50)
        self.cell(0, 8, "HAFIANE MOUNIR IMPORT", align="L")

    def footer(self):
        self.set_y(-40)
        self.set_font("Arial", "", 9)
        self.cell(0, 8, "AUTORISATION IMPORT : 2026/04588/و ت خ ت ص", align="L")
        try:
            self.image("mon_qr.png", x=10, y=245, w=35)
        except:
            pass

def creer_facture(num, nom, adr, ville, tel, articles, date_v="", ent_nom="", ent_adr="", ent_wa="", ent_imm="", ent_tel=""):
    pdf = FacturePDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 28)
    pdf.set_xy(110, 15)
    pdf.cell(90, 20, "FACTURE", align="R")

    pdf.set_font("Arial", "", 11)
    pdf.set_xy(10, 65)
    pdf.cell(60, 8, f"DATE : {date_v or '__ / __ / ____'}")
    pdf.cell(60, 8, "ÉCHÉANCE : __ / __ / ____")

    pdf.set_font("Arial", "B", 14)
    pdf.set_xy(140, 65)
    pdf.cell(60, 8, f"FACTURE N° : {num}", align="R")

    # ÉMETTEUR
    pdf.set_font("Arial", "B", 12)
    pdf.set_xy(10, 80)
    pdf.cell(90, 8, "ÉMETTEUR :")
    pdf.set_font("Arial", "", 10)
    pdf.set_xy(10, 88)
    pdf.multi_cell(90, 5, f"HAFIANE MOUNIR IMPORT\nCité Kababe Ramdane, 43013 - Mila\nTél/WhatsApp: {ent_tel or ent_wa}\nImmat: {ent_imm}")

    # DESTINATAIRE
    pdf.set_font("Arial", "B", 12)
    pdf.set_xy(110, 80)
    pdf.cell(90, 8, "DESTINATAIRE :")
    pdf.set_font("Arial", "", 10)
    pdf.set_xy(110, 88)
    pdf.multi_cell(90, 5, f"{str(nom).upper()}\n{adr}\n{ville}\nTél: {tel}")

    # TABLEAU
    pdf.set_xy(10, 125)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(100, 10, "Description", border=1)
    pdf.cell(30, 10, "Prix Unitaire", border=1, align="C")
    pdf.cell(25, 10, "Quantité", border=1, align="C")
    pdf.cell(35, 10, "Total", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    total = 0
    pdf.set_font("Arial", "", 10)
    for art in articles:
        pu = float(art.get('prix', 0))
        qte = float(art.get('qte', 0))
        ligne = pu * qte
        total += ligne
        pdf.cell(100, 10, art.get('desc', ''), border=1)
        pdf.cell(30, 10, f"{pu:,.2f}", border=1, align="C")
        pdf.cell(25, 10, f"{qte}", border=1, align="C")
        pdf.cell(35, 10, f"{ligne:,.2f}", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Arial", "B", 16)
    pdf.set_xy(140, 220)
    pdf.cell(60, 12, f"TOTAL TTC : {total:,.2f} DA", align="R")

    pdf.output(f"Facture_REF-{num}.pdf")
    return f"Facture_REF-{num}.pdf"