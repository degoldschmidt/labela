from cli import *
from test import load_data
import tkinter as tk
from tkinter import filedialog
import os

class Label(object):
    def __init__(self, _name, _date):
        self.name = _name
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
            out_header = "\\vspace*{-0.15cm}\n"
        main =  "\\begin{large}\n" + "{0:} \\\\[0.5em]\n".format(self.name) +  "\\end{large}\n" + "{1:}\n\\newpage".format(self.name, self.date)
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
\\usepackage{fontspec}
\\setmainfont{Courier}


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


if __name__ == "__main__":
    tk.Tk().withdraw()
    ### 1) Type in google sheets ID
    # tkinter entry window OR command line interface
    #_id = query_val('Please type in ID for google sheets', '\n[You can find the ID in the URL to the sheets]\n')
    df = load_data() # test data

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
    os.system('"xelatex" -synctex=1 -interaction=nonstopmode {}'.format(_filename))
    os.system('mv {}.pdf ./pdf/{}.pdf'.format(os.path.join(_cwd, _basename), _basename))
    os.system('rm {}.*'.format(_basename))
