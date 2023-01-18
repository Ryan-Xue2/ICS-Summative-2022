from PIL import Image
image_name = input('image name: ')
image = Image.open(image_name)
image.resize((50, 50))
image.save()