'''from wand.image import Image as wi
pdf = wi(filename="sample.pdf",resolution=300)
pdfImage = pdf.convert("jpeg")
i=1
for img in pdfImage.sequence:
    page = wi(image=img)
    page.save(filename=str(i)+".jpg")
    i=+1'''
import cv2
import reduce_noise  
from os.path import join,exists  
from os import makedirs
import os 
path=os.getcwd()   
from pdf2image import convert_from_path    
def convert_img(filename,pdf_name):
    image_path=join(path,pdf_name)
    if not exists(image_path):
        makedirs(image_path,exist_ok=True)
    pages = convert_from_path(filename, 500)
    for i,page in enumerate(pages):
        page.save(join(image_path,str(i)+'_.jpg'), 'JPEG')
    return image_path

from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger
def create_pdf(pdf_name,page_num,string):
    folder_name=pdf_name+'_pdf'
    pdf_path=join(path,folder_name)
    if not exists(pdf_path):
        makedirs(pdf_path,exist_ok=True)
    text=string.split("\n")
    file_name=os.path.join(pdf_path,str(page_num)+'.pdf')
    my_canvas=canvas.Canvas(file_name)
    textobject = my_canvas.beginText()
    textobject.setTextOrigin(10, 800)
    for i in text:
        textobject.textLine(text=i)
    my_canvas.drawText(textobject)
    my_canvas.save()
    return file_name

def merge_pdf(array):
    new_file=os.path.join(path,"result.pdf")
    merger = PdfFileMerger()
    for i,pdf in enumerate(array):
        #merger.merge(position=i,fileobj=pdf)
        merger.append(pdf)
        #PyPDF2.pdfcat(merger, pdf)
    merger.write(new_file)
    merger.close()
    return new_file        
        
def pdf_to_textpdf(file_path,pdf_name):
    image_folder_path=convert_img(file_path,pdf_name)
    images=os.listdir(image_folder_path)
    lst=[]
    for image in images:
        page_num=image.split(".")[0]
        image_path=os.path.join(image_folder_path,image)
        image=cv2.imread(image_path,0)
        string=reduce_noise.fetch_string(image)
        lst.append(create_pdf(pdf_name,page_num,string))
    output_path=merge_pdf(lst[::-1])
    return output_path

output_path=pdf_to_textpdf('sample.pdf','sample')
        
        
    
    
    

        
        

