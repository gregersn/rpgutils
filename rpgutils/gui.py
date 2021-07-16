import PySimpleGUI as sg

layout = [[sg.Text("RPGUtils")],
          [sg.InputText()],
          [sg.Submit(), sg.Cancel()]]


window = sg.Window("RPG Utils", layout)


def showgui():
    event, values = window.read()
    window.close()
    print(values)
