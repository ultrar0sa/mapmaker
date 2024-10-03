from turtle import Turtle

from tkinter import *
from tkinter import Tk, ttk, filedialog
import json
import tkinter
import os

PROJECT_NAME = "mapmakerprototype"
saveindex = 0
loadedFile = ""
currentBackgroundImage = ""

def change_background_image():
    global currentBackgroundImage
    imagePath = filedialog.askopenfile(initialdir="C:/Users/small/Desktop/projects/mapmaker/images")
    currentBackgroundImage = imagePath.name
    artist.screen.bgpic(imagePath.name)
    save_image(filedialog.askopenfile(initialdir="C:/Users/small/Desktop/projects/mapmaker/savedshapes"))

def draw_text(starting_x_coord, starting_y_coord, text, color="black"):
    artist.penup()
    artist.pencolor(color)
    artist.goto(starting_x_coord, starting_y_coord)
    artist.pendown()
    artist.write(text)
    artist.pencolor("black")


def draw_rectangle(starting_x_coord, starting_y_coord, width, height):
    artist.penup()
    artist.goto(starting_x_coord, starting_y_coord)
    artist.pendown()
    artist.begin_fill()
    count = 1
    while count <= 4:
        print(artist.position())
        if(count % 2 == 0):
            artist.forward(height)
            artist.right(90)
        else:
            artist.forward(width)
            artist.right(90)          
        count += 1
    artist.end_fill()

def load_file(*args):
    artist.clear()
    tkinter.Tk().withdraw()
    loadPath = filedialog.askopenfile(initialdir="C:/Users/small/Desktop/projects/mapmaker/savedshapes")
    print(loadPath.name)
    with open(loadPath.name, "r", encoding="utf-8") as file:
        loadedDict = json.load(file)
        print(str(loadedDict))
        for dict in loadedDict:
            if "backgroundImage" in dict:
                if dict["backgroundImage"] != "":
                    artist.screen.bgpic(dict["backgroundImage"])
            elif "rectHeight" in dict:
                rectHeight.set(dict["rectHeight"])
                rectWidth.set(dict["rectWidth"])
                rectXCoord.set(dict["rectXCoord"])
                rectYCoord.set(dict["rectYCoord"])
                draw_rectangle(rectXCoord.get(), rectYCoord.get(), rectWidth.get(), rectHeight.get())
            elif "text" in dict:
                draw_text(int(dict["textXCoord"]), int(dict["textYCoord"]), dict["text"], dict["textColor"])

def save_handler():
    print(shapeType.get())
    if shapeType.get() == "rectangle":
        save_rect()
    elif shapeType.get() == "text":
        save_text() 

def json_write(writeDict, save_file):
    root = []
    print(os.path.getsize(save_file.name))
    if os.path.getsize(save_file.name) == 0:
        root.append(writeDict)
        with open(save_file.name, mode='w') as f:
            f.write(json.dumps(root, indent=4))
            f.close()
    else:
        with open(save_file.name) as file:
            loadedFile = json.load(file)
            root = loadedFile
            root.append(writeDict)
            file.close()
            with open(save_file.name, mode='w') as f:
                f.write(json.dumps(root, indent=4))
                f.close()
    
def save_text():
    writeDict = {"text" : textInput.get(),
                 "textXCoord" : textXCoordInput.get(),
                 "textYCoord" : textYCoordInput.get(),
                 "textColor" : textColorCombobox.get()}
    save_file = filedialog.askopenfile(initialdir="savedshapes", defaultextension=".json")
    json_write(writeDict, save_file)
    

def save_image(save_file):
    writeDict = {"backgroundImage" : currentBackgroundImage}
    root = []
    if os.path.getsize(save_file.name) == 0:
        root.append(writeDict)
        with open(save_file.name, mode='w') as f:
            f.write(json.dumps(root, indent=4))
            f.close()
    else:
        with open(save_file.name) as file:
            loadedFile = json.load(file)
            root = loadedFile
            root.insert(0, writeDict)
            file.close()
            with open(save_file.name, mode='w') as f:
                f.write(json.dumps(root, indent=4))
                f.close()
    



def save_rect(*args):
    global saveindex
    print(args)
    writeDict = {"rectHeight" : rectHeightInput.get(),
        "rectWidth" : rectWidthInput.get(),
        "rectXCoord" : rectXCoordInput.get(),
        "rectYCoord" : rectYCoordInput.get()}
    save_file = filedialog.askopenfile(initialdir="C:/Users/small/Desktop/projects/mapmaker/savedshapes", defaultextension=".json")
    json_write(writeDict, save_file)
    # root = []
    # print(os.path.getsize(save_file.name))
    # if os.path.getsize(save_file.name) == 0:
    #     root.append(writeDict)
    #     with open(save_file.name, mode='w') as f:
    #         f.write(json.dumps(root, indent=4))
    #         f.close()
    # else:
    #     with open(save_file.name) as file:
    #         loadedFile = json.load(file)
    #         root = loadedFile
    #         root.append(writeDict)
    #         file.close()
    #         with open(save_file.name, mode='w') as f:
    #             f.write(json.dumps(root, indent=4))
    #             f.close()
    # save_image(save_file)
            
    

