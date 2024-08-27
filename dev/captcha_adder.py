from book_request import auth
import requests,json
import base64
from io import BytesIO
from tkinter import Tk, Label,Button,Entry,messagebox
from PIL import Image, ImageTk

user_data = {
    "username": "larisa.tsyrenowa@yandex.ru",
    "password": "1tW&uZez3hqG",
    "target_truck": "O481EB75",
    "target_trunk": "AE069775",
    "driver":{
        "email": "larisa.tsyrenowa@yandex.ru",
        "phone": "89145045696"
    }
}

current_image = None

def get_captcha(headers,root):
        def add_result(captcha):
            result = entr.get()
            captcha["result"] = result
            try:
                with open("data/captchas.json","r",encoding="utf-8") as file:
                    data = json.load(file)               
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            data.append(captcha)
            with open("data/captchas.json","w") as file:
                json.dump(data,file,ensure_ascii=False, indent=4)
            next_image()
        def next_image():
            global current_image,entr
            
            resp = requests.get(url="https://srv-gg.ru/api/captcha", headers=headers)
            captcha = resp.json()
            entr = Entry(root)
            entr.place(x=450,y=300)
            add = Button(root,text="add",command=lambda: add_result(captcha))
            add.place(x=100,y=400)
            if resp.status_code == 200:
                base64_str = captcha.get("captcha")

                if base64_str.startswith('data:image'):
                    base64_str = base64_str.split(',')[1]

                image_data = base64.b64decode(base64_str)
                image_bytes = BytesIO(image_data)
                image = Image.open(image_bytes)

                current_image = ImageTk.PhotoImage(image)

                label.config(image=current_image)
                label.image = current_image


            else:
                messagebox.showerror("error",resp.text)

        

        button = Button(root, text="Следующая", command=next_image)
        button.place(x=450,y=500)

        label = Label(root)
        label.pack()

        next_image()
        

def main(headers):
    root = Tk()
    root.geometry("900x600")

    start = Button(root,text="start",command=lambda: get_captcha(headers,root))
    start.place(x=450,y=560)


    root.mainloop()

if __name__ == "__main__":
    token,ua,cookies = auth(user_data["username"],user_data["password"])
    headers = {
    "Authorization": "Bearer " + token,
    "User-Agent": ua,
    "Cookie": cookies,
    "Referer": "https://srv-gg.ru/booking-process"
    }
    main(headers)

