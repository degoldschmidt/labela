import tkinter as tk
from tkinter import filedialog
import os, sys

from cli import *
from test import load_data
from yamlio import *
from gapp import *

class Label(object):
    def __init__(self, _name, _date):
        self.name = _name
        self.name = self.name.replace('_', '\\_')
        self.name = self.name.replace('#', '\\#')
        self.sizer = 'large'
        if len(self.name) > 10:
            self.sizer = 'normalsize'
        if len(self.name) > 15:
            self.sizer = 'small'
        if len(self.name) > 20:
            self.sizer = 'footnotesize'
        if len(self.name) > 30:
            self.sizer = 'scriptsize'
        self.date = _date
        if _date == 'today':
            self.date = '\\today'
        self.header = False

    def __str__(self):
        out_header = ""
        if self.header:
            out_header =  """
\\begin\{tabular\}\{ p\{1.3in\} p\{1.2in\} r }
{:} & {:} & {:} \\\\
\\hline \\\\
\\end\{tabular\}
""".format(self.TL, self.TC, self.TR)
        else:
            out_header = "\\topskip0pt\n\\vspace*{\\fill}"

        main =  "\\begin{"+self.sizer+"}\n" + "{0:} \\\\[0.5em]\n".format(self.name) +  "\\end{"+self.sizer+"}\n" + "\\footnotesize{1:}\n".format(self.name, self.date) + "\\vspace*{\\fill}\n\\newpage"
        return out_header + main

def get_header():
    return """
% Using 17pt as standard font size
\\documentclass[17pt]{extarticle}
\\usepackage[paperwidth=4in, paperheight=2in, margin=7.5mm, tmargin=10mm]{geometry}
\\usepackage{multicol}

% No indent
\\setlength\\parindent{0pt}

% Thicker hline
\\setlength{\\arrayrulewidth}{.2em}

% Custom font
\\usepackage[quiet]{fontspec}
\\setmainfont{Courier New}


% Format date
\\usepackage[ddmmyyyy]{datetime}
\\usepackage{advdate}
\\newcommand{\yesterday}{{\\AdvanceDate[-1]\\today}}
\\newcommand{\\tomorrow}{{\\AdvanceDate[1]\\today}}

\\begin{document}
\\bf
"""

def get_footer():
    return "\\end{document}"

def convert2pdf(_file, _out=""):
    pass

def get_gsheets(sheet=None, srange=None):
    if sheet is None:
        if os.path.exists(find_stocks()) and query_yn("Found stocks file. Do you want to use it?", default='yes'):
            sheetid = read_yaml(find_stocks())['id']
            sheetrange = read_yaml(find_stocks())['range']
        else:
            sheetid = query_val("Type Google Sheet identifier", "[Can be found in the url address of your sheet after /d/]")
            sheetrange = query_val("Type sheet range to import", "[Press ENTER if you want to load all data]")
            if query_yn("Do you want to save this sheet for future use?", default='yes'):
                write_yaml(find_stocks(), {'id': sheetid, 'range': sheetrange})
    else:
        sheetid = sheet
        sheetrange = srange

    gsheets = GApp(sheetid)
    values = gsheets.get_data(sheetrange)
    df = list_to_df(values)
    return df.dropna(how='all')


if __name__ == "__main__":
    tk.Tk().withdraw()
    ### 1) Type in google sheets ID
    # tkinter entry window OR command line interface
    df = get_gsheets() # test data

    ### 2) Show data in table
    print("\nYour stocks:")
    print(df)
    print()

    ### 3) Type in label column
    _label = query_val('Please type in which column should be the label', '[default: "genotype"]\n', default='genotype')
    assert _label in df.columns, "Label is not in columns"

    ### 4) Write TeX file
    _cwd = os.getcwd()
    _filename = filedialog.asksaveasfilename(title="Save TeX file as...", defaultextension=".tex", initialdir=os.path.join(_cwd,'tex'))
    assert len(_filename) > 0, "Not a valid filename"
    if os.path.exists(_filename):
        wmode = 'wt'
    else:
        wmode = 'xt'
    with open(_filename, wmode) as f:
        f.write(get_header())
        for each_row in df[_label]:
            if not each_row is _label:
                this_label = Label(each_row, '')
                f.write(str(this_label))
        f.write(get_footer())

    ### 5) Convert TeX file to pdf file
    _basename = os.path.basename(_filename).split('.')[0]
    os.system('"xelatex" -synctex=1 -interaction=nonstopmode -halt-on-error {}'.format(_filename))
    if sys.platform == 'win32' or sys.platform == 'win64':
        os.system('copy {}.pdf {}.pdf'.format(os.path.join(_cwd, _basename), os.path.join(_cwd, 'pdf',_basename)))
        os.system('del {}.*'.format(_basename))
    else:
        os.system('cp {}.pdf ./pdf/{}.pdf'.format(os.path.join(_cwd, _basename), _basename))
        os.system('rm {}.*'.format(_basename))
