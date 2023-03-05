import requests


def get_images() -> None:
    # for index in range(20):
    #     i = index+1
    i = 20
    image_url = f"https://fakeimg.pl/25{i}x10{i}/"
    img_data = requests.get(image_url).content
    with open(f'images/post{i}.jpg', 'wb') as handler:
        handler.write(img_data)


if __name__ == "__main__":
    get_images()
