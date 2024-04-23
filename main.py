from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

def get_spikes(fd_dvars_spikes, outlier_spikes):
    '''
    Description:
        Asks for where spikes are occurring
    Arguments:
        fd_dvars_spikes:set(string) - list of spikes on fd and dvars graphs
        outlier_spikes:set(string) - list of outlier spikes
    Returns:
        all_spike_string:string - formatted string of spikes that appear in all graphs
        fd_dvars_spike_string:string - formatted string of spikes that appear in only fd and dvars graphs
        fd_dvars_spikes:set(string) - updated list of spikes that appear in  fd and dvars graph
        outlier_spikes: set(string) - updated list of spikes that appear in outlier graph
    '''
    # Collect spikes
    while True:
        spike = input("Add spike: ")
        if not spike.isdigit():
            print("Spikes done")
            break
        else:
            fd_dvars_spikes.add(spike.strip())
            choice = input("Also on outlier? y/n: ")
            if choice.lower() == "y":
                outlier_spikes.add(spike.strip())
    
    # Format spike_string
    all_spike_string = "Spikes around "
    fd_dvars_spike_string = "Spikes around "
    sorted_spikes = list(fd_dvars_spikes)
    sorted_spikes.sort()

    for i, spike in enumerate(sorted_spikes):
        if i < len(fd_dvars_spikes)-1:
            if spike in outlier_spikes:
                all_spike_string += f"t={spike}, "
            else:
                fd_dvars_spike_string += f"t={spike}, "
        else:
            if spike in outlier_spikes:
                all_spike_string += f"t={spike} "
            else:
                fd_dvars_spike_string += f"t={spike} "
    
    all_spike_string += "on all graphs. "
    fd_dvars_spike_string += "on the DVARS and FD graphs. "
    
    return all_spike_string, fd_dvars_spike_string, fd_dvars_spikes, outlier_spikes

def get_wraps(bold_wrap, std_wrap):
    '''
    Description:
        Asks for where wrap-arounds are occurring
    Arguments:
        bold_wrap:set
        std_wrap:set
    Returns:
        bold_string:string
        std_string:string
        bold_wrap:set
        std_wrap:set
        '''
    # Get wraps
    while True:
        wrap = input("Add wrap-around: ")
        if not wrap or not wrap[0].isdigit():
            print("Wrap-arounds done")
            break
        else:
            set_ = input("Bold or std set? ")
            if set_.lower() == "bold":
                bold_wrap.add(wrap)
            else:
                std_wrap.add(wrap)
    
    # Make strings
    bold_string = "BOLD: Wrapping in images "
    for i, wrap in enumerate(bold_wrap):
        if i < len(bold_wrap)-1: 
            bold_string += f"{wrap}, "
        else:
            bold_string += f"{wrap}. "

    std_string = "STD: Wrapping in images "
    for i, wrap in enumerate(std_wrap):
        if i < len(std_wrap)-1: 
            std_string += f"{wrap}, "
        else:
            std_string += f"{wrap}. "

    return bold_string, std_string, bold_wrap, std_wrap

def get_fuzz(bold_fuzz, std_fuzz):
    '''
    Description:
        Asks for where fuzziness is occurring
    Arguments:
        bold_fuzz:set
        std_fuzz:set
    Returns:
        bold_string:string
        std_string:string
        bold_fuzz:set
        std_fuzz:set
        '''
    # Get wraps
    while True:
        fuzz = input("Add fuzziness: ")
        if not fuzz or not fuzz[0].isdigit():
            print("Fuzziness done")
            break
        else:
            set_ = input("Bold or std set? ")
            if set_.lower() == "bold":
                bold_fuzz.add(fuzz)
            else:
                std_fuzz.add(fuzz)
    
    # Make strings
    bold_string = "BOLD: Fuzziness in images "
    for i, fuzz in enumerate(bold_fuzz):
        if i < len(bold_fuzz)-1: 
            bold_string += f"{fuzz}, "
        else:
            bold_string += f"{fuzz}. "

    std_string = "STD: Fuzziness in images "
    for i, fuzz in enumerate(std_fuzz):
        if i < len(std_fuzz)-1: 
            std_string += f"{fuzz}, "
        else:
            std_string += f"{fuzz}. "

    return bold_string, std_string, bold_fuzz, std_fuzz

def format_notes(strings):
    '''
    Description:
        Combines all strings in input
    Argument:
        strings:dict
    Returns:
        notes:string
    '''
    notes = ""
    # Give an order to it
    if "noisy" in strings:
        notes += strings["noisy"]
    if "all_spikes" in strings:
        notes += strings["all_spikes"]
    if "fd_dvar_spikes" in strings:
        notes += strings["fd_dvar_spikes"]
    if "bold_wraps" in strings:
        notes += strings["bold_wraps"]
    if "std_wraps" in strings:
        notes += strings["std_wraps"]
    if "bold_fuzz" in strings:
        notes += strings["bold_fuzz"]
    if "std_fuzz" in strings:
        notes += strings["std_fuzz"]
    return notes

