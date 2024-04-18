from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver


# Scrap values
# Template notes - Idea: Open link and show user the site to scroll through. Close when done
# Ex: Spikes at t=X1, t=X2..., Noisy throughout, [Nothing], Wrap-around at [], etc.



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
    print(values) 


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
    for i, spike in enumerate(fd_dvars_spikes):
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
    for s in strings.values():
        notes += s
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
    features = "1. Noisy throughout\n2. Spike(s)\n3. Wrap-around\n4. \n5. Done"
    # Holder vars
    notes = {}
    fd_dvars_spikes = set()
    outlier_spikes = set()
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
                notes["noisy"] = "Noisy throughout. "
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
            else:
                all_spike_string, fd_dvars_spike_string, fd_dvars_spikes, outlier_spikes = get_spikes(fd_dvars_spikes, outlier_spikes)
                if len(outlier_spikes) > 0:
                    notes["all_spikes"] = all_spike_string
                if len(outlier_spikes) != len(fd_dvars_spikes):
                    notes["fd_dvar_spikes"] = fd_dvars_spike_string
        elif option == 3: # Wrap-around
            pass
        elif option == 4:
            pass
        elif option == 5:
            print("Stopping")
            break
        print("Added")
        print()
    
    # Close page
    driver.quit()


    return format_notes(notes)

url = "https://joanna-hernandez.github.io/mriqc-PSANDS/sub-103_ses-1_task-SRT_bold.html"
# get_data(url)
print(assess_scans(url))