def add_to_canvas(*args):
    if shapeType.get() == "rectangle":
        print("drawing rectangle")
        rectHeight.set(rectHeightInput.get())
        rectWidth.set(rectWidthInput.get())
        rectXCoord.set(rectXCoordInput.get())
        rectYCoord.set(rectYCoordInput.get())
        draw_rectangle(rectXCoord.get(), rectYCoord.get(), rectWidth.get(), rectHeight.get())
    elif shapeType.get() == "text":
        print("writing text")
        text.set(textInput.get())
        textXCoord.set(textXCoordInput.get())
        textYCoord.set(textYCoordInput.get())
        draw_text(textXCoord.get(), textYCoord.get(), text.get(), textColorCombobox.get())
        
    

def clear_options():
    rectFrame.grid_forget()
    textFrame.grid_forget()

def create_options(*args):
    clear_options()
    shapeType.set(shapeTypeDropdown.get())
    match shapeType.get():
        case "rectangle":
            rectFrame.grid(column=1, row=1)
        case "text":
            textFrame.grid(column=1, row=1)
        case _:
            print("what the fuck")

artist = Turtle()
artistCanvas = artist.screen
artist.pensize(5)
artist.fillcolor("white")
artist.hideturtle()

makerRoot = Tk()
makerRoot.title("mapmaker presented by lcd soundsystem sponsored by bank of america")
makerRoot.geometry("600x400")
makerFrame = ttk.Frame(makerRoot)
makerFrame.grid(column=0, row=0, sticky=(N, S, E, W))

rectFrame = ttk.Frame(makerFrame)
rectHeightLabel = ttk.Label(rectFrame, text="rectangle height")
rectWidthLabel = ttk.Label(rectFrame, text="rectangle width")
rectHeightInput = ttk.Entry(rectFrame)
rectWidthInput = ttk.Entry(rectFrame)
rectXCoordLabel = ttk.Label(rectFrame, text="starting x coord")
rectYCoordLabel = ttk.Label(rectFrame, text="starting y coord")
rectXCoordInput = ttk.Entry(rectFrame)
rectYCoordInput = ttk.Entry(rectFrame)
rectHeightLabel.grid(column=1, row=0, sticky=N)
rectHeightInput.grid(column=2, row=0, sticky=N)
rectWidthLabel.grid(column=1, row=1, sticky=N)
rectWidthInput.grid(column=2, row=1, sticky=N)
rectXCoordLabel.grid(column=1, row=2, sticky=N)
rectXCoordInput.grid(column=2, row=2, sticky=N)
rectYCoordLabel.grid(column=1, row=3, sticky=N)
rectYCoordInput.grid(column=2, row=3, sticky=N)


# rectHeightLabel.grid_forget()
# rectWidthLabel.grid_forget()

textFrame = ttk.Frame(makerFrame)
textInputLabel = ttk.Label(textFrame, text="text")
textInput = ttk.Entry(textFrame)
textXCoordLabel = ttk.Label(textFrame, text="starting x coord")
textYCoordLabel = ttk.Label(textFrame, text="starting y coord")
textXCoordInput = ttk.Entry(textFrame)
textYCoordInput = ttk.Entry(textFrame)
textColorLabel = ttk.Label(textFrame, text="color")
textColorCombobox = ttk.Combobox(textFrame, values=("black", "white", "gray", "pink", "green", "blue"))
textInputLabel.grid(column=1, row=0,sticky=N)
textInput.grid(column=2, row=0,sticky=N)
textXCoordLabel.grid(column=1, row=1, sticky=N)
textXCoordInput.grid(column=2, row=1, sticky=N)
textYCoordLabel.grid(column=1, row=2, sticky=N)
textYCoordInput.grid(column=2, row=2, sticky=N)
textColorLabel.grid(column=1, row=3, sticky=N)
textColorCombobox.grid(column=2, row=3, sticky=N)





shapeType = StringVar()
rectHeight = IntVar()
rectWidth = IntVar()
rectXCoord = IntVar()
rectYCoord = IntVar()
text = StringVar()
textXCoord = IntVar()
textYCoord = IntVar()
shapeTypeDropdown = ttk.Combobox(makerFrame, textvariable=shapeType, values=("rectangle", "text"))
shapeTypeDropdown.state(["readonly"])
shapeTypeDropdown.grid(column=0, row=0, sticky=W)
shapeTypeDropdown.bind("<<ComboboxSelected>>", create_options)

submitButton = ttk.Button(makerRoot, text="add to canvas", command=add_to_canvas)
submitButton.place(x=510, y=360)

saveButton = ttk.Button(makerRoot, text="save", command=save_handler)
saveButton.place(x=410, y=360)

loadButton = ttk.Button(makerRoot, text="load", command=load_file)
loadButton.place(x=310, y=360)

clearButton = ttk.Button(makerRoot, text="clear", command=artist.clear)
clearButton.place(x=210, y=360)

changeBackgroundButton = ttk.Button(makerRoot, text="change img", command=change_background_image)
changeBackgroundButton.place(x=110, y=360)

col_count, row_count = makerFrame.grid_size()

for col in range(col_count):
    makerFrame.grid_columnconfigure(col, minsize=20)

for row in range(row_count):
    makerFrame.grid_rowconfigure(row, minsize=20)
# style = ttk.Style()
# style.configure(style="TFrame", background="white")
# style.configure(style="Frame1.TFrame", background="pink")
#topThing = ttk.Frame(makerFrame, style="Frame1.TFrame")

#topThing.grid(column=2, row=1, sticky=N)
makerRoot.mainloop()