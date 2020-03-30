from tkinter import *
from tkinter import ttk
from pymarc import MARCReader
import requests


with open('\\\\library.northwestern.edu\cab\StaffDocs\jcs8769\Documents\AuthorityOngoing\Ongoing work\weekof20191229\\boxrecords', 'rb') as fh:

    reader = MARCReader(fh, to_unicode=True, force_utf8=True)

    count = 0

    for record in reader:

        count += 1

        pcc_status = record['042']

        mmsid = re.sub("=001  ", "", str(record['001']))

        #removes headings from PCC records


        if pcc_status == None:

            for f in record.get_fields('100' , '600' , '700'):

                fx = str(f)

                #if re.search(".+\$0\(uri\).+", fx):

                subfield_a = re.sub(r"(=.00  ..)(\$a)(.+?)(\$e.+|$)", r"\3", fx)

                has_subfields = re.search(r"\$[bcdfghjklmnopqrstux1234568]", fx)

                if not has_subfields:
                    #prints headings that are only $a

                    space_count = subfield_a.count(" ")

                    fy = re.sub(r"(\$0)", r" |\1", fx)

                    if subfield_a.isupper() is not True:

                        if space_count <= 1:

                            if re.search("\$0\(uri\)", fx):

                                fz = fx

                                for cnt, line in enumerate(record):

                                    if re.search(fz, str(line)):
                                        indexofheadingstart = float(cnt) + 2
                                        # print(indexofheadingstart)

                                lccn = re.sub(r"(.+)(http:\/\/id\.loc\.gov\/authorities\/names\/)(.+)(\$)(.+)",
                                              r"http://www.viaf.org/viaf/lccn/\3/marc21.xml", fx)

                                r = requests.get(lccn)

                                r1 = re.sub(r'(<mx:datafield ind1=\".\" ind2=\".\" tag=\")(...)(\">)', r'Tag=\2 ', r.text)

                                r2 = re.sub(r'(<mx:subfield code=\")(.)(\">)', r'$\2', r1)

                                r3 = re.sub(r'(<mx:datafield tag=\")(...)(\" ind1=\".\" ind2=\".\">)', r'Tag=\2 ', r2)

                                r4 = re.sub(r'(<.+>)', r'', r3)

                                        ########################################################
                            ##WIdgets start here
                                class AuthorityControl:

                                    def __init__(self, master):

                                        self.label = ttk.Label(master, text = "Personal Name Authority Control")
                                        self.label.grid(row = 0, column = 0, columnspan = 2)

                                        ttk.Button(master, text="Submit",
                                                   command=self.submit_button).grid(row=2, column=0, sticky= 'e')

                                        ttk.Button(master, text="Next",
                                                   command=master.destroy).grid(row=2, column=3, sticky= 'w')

                                        self.bib = Text(master, width=60, height = 30)
                                        self.bib.grid(row=5, column=0, columnspan=1, padx=5, sticky='n')
                                        self.bib.config(wrap = 'word')
                                        self.bib.configure(state='normal')
                                        self.bib.insert(1.0, record)
                                        self.bib.configure(state='disabled')

                                        bib_scrollbar = ttk.Scrollbar(master, orient = VERTICAL, command = self.bib.yview)
                                        bib_scrollbar.grid(row = 5, column = 1, sticky= 'ns')
                                        self.bib.config(yscrollcommand = bib_scrollbar.set)

                                        #tag the heading in the bib
                                        self.bib.tag_add('tag_heading', '{}'.format(indexofheadingstart), '{} lineend'.format(indexofheadingstart))
                                        self.bib.tag_configure('tag_heading', background = '#00ffff')

                                        self.aut = Text(master, width=60, height = 30)
                                        self.aut.grid(row=5, column=3, columnspan=1, padx=5, sticky='n')
                                        self.aut.config(wrap = 'word')
                                        self.aut.configure(state='normal')
                                        self.aut.insert(1.0, r4)
                                        self.aut.configure(state='disabled')

                                        aut_scrollbar = ttk.Scrollbar(master, orient = VERTICAL, command = self.aut.yview)
                                        aut_scrollbar.grid(row = 5, column = 4, sticky= 'ns')
                                        self.aut.config(yscrollcommand = aut_scrollbar.set)

                                        self.updated_name = ttk.Entry(master, width = 140)
                                        self.updated_name.grid(row = 4, column = 0, columnspan= 4, sticky ='w')
                                        self.updated_name.insert(0, fx)

                                        self.record_count_label = ttk.Label(master, text="Record number: {}".format(count))
                                        self.record_count_label.grid(row=6, column=0, columnspan=1, sticky='e')

                                    def submit_button(self):
                                        print(mmsid, '||', subfield_a, ' || {}'.format(self.updated_name.get()), ' || ', '‡g(', record['650']['a'], ')','‡5IEN', sep='')
                                        #self.label.config(text='Submit action here')

                                def main():

                                    root = Tk()
                                    app = AuthorityControl(root)
                                    root.mainloop()

                                if __name__ == "__main__": main()