def assess_scans(url):
    '''
    Description:
        Opens url's webpage and asks for user inputs on scans. Uses several templates
    Arguments:
        url:string
    Returns:
        assessments:string - string containing every user assessment
    '''
    # Open url
    driver = webdriver.Chrome()
    driver.get(url)

    # Start adding info
    features = "1. Noisy throughout\n2. Spike(s)\n3. Wrap-around\n4. Fuzziness \n5. Done"
    # Holder vars
    notes = {}
    fd_dvars_spikes = set()
    outlier_spikes = set()
    bold_wraps = set()
    std_wraps = set()
    bold_fuzz = set()
    std_fuzz = set()

    while True:
        print("Current Notes:", format_notes(notes))
        print()
        print("What feature would you like to add?")
        print(features)
        print()
        option = int(input("Enter choice: "))
        if option == 1: # Noisy
            if "noisy" in notes: 
                # Delete it if wanted
                choice = input("Want to undo noisiness note? y/n:")
                if choice.lower() == "y":
                    del notes["noisy"]
            else:
                notes["noisy"] = "Noise throughout. "
        elif option == 2: # Spikes
            if "fd_dvar_spikes" in notes or "all_spikes" in notes: 
                # Delete it if wanted
                choice = input("Want to remove all spikes? y/n:")
                if choice.lower() == "y":
                    fd_dvars_spikes = set()
                    outlier_spikes = set()
                    if "all_spikes" in notes:
                        del notes["all_spikes"]
                    if "fd_dvar_spikes" in notes:
                        del notes["fd_dvar_spikes"]
            all_spike_string, fd_dvars_spike_string, fd_dvars_spikes, outlier_spikes = get_spikes(fd_dvars_spikes, outlier_spikes)
            if len(outlier_spikes) > 0:
                notes["all_spikes"] = all_spike_string
            if len(outlier_spikes) != len(fd_dvars_spikes):
                notes["fd_dvar_spikes"] = fd_dvars_spike_string
        elif option == 3: # Wrap-around
            if "bold_wraps" in notes or "std_wraps" in notes:
                 # Delete it if wanted
                choice = input("Want to remove all wrap-arounds? y/n:")
                if choice.lower() == "y":
                    bold_wraps = set()
                    std_wraps = set()
                    if "bold_wraps" in notes:
                        del notes["bold_wraps"]
                    if "std_wraps" in notes:
                        del notes["std_wraps"]
            else:
                bold_string, std_string, bold_wraps, std_wraps = get_wraps(bold_wraps, std_wraps)
                if len(bold_wraps) > 0:
                    notes["bold_wraps"] = bold_string
                if len(std_wraps) > 0:
                    notes["std_wraps"] = std_string
        elif option == 4: # Fuzziness
            if "bold_fuzz" in notes or "std_fuzz" in notes:
                 # Delete it if wanted
                choice = input("Want to remove all fuzziness? y/n:")
                if choice.lower() == "y":
                    bold_fuzz = set()
                    std_fuzz = set()
                    if "bold_fuzz" in notes:
                        del notes["bold_fuzz"]
                    if "std_fuzz" in notes:
                        del notes["std_fuzz"]
            else:
                bold_string, std_string, bold_fuzz, std_fuzz = get_fuzz(bold_fuzz, std_fuzz)
                if len(bold_fuzz) > 0:
                    notes["bold_fuzz"] = bold_string
                if len(std_fuzz) > 0:
                    notes["std_fuzz"] = std_string
        elif option == 5:
            print("Stopping")
            break
        print("Added")
        print()
    
    # Close page
    driver.quit()


    return format_notes(notes)
def get_data(url):
    '''
    Description:
        Goes to url and grabs fd_mean, tsnr, fwhm_x, fwhm_y, fwhm_z, and dvars_std values
    Arguments:
        url:string
    Returns:
        values:dictionary - contains all variables
    '''
    # Open url and prepare html parser
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # Get iqms table data
    table = soup.find("table", {"id": "iqms-table"})

    # Grab values
    fwhm_vars = {"mean", "x", "y", "z"}
    values = {}
    if table:
        # Get all rows of table
        rows = table.find_all("tr")
        for row in rows:
            # Split variable names and values
            cells = row.find_all("td")
            if cells:
                # Look for needed values
                data = [cell.text.strip() for cell in cells]
                if data[0] == "fd" and data[1] == "mean": # fd value
                    values[f"fd_mean"] = data[2]
                elif data[0] == "fwhm": # fwhm values
                    var = data[1]
                    if var in fwhm_vars:
                        values[f"fwhm_{var}"] = data[2]
                elif data[0] == "tsnr": # tsnr value
                    values["tsnr"] = data[1]
                elif data[0] == "dvars" and data[1] == "std": # dvars_std value
                    values["dvars_std"] = data[2]
    return values


def get_updated_rows(starting_row_num, num_rows):
    # Read and update rows
    with open("data/mri_data.csv", "r") as f:
        csvreader = csv.reader(f)
        new_rows = []
        for i,row in enumerate(csvreader):
            if i == 0:
                new_rows.append(row[:8])
            elif (i+1)-starting_row_num >= num_rows:
                last_row = i
                break
            elif i+1 >= starting_row_num:
                print(f"{i-(starting_row_num-1)+1}/{num_rows}")
                new_data = [0]*8
                if row[1] == "Ben":
                    url = row[3]
                    values = get_data(url)
                    notes = assess_scans(url)
                    
                    # Create new row
                    new_data[0] = notes
                    new_data[1] = values["fd_mean"]
                    new_data[2] = values["tsnr"]
                    new_data[3] = values["fwhm_x"]
                    new_data[4] = values["fwhm_y"]
                    new_data[5] = values["fwhm_z"]
                    new_data[6] = values["dvars_std"]    
                else:
                    new_data[0] = "N/A"
                new_data[7] = i
                new_rows.append(new_data)
                

    # Write to output file
    with open("data/output.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(new_rows)
    return last_row


print("\nLast row looked at:", get_updated_rows(starting_row_num=153, num_rows=1))



