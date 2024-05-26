
import tensorflow as tf
import numpy as np
from PIL import Image
from django.shortcuts import render
from .forms import FlowerForm
from .models import Flower
from keras.models import load_model

# Load the TensorFlow SavedModel
model_path = "classifier_model/findtheflower.keras"
model = load_model(model_path)

# Define your class names
CLASS_NAMES = ['Damask Rose', 'Echeveria flower', 'Mirabilis Jalapa', 'Rain Lily', 'Zinnia Elegans']

def classify_flower(image):
    # Preprocess the image
    image = image.resize((224, 224))  # Resize image to match model input size
    image_array = np.array(image) / 255.0   # Normalize pixel values to [0, 1]
    input_tensor = np.expand_dims(image_array, axis=0).astype(np.float32)  # Add batch dimension

    # Perform inference
    output = model(input_tensor)

    # Get the predicted class index
    predicted_class_index = np.argmax(output, axis=-1)[0]
    
    # Map the predicted class index to the class name
    predicted_class = CLASS_NAMES[predicted_class_index]

    return predicted_class

# Define a view to handle image uploads
# Define a view to handle image uploads
def upload_image(request):
    if request.method == 'POST':
        form = FlowerForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image to the database
            flower = form.save()

            # Perform classification on the uploaded image
            image_path = flower.image.path
            image = Image.open(image_path).convert('RGB')
            predicted_class = classify_flower(image)

            # Update the flower object with the classification result
            flower.classification = predicted_class
            flower.save()

            # Redirect to the result page with the flower object ID
            return render(request, 'result.html', {'flower': flower})
    else:
        form = FlowerForm()
    return render(request, 'upload.html', {'form': form})


# Define a view to display the classification result
def result_page(request):
    if request.method == 'GET':
        flower_id = request.GET.get('flower_id')
        if flower_id:
            # Retrieve the flower object from the database
            try:
                flower = Flower.objects.get(pk=flower_id)
            except Flower.DoesNotExist:
                flower = None
            return render(request, 'result.html', {'flower': flower})
    # Redirect to the upload page if flower_id is not provided or if the request method is not GET
    return render(request, 'upload.html', {'form': FlowerForm()})