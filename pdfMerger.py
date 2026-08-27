import PyPDF2

merger=PyPDF2.PdfMerger()
pdf_files=["Peaceful Motivation Story.pdf","The_Mountain_and_the_Climber.pdf"]

for pdf_file in pdf_files:
    pdf_file=open(pdf_file,"rb")
    pdfreader=PyPDF2.PdfReader(pdf_file)

    merger.append(pdfreader)

pdf_file.close()
merger.write("merged_pdf.pdf")