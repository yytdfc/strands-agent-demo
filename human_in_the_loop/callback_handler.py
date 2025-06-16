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
                user_input = input("⚠️ Please confirm to use the tool ⚠️  (y/N): ")
                if user_input.lower() != "y":
                    content["text"] =  f"Tool {content['toolUse']['name']} was not used."
                    content.pop("toolUse")

            elif "toolResult" in content:
                status = content["toolResult"]["status"]
                status_color = GREEN if status == "success" else RED
                print(f"\n{BOLD}{MAGENTA}📊 Tool Result ({status_color}{status}{MAGENTA}):{END}")
                
                for result_content in content["toolResult"]["content"]:
                    if "image" in result_content:
                        print(f"{CYAN}📷 Displaying image:{END}")
                    elif "text" in result_content:
                        print(f"{result_content['text']}")
                    else:
                        print(f"{YELLOW}Other content:{END} {result_content}")
            else:
                pass
