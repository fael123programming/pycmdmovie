from PIL import Image
import os, time, cv2


ASCII_CHARS = ' .:=+*#%@'


def _scale_image(image, new_width):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width / 2)
    new_image = image.resize((new_width, new_height))
    return new_image


def _convert_to_grayscale(image):
    return image.convert("L")


def _map_pixels_to_ascii(image, range_width, negative):
    ascii_chars = ASCII_CHARS
    if negative:
        ascii_chars = ascii_chars[::-1]
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        pixel_index = min(int(pixel_value // range_width), len(ascii_chars) - 1)
        ascii_str += ascii_chars[pixel_index]
    return ascii_str


def _convert_image_to_ascii(image_path, new_width, range_width, negative):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return
    image = _convert_to_grayscale(image)
    image = _scale_image(image, new_width)
    ascii_str = _map_pixels_to_ascii(image, range_width, negative)
    ascii_lines = [ascii_str[index:index+new_width] for index in range(0, len(ascii_str), new_width)]
    ascii_art = "\n".join(ascii_lines)
    return ascii_art


def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def _extract_frames(video_path):
    folder = video_path.split('.')[0] + '_movie'
    if not os.path.exists(folder):
        os.makedirs(folder)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Error: Unable to open video.')
        return
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(folder, f'frame_{frame_count:04d}.png')
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()
    print(f'Frames extracted: {frame_count}')


def display_img(img_path, *, img_width=500, range_width=25, negative=False):
    ascii_art = _convert_image_to_ascii(img_path, img_width, range_width, negative)
    print(ascii_art)


def display_imgs(imgs_dir, *, img_width=500, range_width=25, negative=False, delay=.1, clear=False, infinite=True):
    valid_extensions = ('jpg', 'jpeg', 'png')
    imgs = [img for img in os.listdir(imgs_dir) if img.split('.')[1] in valid_extensions]
    if len(imgs) == 0:
        print(f'No images found. Please consider the following image extensions: {valid_extensions}')
        return
    while True:
        for img in imgs:
            ascii_img = _convert_image_to_ascii(os.path.join(imgs_dir, img), img_width, range_width, negative)
            print(ascii_img)
            time.sleep(delay)
            if clear:
                _clear()
        if not infinite:
            break


def display_video(video_path, *, video_width=500, range_width=25, negative=False, delay=.1, clear=False, infinite=True):
    dir = video_path.split('.')[0] + '_movie'
    if not os.path.exists(dir):
        _extract_frames(video_path)
    display_imgs(dir, img_width=video_width, range_width=range_width, negative=negative, delay=delay, clear=clear, infinite=infinite)
