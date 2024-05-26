import fitz  # PyMuPDF
import base64
from io import BytesIO
from PIL import Image


def convert_pdf_to_images(pdf_file, image_format="png", dpi=300):
    if not pdf_file:
        print("No PDF file provided.")
        return []

    # Open the PDF file from the uploaded file-like object
    pdf_bytes = pdf_file.read()  # Read the file-like object into bytes
    doc = fitz.open("pdf", pdf_bytes)  # Open the PDF from bytes

    base64_images = []

    for page_number in range(len(doc)):
        # Get the page
        page = doc.load_page(page_number)
        
        # Specify zoom factor based on DPI. Default PDF DPI is 72.
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        
        # Get the pixmap of the page with specified DPI (rasterized image)
        pix = page.get_pixmap(matrix=matrix)
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save the image to a BytesIO object
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=image_format.upper())
        
        # Encode the image to base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        base64_images.append(img_base64)
    
    # Close the PDF after processing
    doc.close()
    print(f"All pages have been converted to {image_format} at {dpi} DPI.")
    
    return base64_images