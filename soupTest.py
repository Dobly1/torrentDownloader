import os.path
import tkinter
from tkinter import *
from tkinter import ttk

import urllib3
from bs4 import BeautifulSoup
from qbittorrent import Client


def string_stop(inputString, startCharacter, endCharacter):
    for i in range(len(inputString) - 1):
        if (inputString[i] == str(startCharacter) and inputString[i + 1] == str(endCharacter)):
            return i


def pirates_bay_scraper(myURL):
    try:
        http = urllib3.PoolManager()
        print(myURL)
        response = http.request('GET', myURL)
        soup = BeautifulSoup(response.data, features="lxml")
        rows = soup.findAll('table')[0].findAll('tr')
        # Creating Storage List
        nameList = []
        upDateList = []
        magnetLinkList = []
        i = 0
        # Print Details for all rows
        for j in range(2, len(rows)-1):
            # Grab Tabledata
            tableData = rows[j].find_all('td')

            tableLink = tableData[1].find('a')
            torrentName = tableLink.get('title')

            dateUpload = tableData[1].find('font', {'class:', 'detDesc'})
            dateUpString = str(dateUpload)
            dateUpStrReplace = dateUpString.replace('<font class="detDesc">Uploaded ', "")

            torrentLinkList = tableData[1].find_all('a')
            torrentMagnetLink = torrentLinkList[1]
            torrentMagnetLink = torrentMagnetLink.get('href')

            # Print Name
            finalTorrentName = torrentName.replace("Details for", " ")

            nameList.append(finalTorrentName)

            # Print Details
            stringEnd = string_stop(dateUpStrReplace, "U", "L")
            finalDateUploadString = dateUpStrReplace[0:stringEnd]

            upDateList.append(finalDateUploadString)

            # Magnet Link
            stringEnd = string_stop(torrentMagnetLink, "<", "t")
            finaltorrentMagnetLink = torrentMagnetLink[0:stringEnd]

            magnetLinkList.append(str(finaltorrentMagnetLink))
        global torrentList
        torrentList = [nameList, upDateList, magnetLinkList]
        return torrentList
    except:
        pass


def add_torrent(client, folder, magnetLink):
    try:
        magnet = int(magnetLink)
        if(folder==1):
            folder_dir = '/home/callum/Plex/TVShows'
        elif(folder==2):
            folder_dir = '/home/callum/Plex/Movies'
        client.download_from_link( torrentList[2][magnet], savepath=folder_dir)
        confirmed_box()
    except:
        pass


def add_client(clientIP, username, password):
    try:
        qb = Client(clientIP+"/")
        qb.login(username, password)
        return qb
    except:
        pass


def search_torrent(tree, terms):
    terms = terms.replace(" ", "%20")
    searchList = pirates_bay_scraper('thepiratebay10.org/search/' + terms)
    torrentList = searchList
    tree_populater(tree, searchList)


def tree_populater(tree, listOfTorrent):
    tree.delete(*tree.get_children())
    try:
        for i in range(len(listOfTorrent[0])):
            tree.insert('', 'end', text=listOfTorrent[0][i], values=(listOfTorrent[1][i], "Torrent # " + str(i)))
    except:
        pass


def check_client():
    if (os.path.isfile("configs.txt")):
        main_function_window()
    else:
        config_creator_window()


def create_config(window, name, ipaddress, username, password):
    window.destroy()
    configInfo = [name+"\n", ipaddress+"\n", username+"\n", password+"\n"]
    with open("configs.txt", 'a') as f:
        for i in range(4):
            f.write(configInfo[i])

        f.close()
        main_function_window()


def config_creator_window(isWindow=False, window=None):
    if (isWindow):
        window.destroy()

    configCreate = Tk()
    configCreate.title("Create your Config")
    configCreate.geometry("400x300")

    formattingFrame = tkinter.Frame(configCreate)

    regularFrame = tkinter.Frame(configCreate)
    formattingFrame.grid(row=0, column=0, sticky='nsew')
    regularFrame.grid(row=1, column=0, sticky='nsew')

    configCreate.grid_columnconfigure(0, weight=1)
    formattingFrame.grid_columnconfigure(0, weight=1)

    # Labels
    description = Label(formattingFrame, text="Create a download client configuration", font="ARIAL 12 bold")
    name = Label(regularFrame, text="Name of Config: ", font="ARIAL 14 bold")
    ip = Label(regularFrame, text="IP of torrent Client: ", font="ARIAL 14 bold")
    userN = Label(regularFrame, text="User Name: ", font="ARIAL 14 bold")
    passW = Label(regularFrame, text="Password: ", font="ARIAL 14 bold")

    # Text Entries
    nameEntry = Entry(regularFrame)
    ipEntry = Entry(regularFrame)
    userNEntry = Entry(regularFrame)
    passWEntry = Entry(regularFrame)

    # Button
    enterButton = Button(regularFrame, text="Enter", font="ARIAL 18 bold",
                         command=lambda: create_config(configCreate, str(nameEntry.get()), str(ipEntry.get()),
                                                       str(userNEntry.get()), str(passWEntry.get())))

    # Gridding
    description.grid(row=0, column=0)

    name.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)

    ip.grid(row=1, column=0)
    ipEntry.grid(row=1, column=1)

    userN.grid(row=2, column=0)
    userNEntry.grid(row=2, column=1)

    passW.grid(row=3, column=0)
    passWEntry.grid(row=3, column=1)

    enterButton.grid(row=4, column=1)

    configCreate.mainloop()


