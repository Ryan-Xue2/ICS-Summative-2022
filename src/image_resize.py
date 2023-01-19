from PIL import Image
image_name = input('image name: ')
image = Image.open('images/'+image_name)
# image = image.resize((50, 50))
image = image.resize((1600, 500))
image.save('images/'+image_name)