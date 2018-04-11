import argparse
import subprocess
import os

mainstr =   """
%%% Written with Labela\n% Using 17pt as standard font size
\\documentclass[17pt]{extarticle}
\\usepackage[paperwidth=4in, paperheight=2in, margin=7.5mm, tmargin=10mm, bmargin=2mm]{geometry}
\\usepackage{multicol}
% No indent
\\setlength\\parindent{0pt}
% Thicker hline
\\setlength{\\arrayrulewidth}{.1em}
% Custom font
\\usepackage{fontspec}
\\setmainfont{Comfortaa}
\\usepackage{mathtools}
\\usepackage{wasysym}
% Format date
\\usepackage[ddmmyyyy]{datetime}
\\usepackage{advdate}
\\begin{document}
"""

def get_label(GAL4, UAS):
    labelstr = "\\begin{small}\n"
    if "^" in UAS:
        stuff = UAS.split('^')[0]
        upper = UAS.split('^')[1]
        rUAS = stuff+'$^{\\textnormal{'+upper+'}}$'
    else:
        rUAS = UAS
    labelstr += "\\textbf{"+GAL4+"-GAL4 > UAS-"+rUAS+"}"
    labelstr += """
\\newline

\\vspace*{-0.2in}

\\noindent
\\begin{tabular}{ p{1.8in} r }
\\hline \\\\[-0.75em]
eclosion \\& add \\mars: & \\thisday \\\\
flip YBM: & \\AdvanceDate[3]\\thisday \\\\
flip diet: & \\AdvanceDate[4]\\thisday \\\\
assay: & \\AdvanceDate[8]\\thisday \\\\
\\end{tabular}
\\end{small}
\\newpage
                """
    return labelstr



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gal4', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('--uas', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('--days', nargs='+', help='<Required> Set flag', required=True)

    list_uas = parser.parse_args().uas
    list_gal4 = parser.parse_args().gal4
    list_days = parser.parse_args().days

    with open('lines.tex', 'w') as f:
        for uas in list_uas:
            for gal in list_gal4:
                f.write(get_label(gal, uas))

    for day in list_days:
        mainstr += "\\def \\thisday{\\AdvanceDate["+day+"]\\today}\n\\input{lines}"

    mainstr += "\\end{document}"

    with open('out.tex', 'w') as f:
        f.write(mainstr)

    FNULL = open(os.devnull, 'w')
    return_value = subprocess.call(['xelatex', 'out.tex'], stdout=FNULL, stderr=subprocess.STDOUT)
    for each_file in os.listdir():
        if not each_file.endswith('pdf'):
            os.remove(each_file)
