import csv
import os
import sys
from collections import Counter
mypath = "C:\\Users\\venturf2\\Downloads\\RegistrationSP15.csv"
number_groups = 30


class my_main():
    def __init__(self, mypath, number_groups):
        self.mypath = mypath
        csvfile = open(mypath, 'rb')
        myreader = csv.reader(csvfile, delimiter=',')

        self.mydict = {}
        mylists = {}
        for i, row in enumerate(myreader):
            for j, item in enumerate(row):
                if j != 0:
                    if i == 0:
                        mylists[j-1] = [item]
                        continue
                    mylists[j-1].append(item)
            self.mydict[row[0]] = row[1:]  # Need to check this
        self.list_count = {}
        self.list_names = {}
        for i, num in enumerate(mylists):
            self.list_count[i] = Counter(mylists[num])
            self.list_names[i] = self.list_count[i].keys()
        total = len(self.mydict)
        self.grouplist = {}
        for group_num in range(number_groups):
            self.grouplist["name"+str(group_num)] = my_group("name"+str(group_num))
            self.grouplist["name"+str(group_num)].add_attributes(self.list_names)

    def item_type(self, item_name):
        for num in self.list_names:
            if item_name in self.list_names[num]:
                return num

    def get_min_groups(self, item=None):
        "chapter,major,grad = item"
        len_list = {}
        for group in self.grouplist:
            if item is not None:
                group_length = self.grouplist[group].item_in_group(item)
            else:
                group_length = self.grouplist[group].group_length()
            try:
                len_list[group_length].append(group)
            except KeyError:
                len_list[group_length] = [group]
        min_key = min(len_list.keys())
        return len_list[min_key]

    def create_groups(self):
        for member in self.mydict:
            best_group = self.find_best_group(self.mydict[member])
            self.grouplist[best_group].add_person(member, self.mydict[member])
            self.mydict[member].append(best_group)

    def output(self):
        filepath = os.path.splitext(self.mypath)[0]+"_OUT.csv"
        csvfile = open(filepath, 'wb')
        mywriter = csv.writer(csvfile, delimiter=',')
        mywriter.writerow(["name", "chapter", "major", "grad", "role",
                           "gender", "group", "group2"])
        for member in self.mydict:
            out = [member]
            out.extend(self.mydict[member])
            mywriter.writerow(out)

    def find_best_group(self, items):
        min_groups = self.get_min_groups()
        for item in items:
            min_groups.extend(self.get_min_groups(item))
#        print min_groups
        group_counts = Counter(min_groups)
        max_value = max(group_counts.values())
        return self.key_from_value(group_counts, max_value)

    def key_from_value(self, mydict, value):
        for item in mydict:
            if mydict[item] == value:
                return item

    def show_variance(self):
        for group in self.grouplist:
            for num in self.list_names:
                print(Counter(self.grouplist[group].list_names[num]))


class my_group():
    def __init__(self, group_name):
        self.group_name = group_name
        self.items_in_group = {}
        self.members_in_group = []

    def add_attributes(self, attributes):
        self.list_names = attributes
        for i, item in enumerate(attributes):
            self.items_in_group[i] = []

    def group_length(self):
        return len(self.members_in_group)

    def add_person(self, member_name, member_items):
        for i, item in enumerate(member_items):
            self.items_in_group[i].append(item)
        self.members_in_group.append(member_name)

    def item_type(self, item_name):
        for num in self.list_names:
            if item_name in self.list_names[num]:
                return num

    def item_in_group(self, item_name):
        list_type = self.item_type(item_name)
        item_list = self.items_in_group[list_type]
        if item_name in item_list:
            counts = Counter(item_list)
            return counts[item_name]
        else:
            return 0

