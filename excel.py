import win32com.client as win32
import re

class Excel:
    def __init__(self,filename = None):
        self.xlapp = win32.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlbook = self.xlapp.Workbooks.Open(filename)
        else:
            self.xlbook = self.xlapp.Workbooks.Add()
            self.filename = ''
        self.xlapp.Visible = False   #隐藏操作excel
        self.xlapp.DisplayAlerts = False  #不弹出提示


    def creatSheet(self, before=None , after = None , name=None):
        sht = self.xlbook.Worksheets.Add(Before = before,After =after)
        if name:
            sht.Name = name

    def renameSheet(self, sheet , name):
        try:
            self.xlbook.Worksheets(sheet).Name = name
        except Exception as e:
            print(e.args[0])


    def save(self,savefilename = None):
        if savefilename:
            self.filename = savefilename
            self.xlbook.SaveAs(savefilename)
        else:
            self.xlbook.Save()

    def close(self):
        self.xlbook.Close(SaveChanges=False)
        self.xlapp.Application.Quit()

    def getCell(self, sheet , row , col):
        "get value of one cell"
        sht =self.xlbook.Worksheets(sheet)
        return sht.Cells(row , col).Value

    def setCell(self, sheet , row , col , value):
        "set value of one cell"
        sht = self.xlbook.Worksheets(sheet)
        sht.Cells(row , col).Value = value

    def getRange(self, sheet , row1 , col1 , row2 , col2):
        "get values of a range"
        sht = self.xlbook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1,col1),sht.Cells(row2,col2)).Value

    def setRange(self, sheet ,  top_row ,left_col , values):
        sht = self.xlbook.Worksheets(sheet)
        right_col = left_col + len(values[0]) - 1
        bottom_row = top_row + len(values) - 1
        sht.Range(sht.Cells(top_row, left_col), sht.Cells(bottom_row, right_col)).Value = values

    def getContiguousRange(self, sheet , row , col):
        sht = self.xlbook.Worksheets(sheet)
        bottom = row
        while sht.Cells(bottom + 1, col).Value not in [None, '']:
            bottom += 1
        right = col
        while sht.Cells(col, right+1).Value not in [None, '']:
            right += 1
        return sht.Range(sht.Cells(row, col), sht.Cells(bottom, right)).Value

    def fixStringsAndDates(self, aMatrix):
        # converts all unicode strings and times
        newmatrix = []
        for row in aMatrix:
            newrow = []
            for cell in row:
                if cell is None:
                    newrow.append('')
                elif isinstance(cell,str):
                    cell = cell.strip()
                    if is_int(cell):
                        newrow.append(str(int(cell)))
                    else:
                        newrow.append(cell)
                else:
                    newrow.append(str(cell))
                # if isinstance(cell, win32.pywintypes.UnicodeType):
                #     newrow.append(str(cell))
                # elif isinstance(cell, win32.pywintypes.TimeType):
                #     newrow.append(str(cell))
                # elif cell is None:
                #     newrow.append('')
                # else:
                #     newrow.append(cell)
            newmatrix.append(newrow)
        return newmatrix

    def setCellFormat(self, sheet , row , col ,format_str):
        """format_str: "@" 设置A1单元格为文本格式
                       "yyyy/m/d" '设置B1单元格为日期格式
                       "[$-F400]h:mm:ss AM/PM" '设置C1单元格为时间格式
                       "0.00%" '设置D1单元格为百分比格式
                       "0.00E+00" '设置E1单元格为科学记数法格式
                       "G/通用格式" '设置F1单元格为常规格式
        """
        sht = self.xlbook.Worksheets(sheet)
        sht.Cells(row , col).NumberFormatLocal = format_str

    def setRangeFormat(self, sheet , row1 , col1 , row2 , col2 ,format_str):
        sht = self.xlbook.Worksheets(sheet)
        sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).NumberFormatLocal = format_str





def is_int(num):
    pattern = re.compile('^[-+]?[0-9]+(\.0*)?$')
    result = re.match(pattern,num)
    if result:
        return True
    else:
        return False

def is_float(num):
    pattern = re.compile('^[-+]?[0-9]+(\.[0-9]*)?$')
    result = re.match(pattern,num)
    if result:
        return True
    else:
        return False