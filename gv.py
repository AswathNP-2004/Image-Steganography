from tkinter import *
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from stegano import lsb  # pip install stegano

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=self.text, justify='left',
                      background="#ffffe0", relief='solid', borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def create_tooltip(widget, text):
    ToolTip(widget, text)

root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#add8e6")

def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File', 
                                          filetype=(("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All Files", "*.*")))
    try:
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img, width=250, height=250)
        lbl.image = img
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open image file: {e}")

def Hide():
    try:
        message = text1.get(1.0, END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to hide.")
            return
        global secret
        secret = lsb.hide(str(filename), message)
        messagebox.showinfo("Success", "Message hidden successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide message: {e}")

def show():
    password = "mypassword"  # Predefined password
    user_password = simpledialog.askstring("Password", "Enter password:", show='*')
    
    if user_password == password:
        try:
            clear_message = lsb.reveal(filename)
            if clear_message:
                text1.delete(1.0, END)
                text1.insert(END, clear_message)
            else:
                messagebox.showinfo("No Message", "No hidden message found in the image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reveal message: {e}")
    else:
        messagebox.showerror("Error", "Incorrect password!")

def save():
    try:
        if secret:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
            if save_path:
                secret.save(save_path)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showwarning("Warning", "No hidden message to save.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

# Icon
image_icon = PhotoImage(file="logo1.png")
root.iconphoto(False, image_icon)
# Logo
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#add8e6").place(x=10, y=0)
Label(root, text="Encryption                        Decryption", fg="blue", font="arial 20 bold").place(x=100, y=20)
# First Frame
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)
lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame
frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="arial 15", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

btn_open_image = Button(frame3, text="Open Image", width=12, height=2, font="arial 12 bold", command=showimage)
btn_open_image.place(x=20, y=30)
create_tooltip(btn_open_image, "Select an image file to hide a message")

btn_save_image = Button(frame3, text="Save Image", width=12, height=2, font="arial 12 bold", command=save)
btn_save_image.place(x=180, y=30)
create_tooltip(btn_save_image, "Save the image with the hidden message")

Label(frame3, text="Picture Image, Photo file", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth Frame
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

btn_hide_data = Button(frame4, text="Hide Data", width=12, height=2, font="arial 12 bold", command=Hide)
btn_hide_data.place(x=20, y=30)
create_tooltip(btn_hide_data, "Hide the text message in the selected image")

btn_show_data = Button(frame4, text="Show Data", width=12, height=2, font="arial 12 bold", command=show)
btn_show_data.place(x=180, y=30)
create_tooltip(btn_show_data, "Reveal the hidden message from the selected image")

Label(frame4, text="Picture Image, Photo file", bg="#2f4155", fg="yellow").place(x=20, y=5)
root.mainloop()