def selected_button(num):
        global dir
        dir = num


def main_function_window(torrent_connection=False, torrent_number=0):
    # Window Config
    window = Tk()
    window.title("Easy Torrent Downloader")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(str(screen_width) + 'x' + str(screen_height))

    var = tkinter.StringVar()
    # Frames
    widgetFrame = tkinter.Frame(window)
    treeFrame = tkinter.Frame(window)
    # Grids
    treeFrame.grid(row=1, column=0, sticky="nsew")
    widgetFrame.grid(row=0, column=0, sticky="nsew")

    # Top Frame Widgets

    # Radio Buttons
    tvDir = Radiobutton(widgetFrame, text="TV", value=1, variable=var, command = lambda : selected_button(1))
    movieDir = Radiobutton(widgetFrame, text="Movie", value=2, variable=var, command = lambda : selected_button(2))

    # Labels
    selectDir = Label(widgetFrame, text="Select Download Directory: ")
    selectConfig = Label(widgetFrame, text="Select Download Configuration: ")
    searchTorrentLabel = Label(widgetFrame, text="Search Torrent by Name: ")
    whichTorrentToDownload = Label(widgetFrame, text="Torrent # you would like to download: ")
    current_connection_info = Label(widgetFrame, text="Current Connection: "+str(torrent_number))
    # Text Entry
    torrentSearch = Entry(widgetFrame, width=50)
    torrentNumber = Entry(widgetFrame, width=5)
    # Listbox
    configSelector = Listbox(widgetFrame, height=1)
    configs_lists = list_populate(configSelector)
    # Button
    enterTorrentSearch = Button(widgetFrame, text="Search", font="ARIAL 10 bold",
                                command=lambda: search_torrent(tree, torrentSearch.get()))
    downloadTorrentButton = Button(widgetFrame, text="Download", font="ARIAL 10 bold",
                                   command=lambda: add_torrent(torrent_client, dir, torrentNumber.get()))
    createNewConfigButton = Button(widgetFrame, text="Create New Config", font="ARIAL 10 bold",
                                   command=lambda: config_creator_window(isWindow=True, window=window))
    create_connection_button = Button(widgetFrame, text="Connect", font="ARIAL 10 bold",
                                      command=lambda: connect_to_torrent_client(window, configSelector.get(ACTIVE)[0]))
    if not torrent_connection:
        torrent_client = add_client(configs_lists[1][0], configs_lists[2][0], configs_lists[3][0])
    else:
        torrent_client = add_client(configs_lists[1][int(torrent_number)], configs_lists[2][int(torrent_number)], configs_lists[3][int(torrent_number)])
    #Top Frame Widgets Grid
    selectDir.grid(column=0, row=0, columnspan=1)
    tvDir.grid(column=1, row=0)
    movieDir.grid(column=2, row=0)
    torrentSearch.grid(row=1, column=1, sticky='w', columnspan=4, rowspan=1)
    configSelector.grid(row=0, column=4)
    enterTorrentSearch.grid(row=1, column=4, )
    selectConfig.grid(row=0, column=3)
    searchTorrentLabel.grid(row=1, column=0, sticky='w')
    whichTorrentToDownload.grid(row=1, column=5)
    torrentNumber.grid(row=1, column=6)
    downloadTorrentButton.grid(row=1, column=7)
    createNewConfigButton.grid(row=0, column=5)
    create_connection_button.grid(row=0, column=6)
    current_connection_info.grid(row=0, column=7)
    # Tree
    tree = ttk.Treeview(treeFrame, columns=("Details", "Download"))
    tree.grid(row=0, column=0, sticky='NSEW')
    tree.heading('#0', text="Name")
    tree.heading("Details", text="Details")
    tree.heading("Download", text="Download")
    tree.column('#0', anchor='center')
    tree.column('Details', anchor='center')
    tree.column('Download', anchor='center')
    treeFrame.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=1)
    window.mainloop()


def list_populate(listBox, ):
    listBox.delete(0,END)
    config_name = []
    config_ip_address = []
    config_user_name = []
    config_password = []
    configList = []
    with open("configs.txt", 'r') as f:
        while True:
                currentLine = (f.readline()).strip()
                if currentLine == "":
                        break
                configList.append(str(currentLine))
        f.close()
    i = 0
    config_number = 0
    while i<len(configList)-3:
        listBox.insert(END, str(config_number) + ". " + configList[i])
        config_name.append(configList[i])
        config_ip_address.append("http://"+configList[i+1])
        config_user_name.append(configList[i+2])
        config_password.append(configList[i+3])
        config_number += 1
        i += 4
    return[config_name, config_ip_address, config_user_name, config_password]


def connect_to_torrent_client(window, active_torrent_number):
        window.destroy()
        main_function_window(torrent_connection=True, torrent_number=active_torrent_number)


def confirmed_box():
    window = Tk()
    window.title("Success")
    window.geometry('150x60')
    confirmed_message = Label(window, text="Success!")
    confirmed_message.pack(fill=X)
    confirmed_enter = Button(window, text="Ok", command=lambda: window.destroy())
    confirmed_enter.pack(fill=X)
    window.mainloop()


def main():
        check_client()


if __name__ == '__main__':
    main()
