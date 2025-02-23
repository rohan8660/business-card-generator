from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import qrcode
import base64
import io
import vobject

app = Flask(__name__)

# Text position constants (as percentage of template dimensions)
TEXT_X_OFFSET = 0.15  # 15% from left
NAME_Y_POS = 0.30    # 15% from top
PHONE_Y_POS = 0.45   # 40% from top
EMAIL_Y_POS = 0.55   # 65% from top
QR_X_POS = 0.61      # 75% from left
QR_Y_POS = 0.36      # 30% from top

def generate_vcard(name, email, phone):
    vcard = vobject.vCard()
    vcard.add('fn').value = name
    vcard.add('email').value = email
    vcard.add('tel').value = phone
    return vcard.serialize()

def generate_qr_code(vcard_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def create_business_card(name, email, phone, debug=False):
    # Load the Cable Australia template
    template = Image.open('static/template.png')
    draw = ImageDraw.Draw(template)
    
    try:
        # Increase font size
        font = ImageFont.truetype("Arial", 25)
    except IOError:
        font = ImageFont.load_default()
    
    # Get template dimensions
    width, height = template.size
    
    # Adjust x_offset slightly to accommodate larger text
    x_offset = int(width * 0.15)  # Increased from 0.15 to 0.18 to give more space
    
    # Vertical positions might need slight adjustments for larger text
    name_y = int(height * 0.30)
    phone_y = int(height * 0.45)
    email_y = int(height * 0.60)
    
    # Text color matching template's blue
    text_color = 'rgb(0,28,84)'  # Dark blue
    
    # Add text with proper alignment
    # Get text size for centering if needed
    name_bbox = draw.textbbox((0, 0), name, font=font)
    email_bbox = draw.textbbox((0, 0), email, font=font)
    phone_bbox = draw.textbbox((0, 0), phone, font=font)
    
    # Draw text aligned with icons, adjusted for larger font
    draw.text((x_offset, name_y - name_bbox[3]/2), name, font=font, fill=text_color)
    draw.text((x_offset, phone_y - phone_bbox[3]/2), phone, font=font, fill=text_color)
    draw.text((x_offset, email_y - email_bbox[3]/2), email, font=font, fill=text_color)
    
    # QR code placement
    qr_size = int(height * 0.4)  # QR code size 40% of height
    vcard_data = generate_vcard(name, email, phone)
    qr_image = generate_qr_code(vcard_data).resize((qr_size, qr_size))
    
    # Position QR code in the white space
    qr_x = int(width * QR_X_POS)  # 75% from left
    qr_y = int(height * QR_Y_POS)  # 30% from top
    
    # Add white background for QR
    white_bg = Image.new('RGB', (qr_size + 20, qr_size + 20), 'white')
    template.paste(white_bg, (qr_x - 10, qr_y - 10))
    template.paste(qr_image, (qr_x, qr_y))
    
    if debug:
        # Draw guidelines
        debug_color = 'rgba(255, 0, 0, 128)'  # Semi-transparent red
        
        # Draw vertical and horizontal center lines
        draw.line([(width/2, 0), (width/2, height)], fill=debug_color, width=1)
        draw.line([(0, height/2), (width, height/2)], fill=debug_color, width=1)
        
        # Draw text anchor points
        point_size = 5
        for y in [name_y, phone_y, email_y]:
            draw.ellipse([(x_offset-point_size, y-point_size), 
                         (x_offset+point_size, y+point_size)], 
                        fill=debug_color)
    
    return template

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_card():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    debug = request.form.get('debug', False)
    
    # Generate the business card
    card = create_business_card(name, email, phone, debug=debug)
    
    # Convert the image to base64 for displaying in HTML
    buffered = io.BytesIO()
    card.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('index.html', card_image=img_str)

if __name__ == '__main__':
    app.run(debug=True) 