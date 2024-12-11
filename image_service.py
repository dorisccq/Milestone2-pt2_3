import torch
from diffusers.utils import load_image
from diffusers import FluxControlNetModel
from diffusers.pipelines import FluxControlNetPipeline
from flask import Flask, request, send_file,jsonify
from PIL import Image
import io

# Load the pipeline
controlnet = FluxControlNetModel.from_pretrained(
    "jasperai/Flux.1-dev-Controlnet-Upscaler",
    torch_dtype=torch.bfloat16
)
pipe = FluxControlNetPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    controlnet=controlnet,
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    # Get the uploaded image
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    if file:
        try:
            # Get parameters from form data
            prompt = request.form.get('prompt', '')
            controlnet_conditioning_scale = float(request.form.get('controlnet_conditioning_scale', 0.6))
            num_inference_steps = int(request.form.get('num_inference_steps', 28))
            guidance_scale = float(request.form.get('guidance_scale', 3.5))
            
            # Open and process the image
            input_image = Image.open(file)
            # Resize the image x4
            w, h = input_image.size
            resized_image = input_image.resize((w * 4, h * 4))
            # Generate the image
            output_image = pipe(
                prompt=prompt, 
                control_image=resized_image,
                controlnet_conditioning_scale=controlnet_conditioning_scale,
                num_inference_steps=num_inference_steps, 
                guidance_scale=guidance_scale,
                height=resized_image.size[1],
                width=resized_image.size[0]
            ).images[0]
            # Save the output image to a byte stream
            img_byte_arr = io.BytesIO()
            output_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            # Return the image as a response
            return send_file(
                io.BytesIO(img_byte_arr),
                mimetype='image/png',
                as_attachment=False,
                download_name='output.png'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)