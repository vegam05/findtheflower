from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='flowers/')  # Assuming you want to upload flower images
    classification = models.CharField(max_length=50, null=True, blank=True)  # Classification field for storing the predicted class

    def __str__(self):
        return self.name
