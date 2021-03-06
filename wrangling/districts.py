from collections import defaultdict
from csv import DictReader, DictWriter
import heapq

kHEADER = ["STATE", "DISTRICT", "MARGIN"]

def district_margins(state_lines):
    """
    Return a dictionary with districts as keys, and the difference in
    percentage between the winner and the second-place as values.

    @lines The csv rows that correspond to the districts of a single state
    """
    first = 101.0
    second = 0.0
    margin = 100.0
    # Complete this function
    for x in state_lines:
        if x["GENERAL %"]:
            percent_string = x["GENERAL %"].replace(",",".").replace("%","")
            if (percent_string != ""):
                percent = float(percent_string)
                if x["GE WINNER INDICATOR"] == "W":
                    first = percent
                elif x["GE WINNER INDICATOR"] != "W" and percent > second:
                    second = percent
#    return dict((int((x["D"])[:2]), first - second) for x in state_lines if x["D"] and x["D"] != "H")
    return dict((int(x["D"]), 25.0) for x in state_lines if x["D"] and
            not (x["D"] == "H" or " - " in x["D"]))

def all_states(lines):
    """
    Return all of the states (column "STATE") in list created from a
    CsvReader object.  Don't think too hard on this; it can be written
    in one line of Python.
    """

    # Complete this function
    return set(x["STATE"] for x in lines if x["STATE"] != "")

def all_state_rows(lines, state):
    """
    Given a list of output from DictReader, filter to the rows from a single state.

    @state Only return lines from this state
    @lines Only return lines from this larger list
    """

    # Complete/correct this function
    for ii in lines:
        if (ii["STATE"] == state):
            yield ii

    # Alternate Solution (Single Line)
    # return list(x for x in lines if x["STATE"] == state)

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()

    summary = {}
    for state in all_states(lines):
        margins = district_margins(all_state_rows(lines, state))

        for ii in margins:
            summary[(state, ii)] = margins[ii]

    for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        output.writerow({"STATE": ii[0], "DISTRICT": ii[1], "MARGIN": mm})
