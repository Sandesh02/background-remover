from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageChops
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the file from the POST request
    file = request.files['image']

    # Save the file to the uploads folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # Read the image
    img = Image.open(file)

    # Remove the background from the image
    img_no_bg = remove_background(img)

    # Save the image to the uploads folder
    img_no_bg_path = os.path.join(app.config['UPLOAD_FOLDER'], 'no_bg_' + file.filename)
    img_no_bg.save(img_no_bg_path)

    return redirect(url_for('uploaded_file', filename=img_no_bg_path))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('result.html', img_path=filename)

def remove_background(image):
    # Convert the image to RGBA
    rgba_image = image.convert('RGBA')

    # Get the alpha channel
    alpha = rgba_image.split()[-1]

    # Create a mask with the alpha channel
    mask = Image.new('L', rgba_image.size, 0)
    mask.paste(alpha, alpha)

    # Invert the mask
    inverted_mask = ImageChops.invert(mask)

    # Apply the inverted mask to the image
    image_no_bg = Image.new("RGBA", rgba_image.size, (255, 255, 255, 0))
    image_no_bg.paste(rgba_image, mask=inverted_mask)

    # Set the background to white
    image_no_bg = image_no_bg.convert('RGB')
    image_no_bg = Image.new("RGB", image_no_bg.size, (255, 255, 255))
    image_no_bg.paste(image_no_bg, mask=inverted_mask)

    return image_no_bg

if __name__ == '__main__':
    app.run(debug=True)
