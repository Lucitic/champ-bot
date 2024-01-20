import pandas as pd
import numpy as np
import io
from pyscript import document


heads = []
fams = []
head_id = 0
head_template = document.createElement("head-template")
dicts = {}
early_exit = False




def addHead(event):
    input_value = document.querySelector("#headname")
    head_name = input_value.value
    heads.append(head_name)
    arr_div = document.querySelector("#headsarr")
    arr_div.innerText = heads

    input_value.value = ""
    head_id = f"head-{len(heads)}"
    head_el = head_template.cloneNode(head_id)
    document.querySelector("#head_list").append(head_el)
    head_el.setAttribute("headName", head_name)
    head_el.setAttribute("id", head_id)
    head_el.setAttribute("class", "head")


def addFam(event):
    input_value = document.querySelector("#famname")
    fam = input_value.value
    fams.append(fam)
    input_value.value = ""
    arr_div = document.querySelector("#famsarr")
    arr_div.innerText = fams


def dictConstruct(event):
    document.querySelector("#first").style.display = "none"
    document.querySelector("#second").style.display = "block"

    all_els = document.querySelectorAll("head")

    heads_selector = document.createElement("all-heads-selector")
    document.querySelector("#head_list").appendChild(heads_selector)

    for head in heads:
        label = document.createElement("label")
        heads_selector.appendChild(label)
        label.setAttribute("for", head)
        label.innerText = f"Choose the fam '{head}' is leading"
        head_sel = document.createElement("select")
        heads_selector.appendChild(head_sel)
        head_sel.setAttribute("value", head)
        head_sel.setAttribute("name", "head")

        for fam in fams:
            option = document.createElement("option")
            option.setAttribute("value", fam)
            option.innerText = fam
            head_sel.appendChild(option)

        heads_selector.appendChild(document.createElement("br"))

def dictCombine(event):
    list_heads_with_fams = document.querySelectorAll("select[name]")
    pairs = list_heads_with_fams.entries()

    for pair in pairs:
        key = pair[0]
        value = pair[1]
        if key in dicts:
            dicts[key].append(value)
        else:
            dicts[key] = [value]

    document.querySelector("#second").style.display = "none"
    document.querySelector("#third").style.display = "block"


async def csvFile(event):
        file = document.querySelector("#champCSV").files.to_py().item(0) #input("give the filepath to the csv in string format i.e'/folder/folder/name.csv'")

        fam_heads = heads #input("who are the family heads? give response in ['name', 'name', 'name', ...]") #given in [,]
        fam_names = fams #input("what are the names of the families? given in the same format as previous.") #given in [,]
        fam_relations = dicts
        #for testing
        """fam_heads = ['chris', 'grace', 'callum', 'lawrence', 'ali','gilberto', 'hari','therese']#input("who are the family heads? give response in ['name', 'name', 'name', ...]") #given in [,]
        fam_names = ['Mecha', 'Star', 'laser','anima']#input("what are the names of the families? given in the same format as previous.") #given in [,]
        fam_relations = {'Mecha': ['gilberto', 'lawrence'], 'Star' : ['chris', 'grace'], 'laser': ['hari', 'callum'], 'anima' : ['therese', 'ali']}

"""
        file_content = await file.text()
        tbl = pd.read_csv(io.StringIO(file_content))
        #for fam in fam_names:
            #fam_heads_for_fam = input(f"for family {fam}, who are the heads? give in ['name', 'name',..] format") #
            #fam_relations[fam] = fam_heads_for_fam
        #tbl = pd.read_csv(file_path) #rxc table

        tbl_names={}

        def getPrefs(tbl):
            try:
                tbl['Preferences'] = tbl['Prefs'].fillna(tbl['Preferences'])
            except LookupError as e:
                early_exit = True
                return early_exit

            for name in fam_heads:
                tbl_name = f"{name}_table"
                tbl_names[tbl_name] = tbl[nameFilter(name)]
            for name in fam_names:
                tbl_name = f"{name}_table"
                tbl_names[tbl_name] = tbl[nameFilter(name)]
            return None

        def nameFilter(name): # checks whther a name is in pref returns array for T and F's rx1 filtered by whether a substring is in
            return tbl['Preferences'].str.count(nameRegexPrep(name))>0

        def nameRegexPrep(name): #takes a name and makes it a regex pattern
            regex = ''
            for letter in name:
                regex += f'[{letter}{letter.swapcase()}]+'
            return regex

        def combineTables(tables, relation): #goes through array of tables and combines based on a dictionary of keys
            joint_dict = dict()
            combined = pd.DataFrame()
            for fam in fam_relations: #heads [,], fam string
                heads = fam_relations[fam]
                fam_tbl = f"{fam}_table"
                head_tbls = [tbl_names[f'{head}_table'] for head in heads]
                #joint_dict[f"{fam}"] = tbl_names[fam_tbl].join(head_tbls)
                combined_head = pd.concat(head_tbls)
                combinedfamtbl = pd.concat([tbl_names[fam_tbl], combined_head])[['Email Address', 'First Name', 'Last Name', 'Discord Tag (ex. Gamer#1337)']]
                combinedfamtbl["fam"] = f"{fam}"
                joint_dict[f"{fam}"] = combinedfamtbl
                combined = pd.concat(objs = [combined, combinedfamtbl], ignore_index = True)
            return joint_dict, combined



        early_exit = getPrefs(tbl)
        if early_exit:
            early_exit = False
            alert = document.createElement("script")
            document.body.appendChild(alert)
            alert.innerText = "alert('Please rename the Preferences column in the uploaded csv file where names are indicated Prefs for the program to work');"
            return
        results, csv_results = combineTables(tbl_names, fam_relations)
        print("\n ______ Preliminary fam results in out.zip ______ \n")
        """print_q = ""
        while print_q != "y" and print_q != "n" :
            print_q = input('Would you like to see the preview of the results? (y/n)')
            if print_q == "y":
                print(results)
            elif print_q == "n":
                print('ok')
            else:
                print("Please provide a valid input")"""

        compression_opts = dict(method='zip',
                                archive_name='out.csv')
        csv_results.to_csv('out.zip', index=False,
                  compression=compression_opts)


        document.querySelector("#third").style.display = "none"
        document.querySelector("#fourth").style.display = "block"
