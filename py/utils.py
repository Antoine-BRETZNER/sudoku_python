import cv2
import matplotlib.pyplot as plt

def plot_image(image, title=None):
    """
    Affiche une image en utilisant matplotlib.

    :param image: Image chargée avec OpenCV.
    :param title: Titre optionnel pour l'image.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    if title:
        plt.title(title)
    plt.axis('off')
    plt.show()