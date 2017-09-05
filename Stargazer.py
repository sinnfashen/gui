import wx
import os
import sqlite3

import write_news_sql


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.quote = wx.StaticText(self, label="Your quote :", pos=(20, 30))

        self.con = sqlite3.connect('./You_Database.db')
        self.cur = self.con.cursor()
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        # self.logger = wx.TextCtrl(self, pos=(600,20), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # A button
        self.button = wx.Button(self, label="搜索", pos=(220, 325))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
        self.impo = wx.Button(self, label="导入", pos=(420, 325))
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.impo)

        self.LL = ['AND', 'OR', 'NOT']
        self.Data = {}
        self.Logic = {}

#            self.list.Append([i, self.results[i][10], self.results[i][12]], self.results[i][7], self.results[i][1],
#                             self.results[i][11], self.results[i][6], self.results[i][2], self.results[i][5])
        self.list = wx.ListCtrl(self, -1, (550, 20), (600, 350), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list.AppendColumn('ID',width=50)
        self.list.AppendColumn('标题',width=300)
        self.list.AppendColumn('作者',width=100)
        self.list.AppendColumn('来源报刊', width=100)
        self.list.AppendColumn('版面', width=100)
        self.list.AppendColumn('年', width=50)
        self.list.AppendColumn('月', width=50)
        self.list.AppendColumn('日', width=50)
        # self.list.AppendColumn('股票')
        # self.list.AppendColumn('公司')
        # self.list.AppendColumn('日期')
        self.list.AppendColumn('股票代码', width=100)

        # self.list.Append([1, 's', 'f', 'd'])

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenFile, self.list)

        # name
        wx.StaticText(self, label="文件名称 :", pos=(20, 60))
        self.Data['filename1'] = wx.TextCtrl(self, value="", pos=(150, 60), size=(140, -1))
        self.Logic['filename'] = wx.ComboBox(self, pos=(300, 60), size=(50, -1), choices=self.LL, style=wx.CB_DROPDOWN)
        self.Data['filename2'] = wx.TextCtrl(self, value="", pos=(360, 60), size=(140, -1))

        # code
        wx.StaticText(self, label="股票代码 :", pos=(20, 90))
        self.Data['stock1'] = wx.TextCtrl(self, value="", pos=(150, 90), size=(140, -1))
        self.Logic['stock'] = wx.ComboBox(self, pos=(300, 90), size=(50, -1), choices=self.LL, style=wx.CB_DROPDOWN)
        self.Data['stock2'] = wx.TextCtrl(self, value="", pos=(360, 90), size=(140, -1))

        # auther
        wx.StaticText(self, label="作者 :", pos=(20, 120))
        self.Data['author1'] = wx.TextCtrl(self, value="", pos=(150, 120), size=(140, -1))
        self.Logic['author'] = wx.ComboBox(self, pos=(300, 120), size=(50, -1), choices=self.LL, style=wx.CB_DROPDOWN)
        self.Data['author2'] = wx.TextCtrl(self, value="", pos=(360, 120), size=(140, -1))

        # place
        wx.StaticText(self, label="版面 :", pos=(20, 150))
        self.Data['place1'] = wx.TextCtrl(self, value="", pos=(150, 150), size=(140, -1))
        self.Logic['place'] = wx.ComboBox(self, pos=(300, 150), size=(50, -1), choices=self.LL, style=wx.CB_DROPDOWN)
        self.Data['place2'] = wx.TextCtrl(self, value="", pos=(360, 150), size=(140, -1))


        # the combobox Control
        self.YearList = [str(i) for i in range(1998, 2009, 1)]
        self.MonthList = [str(i) for i in range(1, 13, 1)]
        self.DayList = [str(i) for i in range(1, 32, 1)]
        wx.StaticText(self, label="日期：", pos=(20,180))
        self.Data['SY'] = wx.ComboBox(self, pos=(20, 200), size=(60, -1), choices=self.YearList, style=wx.CB_DROPDOWN, value='1998')
        wx.StaticText(self, label="年", pos=(84, 204))
        self.Data['SM'] = wx.ComboBox(self, pos=(100, 200), size=(40, -1), choices=self.MonthList, style=wx.CB_DROPDOWN, value='02')
        wx.StaticText(self, label="月", pos=(144, 204))
        self.Data['SD'] = wx.ComboBox(self, pos=(160, 200), size=(50, -1), choices=self.DayList, style=wx.CB_DROPDOWN, value='28')
        wx.StaticText(self, label="日", pos=(214, 204))
        wx.StaticText(self, label="至（前后包含)", pos=(80, 228))
        self.Data['EY'] = wx.ComboBox(self, pos=(20, 250), size=(60, -1), choices=self.YearList, style=wx.CB_DROPDOWN, value='2017')
        wx.StaticText(self, label="年", pos=(84, 254))
        self.Data['EM'] = wx.ComboBox(self, pos=(100, 250), size=(40, -1), choices=self.MonthList, style=wx.CB_DROPDOWN, value='08')
        wx.StaticText(self, label="月", pos=(144, 254))
        self.Data['ED'] = wx.ComboBox(self, pos=(160, 250), size=(50, -1), choices=self.DayList, style=wx.CB_DROPDOWN, value='11')
        wx.StaticText(self, label="日", pos=(214, 254))
        # Checkbox
        #self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?", pos=(20,180))
        #self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)
        '''
        # Radio Boxes
        radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
        rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
                         style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenFile)
        '''
    def SearchError(self):
        dlg = wx.MessageDialog(None, u"搜索不合法！", u"错误", wx.OK | wx.ICON_ERROR)
        if dlg.ShowModal() == wx.ID_OK:
            self.Close(True)
        dlg.Destroy()

    def SearchOK(self):
        dlg = wx.MessageDialog(None, u"完成", u"提示", wx.OK | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_OK:
            self.Close(True)
        dlg.Destroy()

    def ImportError(self, e):
        dlg = wx.MessageDialog(None, str(e), u"错误", wx.OK | wx.ICON_ERROR)
        if dlg.ShowModal() == wx.ID_OK:
            self.Close(True)
        dlg.Destroy()

    def OnClick(self,event):
        self.list.DeleteAllItems()
        self.results = []

        condition = ''
        if self.Data['filename1'].Value:
            if condition:
                condition = '{} AND'.format(condition)
            condition = '{} ('.format(condition)
            condition = '{} {}'.format(condition, 'title_docu LIKE "%{}%"'.format(self.Data['filename1'].Value))
            if self.Logic['filename'].Value and self.Data['filename2'].Value:
                condition = '{} {} {}'.format(condition, self.Logic['filename'].Value, 'title_docu LIKE "%{}%"'.format(self.Data['filename2'].Value))
            condition = '{} )'.format(condition)

        if self.Data['stock1'].Value:
            if condition:
                condition = '{} AND'.format(condition)
            condition = '{} ('.format(condition)
            condition = '{} {}'.format(condition, 'gupiao = {}'.format(self.Data['stock1'].Value))
            if self.Logic['stock'].Value and self.Data['stock2'].Value:
                condition = '{} {} {}'.format(condition, self.Logic['stock'].Value, 'gupiao = {}'.format(self.Data['stock2'].Value))
            condition = '{} )'.format(condition)

        if self.Data['place1'].Value:
            if condition:
                condition = '{} AND'.format(condition)
            condition = '{} ('.format(condition)
            condition = '{} {}'.format(condition, 'banmian LIKE "%{}%"'.format(self.Data['place1'].Value))
            if self.Logic['place'].Value and self.Data['place2'].Value:
                condition = '{} {} {}'.format(condition, self.Logic['place'].Value, 'banmian LIKE "%{}%"'.format(self.Data['place2'].Value))
            condition = '{} )'.format(condition)

        if self.Data['author1'].Value:
            if condition:
                condition = '{} AND'.format(condition)
            condition = '{} ('.format(condition)
            condition = '{} {}'.format(condition, 'ZUOZHE = "{}"'.format(self.Data['author1'].Value))
            if self.Logic['author'].Value and self.Data['author2'].Value:
                condition = '{} {} {}'.format(condition, self.Logic['author'].Value, 'zuozhe = "{}"'.format(self.Data['author2'].Value))
            condition = '{} )'.format(condition)

        if condition:
            condition = '{} AND'.format(condition)
        condition = '{} ('.format(condition)
        if self.Data['SY'].Value == self.Data['EY'].Value:
            date = 'YEAR = {} AND'.format(self.Data['SY'].Value)
            if self.Data['SM'].Value == self.Data['EM'].Value:
                date = '{} MONTH = {} AND'.format(date, self.Data['SM'].Value)
                if self.Data['SD'].Value == self.Data['ED'].Value:
                    date = '{} DAY = {}'.format(date, self.Data['SD'].Value)
                else:
                    date = '{} DAY between {} and {} '.format(self.Data['SD'].Value, self.Data['ED'].Value)
            else:
                date = '{} (MONTH = {} AND DAY >= {}) OR (MONTH = {} AND DAY <= {}) OR (MONTH between {} and {})'.format(
                    date, self.Data['SM'].Value, self.Data['SD'].Value,
                    self.Data['EM'].Value, self.Data['ED'].Value,
                    int(self.Data['SM'].Value)+1, int(self.Data['EM'].Value)-1)
        elif self.Data['SY'].Value < self.Data['EY'].Value:
            date = '(YEAR = {} AND MONTH = {} AND DAY >= {}) OR ' \
                   '(YEAR = {} AND MONTH > {}) OR' \
                   '(YEAR between {} and {}) OR' \
                   '(YEAR = {} AND MONTH < {}) OR' \
                   '(YEAR = {} AND MONTH = {} AND DAY <= {})'.format(
                self.Data['SY'].Value, self.Data['SM'].Value, self.Data['SD'].Value,
                self.Data['SY'].Value, self.Data['SM'].Value,
                int(self.Data['SY'].Value)+1, int(self.Data['EY'].Value)-1,
                self.Data['EY'].Value, self.Data['EM'].Value,
                self.Data['EY'].Value, self.Data['EM'].Value, self.Data['ED'].Value
            )
        else:
            self.SearchError()
            return
        condition = '{} {} )'.format(condition, date)

        if not condition:
            self.SearchError()
            return
        order = 'SELECT * FROM You_gongsi WHERE {}'.format(condition)
        responde = self.cur.execute(order)
        for row in responde:
            self.results.append(row)
        for i in range(self.results.__len__()):
            self.list.Append([i, self.results[i][10], self.results[i][12], self.results[i][7], self.results[i][1],
                              self.results[i][11], self.results[i][6], self.results[i][2], self.results[i][5]])
        self.SearchOK()

    def OpenFile(self, event):
        path = self.results[int(event.Label)][8]
        if path.find('H:') != -1:
            path = path.replace('H:', os.getcwd())
        os.system('notepad {}'.format(path))

    def OnOpen(self, e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.DirDialog(self, "Choose a dir", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            try:
                write_news_sql.main(self.dirname)
                self.SearchOK()
            except Exception as e:
                self.ImportError(e)
        dlg.Destroy()


class DatabaseFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1200, 430))
        '''
        self.control = wx.TextCtrl(self)
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
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
        '''


with open('xpdfrc.tem', 'r') as f:
    lines = f.readlines()

with open('xpdfrc', 'w') as f:
    for line in lines:
        f.write('{}\n'.format(line.replace('direction', os.path.join(os.getcwd(), 'xpdfbin-win-3.04'))))

app = wx.App(False)
frame = DatabaseFrame(None, 'Stargazer (alpha)')
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()