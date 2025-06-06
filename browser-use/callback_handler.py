import io

from PIL import Image, ImageDraw

import sixel 

global __prev_image
__prev_image = None


def draw_image(image, x, y, radius=10, color=(255, 0, 0), width=4, enlarge_level=2):
    global __prev_image

    image = Image.open(io.BytesIO(image))
    draw = ImageDraw.Draw(image)

    for i in range(1, enlarge_level + 1):
        draw.circle([x, y], radius=radius * i, outline=color, width=width)

    return image


def message_callback_handler(**kwargs):
    global __prev_image
    # ANSI color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
    
    if "message" in kwargs:
        
        for content in kwargs["message"]["content"]:
            if "text" in content:
                if kwargs["message"]["role"] == "assistant":
                    print(f"\n{BOLD}{GREEN}🌟 Agent:{END}\n")
                elif kwargs["message"]["role"] == "user":
                    print(f"\n{BOLD}{BLUE}👤 User:{END}\n")
                print(f"{content['text']}")
            elif "toolUse" in content:
                print(f"\n{BOLD}{YELLOW}🔧 Tool Used: {content['toolUse']['name']}{END}")
                if content['toolUse']['input']:
                    print(content['toolUse']['input'])
                    if __prev_image and "x" in content['toolUse']['input'] and "y" in content['toolUse']['input']:
                        sixel.display(draw_image(__prev_image, content['toolUse']['input']['x'], content['toolUse']['input']['y']))
            elif "toolResult" in content:
                status = content["toolResult"]["status"]
                status_color = GREEN if status == "success" else RED
                print(f"\n{BOLD}{MAGENTA}📊 Tool Result ({status_color}{status}{MAGENTA}):{END}")
                
                for result_content in content["toolResult"]["content"]:
                    if "image" in result_content:
                        print(f"{CYAN}📷 Displaying image:{END}")
                        __prev_image = result_content["image"]["source"]["bytes"]
                        sixel.display(result_content["image"]["source"]["bytes"])
                    elif "text" in result_content:
                        print(f"{result_content['text']}")
                    else:
                        print(f"{YELLOW}Other content:{END} {result_content}")
            else:
                pass
