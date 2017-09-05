# -*- coding: utf-8 -*-
# @Time  : 2017/8/7 15:02
# @Author: FSOL
# @File  : gui.py

import os

import wx

class DatabaseFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 512))
        self.control = wx.TextCtrl(self)
        self.panel = wx.Panel(self)
        self.CreateStatusBar()

        filemenu = wx.Menu()

        AboutItem = filemenu.Append(wx.ID_ABOUT, "About", "Information about this program")
        filemenu.AppendSeparator()
        ExitItem = filemenu.Append(wx.ID_EXIT, "Exit", "Terminate the program")

        self.Bind(wx.EVT_MENU, self.OnOpen, AboutItem)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "FFFF")

        self.SetMenuBar(menuBar)
        self.Show(True)

    def OnOpen(self, e):
        """ Open a file"""
        keys = ['a', 'b']
        self.list = wx.ListCtrl(self.panel, -1, (15, 50), (500, 250), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i in range(2):
            self.list.InsertColumn(i, keys[i])
        row = 0

app = wx.App(False)
frame = DatabaseFrame(None, 'Small editor')
app.MainLoop()
