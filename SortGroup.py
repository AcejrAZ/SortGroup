import csv,os,sys
from collections import Counter

class my_main(object):
    def __init__(self):
        self.filepath="C:\\Users\\venturf2\\Google Drive\\Theta Tau\\WesternRegion\\RegionalConference\\Regionals - 14Fall_PiD\\RegisteredStudents.csv"
        csvfile = open(self.filepath, 'rb')
        myreader = csv.reader(csvfile, delimiter=',')

        self.mydict = {}
        chapters = []
        majors = []
        grads = []
        genders = []
        for i,row in enumerate(myreader):
            if not i :
                continue
            name,gender,chapter,major,grad = row
            self.mydict[name] = [chapter,major,grad,gender]
            chapters.append(chapter)
            majors.append(major)
            grads.append(grad)
            genders.append(gender)
        self.chapters_count = Counter(chapters)
        self.majors_count = Counter(majors)
        self.grads_count = Counter(grads)
        self.genders_count = Counter(genders)
        self.chapter_names=self.chapters_count.keys()
        self.major_names=self.majors_count.keys()
        self.grad_names=self.grads_count.keys()
        self.gender_names=self.genders_count.keys()
        total = len(self.mydict)
        number_groups = 40
        self.grouplist = {}
        for group_num in range(number_groups):
            self.grouplist["name"+str(group_num)]=my_group("name"+str(group_num))
            attributes=self.chapter_names,self.major_names,self.grad_names,self.gender_names
            self.grouplist["name"+str(group_num)].add_attributes(attributes)

    def item_type(self,item_name):
        if item_name in self.chapter_names:
            return "chapters"
        if item_name in self.major_names:
            return "majors"
        if item_name in self.grad_names:
            return "grads"
        if item_name in self.gender_names:
            return "genders"

    def get_min_groups(self,item=None):
        "chapter,major,grad = item"
        len_list = {}
        for group in self.grouplist:
            if item is not None:
                group_length=self.grouplist[group].item_in_group(item)
            else:
                group_length=self.grouplist[group].group_length()
            try: len_list[group_length].append(group)
            except KeyError: len_list[group_length] = [group]
        min_key = min(len_list.keys())
        return len_list[min_key]

    def create_groups(self):
        for member in self.mydict:
            best_group=self.find_best_group(self.mydict[member])
            self.grouplist[best_group].add_person(member,self.mydict[member])
            self.mydict[member].append(best_group)

    def output(self):
        filepath=os.path.splitext(self.filepath)[0]+"_OUT.csv"
        csvfile = open(filepath, 'wb')
        mywriter = csv.writer(csvfile, delimiter=',')
        mywriter.writerow(["name","chapter","major","grad","gender","group"])
        for member in self.mydict:
            out=[member]
            out.extend(self.mydict[member])
            mywriter.writerow(out)

    def find_best_group(self,items):
        min_groups=self.get_min_groups()
        for item in items:
            min_groups.extend(self.get_min_groups(item))
#        print min_groups
        group_counts=Counter(min_groups)
        max_value=max(group_counts.values())
        return self.key_from_value(group_counts, max_value)

    def key_from_value(self,mydict,value):
        for item in mydict:
            if mydict[item]==value:
                return item

    def show_variance(self):
        for group in self.grouplist:
            print Counter(self.grouplist[group].majors_in_group)
            print Counter(self.grouplist[group].chapters_in_group)
            print Counter(self.grouplist[group].grads_in_group)
            print Counter(self.grouplist[group].genders_in_group)

class my_group(my_main):
    def __init__(self,group_name):
        self.group_name=group_name
        self.chapters_in_group=[]
        self.majors_in_group=[]
        self.grads_in_group=[]
        self.genders_in_group=[]
        self.members_in_group=[]
        self.list_names={
                        "chapters_in_group":self.chapters_in_group,
                        "majors_in_group":self.majors_in_group,
                        "grads_in_group":self.grads_in_group,
                        "genders_in_group":self.genders_in_group
                        }
    def add_attributes(self,attributes):
        chapter_names,major_names,grad_names,gender_names=attributes
        self.chapter_names=chapter_names
        self.major_names=major_names
        self.grad_names=grad_names
        self.gender_names=gender_names

    def group_length(self):
        return len(self.members_in_group)

    def add_person(self,member_name,member_items):
        chapter,major,grad,gender = member_items
        self.chapters_in_group.append(chapter)
        self.majors_in_group.append(major)
        self.grads_in_group.append(grad)
        self.genders_in_group.append(gender)
        self.members_in_group.append(member_name)

    def item_type(self,item_name):
        if item_name in self.chapter_names:
            return "chapters"
        if item_name in self.major_names:
            return "majors"
        if item_name in self.grad_names:
            return "grads"
        if item_name in self.gender_names:
            return "genders"

    def item_in_group(self,item_name):
        list_type=self.item_type(item_name)
        list_name=list_type+"_in_group"
        in_list=self.list_names[list_name]
        if item_name in in_list:
            counts = Counter(in_list)
            return counts[item_name]
        else: return 0

