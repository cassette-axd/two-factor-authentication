from tkinter import *
import windows

root = Tk()
root.title("Two Factor Authentication")

def main():
    windows.LoginWindow(root)


# This will be true when were run this file directly only
if __name__ == "__main__":
    main()

# start the GUI
root.mainloop()