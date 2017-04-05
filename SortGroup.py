import csv
import os
import sys
from copy import deepcopy
from collections import Counter
mypath = r"E:\ThetaTau Drive\Theta Tau\WesternRegion\RegionalConference\Regionals - 17Spring_OG"
mypath = os.path.join(mypath, r"Export_groups.csv")
'''
from regionals import SortGroup
test = SortGroup.GroupCreation(SortGroup.mypath)
test.add_supergroup("GroupA", num_of_subgroups=17)
test.create_all_subgroups()
test.add_supergroup("GroupB", size_of_subgroups=5)
test.create_all_subgroups()
test.output()
'''


class GroupCreation():
    def __init__(self, mypath):
        self.supergroups = []
        self.mypath = mypath
        csvfile = open(mypath, 'r')
        myreader = csv.reader(csvfile, delimiter=',')

        self.mydict = {}
        self.list_names = {}
        for i, row in enumerate(myreader):
            if i == 0:
                headers = row
                self.list_names = {header: [] for header in row}
                header_locs = {loc: header for loc, header in
                               enumerate(row)}
                continue
            for j, item in enumerate(row):
                if item == "":
                    continue
                self.list_names[header_locs[j]].append(item)
            self.mydict[self.list_names['First'][i-1] +
                        self.list_names['Last'][i-1]] = dict(zip(headers,
                                                                 row))
        self.list_count = {num: Counter(self.list_names[num])
                           for num in self.list_names.keys()}

    def add_supergroup(self, supergroup_name=None, size_of_subgroups=20,
                       num_of_subgroups=None):
        self.supergroups.append(Supergroup(self.mydict,
                                           supergroup_name,
                                           size_of_subgroups,
                                           num_of_subgroups))

    def create_all_subgroups(self):
        for supergroup in self.supergroups:
            supergroup.create_groups()
            supergroup.groups_out()

    def output(self):
        filepath = os.path.splitext(self.mypath)[0]+"_OUT.csv"
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = list(self.mydict[list(self.mydict.keys())[0]].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for member in self.mydict:
                writer.writerow(self.mydict[member])


class Supergroup():
    def __init__(self, mydict, supergroup_name=None, size_of_subgroups=20,
                 num_of_subgroups=None):
        '''
        supergroup_name
        size_of_subgroups
        num_of_subgroups
        '''
        self.supergroup_name = supergroup_name
        self.mydict_orig = mydict
        self.mydict = deepcopy(mydict)
        self.grouplist = {}
        self.headers = list(self.mydict[list(self.mydict.keys())[0]].keys())
        if num_of_subgroups is None:
            total = len(self.mydict)
            num_of_subgroups = int(total/size_of_subgroups)
        for group_num in range(num_of_subgroups):
            self.grouplist[str(group_num)] = subgroup(str(group_num),
                                                      self.headers)
        if self.supergroup_name in self.headers:
            for member in list(self.mydict.keys()):
                group_num = self.mydict[member][self.supergroup_name]
                if group_num not in ["", "NA"]:
                    self.grouplist[str(group_num)].add_person(member,
                                                              self.mydict[member])
                    self.mydict.pop(member)
        else:
            self.headers.append(self.supergroup_name)

    def create_groups(self):
        for member in self.mydict:
            best_group = self.find_best_group(self.mydict[member])
            self.grouplist[best_group].add_person(member, self.mydict[member])
            self.mydict[member][self.supergroup_name] = best_group

    def find_best_group(self, member_dict):
        min_groups = self.get_min_groups()
        for item_type, item in member_dict.items():
            if item_type not in ['First', 'Last', self.supergroup_name]:
                min_groups.extend(self.get_min_groups(item, item_type))
        group_counts = Counter(min_groups)
        max_value = max(group_counts.values())
        return self.key_from_value(group_counts, max_value)

    def get_min_groups(self, item=None, item_type=None):
        len_list = {}
        for group in self.grouplist:
            if item is not None:
                group_length = self.grouplist[group].item_in_group(item,
                                                                   item_type)
            else:
                group_length = self.grouplist[group].group_length()
            try:
                len_list[group_length].append(group)
            except KeyError:
                len_list[group_length] = [group]
        min_key = min(len_list.keys())
        return len_list[min_key]

    def key_from_value(self, mydict, value):
        for item in mydict:
            if mydict[item] == value:
                return item

    def show_variance(self):
        for group in self.grouplist:
            for num in self.list_names:
                print(Counter(self.grouplist[group].list_names[num]))

    def groups_out(self):
        for member in self.mydict:
            self.mydict_orig[member][self.supergroup_name] = \
                self.mydict[member][self.supergroup_name]


class subgroup():
    def __init__(self, group_name, headers):
        self.group_name = group_name
        self.items_in_group = {}
        self.members_in_group = []
        self.list_names = headers
        self.items_in_group = {item: [] for item in headers
                               if item not in ['First', 'Last']}

    def group_length(self):
        return len(self.members_in_group)

    def add_person(self, member_name, member_dict):
        for key, value in member_dict.items():
            if key not in ['First', 'Last']:
                self.items_in_group[key].append(value)
        self.members_in_group.append(member_name)

    def item_in_group(self, item=None, item_type=None):
        item_list = self.items_in_group[item_type]
        if item in item_list:
            counts = Counter(item_list)
            return counts[item]
        else:
            return 0
