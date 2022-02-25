from operator import contains

countPos = 0
employees = []
leaders = []

class Employee(object):
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.vertical = ""
        self.project = ""
        self.initDate = ""
        self.email = ""
        self.location = ""
        self.division = ""
        self.department = ""
        self.title = ""
        self.reportsto = ""
        self.reports = []
        self.totalReports = -1
        self.totalReportsExternals = -1
        self.nodeId = 0
        self.external = False
        self.company = ""

# Process each line internals
def processLineInternal(line):
    fields = line.split(",")
    emp = Employee()
    emp.name = fields[0]
    emp.surname = fields[1]
    emp.vertical = fields[2]
    emp.project = fields[3]
    emp.initDate = fields[4]
    emp.email = fields[5]
    emp.location = fields[6]
    emp.division = fields[7]
    emp.department = fields[8]
    emp.title = fields[9]
    emp.reportsto = fields[10]
    employees.append(emp)
    if emp.name=="Contractors Without Boss":
        emp.external=True
    #print(emp.name + " - " + emp.title)
        


# Process each line internals
def processLineContractors(line):
    fields = line.split(",")
    emp = Employee()
    emp.name = fields[0]
    emp.surname = fields[1]
    emp.email = fields[2]
    emp.vertical = fields[3]
    emp.project = fields[4]
    emp.company = fields[5]
    emp.title = emp.company
    emp.location = fields[6]
    emp.reportsto = fields[7]    
    emp.external = True
    if emp.reportsto=="":
        emp.reportsto = "Contractors"

    #filters
    if emp.vertical=="" or emp.vertical in ["Baja","NO TECH POPULATION","Provider","ES INTERNAL EMPLOYEE","NO MORE IN COMPANY"]:
        print("No Procesa")
        print(emp.name + " - " + emp.title)        
    else:
        employees.append(emp)

# Open the file to read the emploee info. Internal
file1 = open("internal.csv", "r")
Lines = file1.readlines()
file1.close()

# Open the file to read the emploee info. External
file2 = open("contractors.csv", "r")
Lines2 = file2.readlines()
file2.close()

def processLines(lines, contractors):
    firstLine = True
    for line in lines:
        if firstLine:
            #print(line)
            firstLine=False
        else:
            if contractors:
                processLineContractors(line)
            else:                    
                processLineInternal(line)

processLines(Lines, False) #process internals
processLines(Lines2, True)  #process contractors

# Process all the employees and get the leaders list
for emp2 in employees:
    if not(contains(leaders,emp2.reportsto)):
        leaders.append(emp2.reportsto)

def findBoss(employee):
    for emp2 in employees:
        if contains(employee.reportsto,"@"):
            if employee.reportsto == emp2.email:
                #print("Empleado: "+employee.name+" - Jefe: "+emp2.name)
                return emp2                    
        else:
            if contains(employee.reportsto,(emp2.name+" "+emp2.surname)):
                #print("Empleado: "+employee.name+" - Jefe: "+emp2.name)
                return emp2
            else:
                #for contractors case that has same reports than name
                if contains(employee.reportsto,emp2.name):
                    #print("Empleado: "+employee.name+" - Jefe: "+emp2.name)
                    return emp2



sinJefe = []
for emp2 in employees:
    # fiends the boss
    boss = findBoss(emp2)
    if (boss):
        boss.reports.append(emp2)
    else:
        sinJefe.append(emp2)
    
    if emp2.division == "Strategy & Data":
        emp2.division = "BI"

for emp2 in sinJefe:
    print("no-jefe for: --> "+emp2.name+" "+emp2.surname+" - "+emp2.reportsto)


print("Total: ",len(employees))
print("Leaders: ",len(leaders))
print("Sin Jefe: ",len(sinJefe))

def findTop(surname):
    for e in employees:
        if surname == e.surname:
            return e

top = findTop("Tech")
#print(len(top.reports))

def countTotalReports(emp):
    empTotalReports = 0    
    if emp.totalReports==-1:
        for e in emp.reports:
            empTotalReports = empTotalReports + countTotalReports(e) + 1
        emp.totalReports = empTotalReports
    
    return emp.totalReports

def countTotalReportsExternals(emp):
    empTotalReports = 0    
    if emp.totalReportsExternals==-1:

        for e in emp.reports:
            empTotalReports = empTotalReports + countTotalReportsExternals(e)
            if e.external:
                empTotalReports = empTotalReports+1

        emp.totalReportsExternals = empTotalReports
    
    return emp.totalReportsExternals

countTotalReports(top)
countTotalReportsExternals(top)

def separation(character, times):
    repeats = character * times
    return repeats

htmlNodes = []
def transvertalTree(element, num, parentId):
    global countPos
    countPos = countPos +1
    elementId = countPos
    sepa = separation("-",num*4)
    element.nodeId = elementId
    #print(parentId,"-", countPos, sepa," "+element.name + " " + element.surname + " (",len(element.reports),")")
    htmlNodes.append(generateHtmlNode(parentId, countPos, element))
    reports = element.reports
    for report in reports:
        transvertalTree(report,num+1,elementId)


def generateHtmlNode(parentId, countPos, element):
    if parentId==0:
        s1 =  "{ id:"+ str(countPos)+", \"Employee Name\": \""+element.name+" "+element.surname+"\", Title: \""+element.title+"\",Reports:\""+str(len(element.reports))+"("+str(element.totalReports)+")-("+str(element.totalReportsExternals)+")\""+", Vertical: \""+element.vertical+"\", Project: \""+element.project+"\", Department: \""+element.division+"\", Flag: \""+flag(element.location)+"\" },"    
    else:
        s1 =  "{ id:"+ str(countPos)+", pid: "+str(parentId)+", \"Employee Name\": \""+element.name+" "+element.surname+"\", Title: \""+element.title+"\",Reports:\""+str(len(element.reports))+"("+str(element.totalReports)+")-("+str(element.totalReportsExternals)+")\""+", Vertical: \""+element.vertical+"\", Project: \""+element.project+"\", Department: \""+element.division+"\", Flag: \""+flag(element.location)+"\" },"    
    
    return s1

ven = ["CCS-Torre Credicard"]
arg = ["BAI-Phillips","ARG - Kavak HQ","BAI-TOM","BAI-Tigre","BAI-DOT","ROS-Rosario Cinépolis    "]
tur = ["IST-Levent","NAV-Nevşehir"]
bra = ["SAO-Kavak City","SAO-We Work"]
col = ["BOG-Kavak HQ"]
sp = ["MAD-Kavak HQ"]
mx = ["CMX-Moliere",
"GDL-Kavak HQ",
"QRO-Paseo Querétaro",
"MEX-Koliseo-Lerma",
"CMX-Impact Hub",
"GDL-Midtown",
"QRO-Puerta La Victoria",
"MEX-Lerma-2",
"PUE-Explanada",
"QRO-Kaizen",
"MTY-Fashion drive",
"MEX-Tlalnepantla",
"CMX-Patio Santa Fe",
"CMX-Cosmopol",
"CMX-Artz Pedregal",
"CMX-Tlalpan",
"CMX-Capital Reforma",
"CMX-San Angel",
"PUE-Las Torres",
"MTY-Punto Valle",
"GDL-Punto Sur",
"CMX-Mixcoac"]

def flag(location):
    if location in arg:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Argentina_flag_icon.svg/300px-Argentina_flag_icon.svg.png"
    if location in mx:
        return "https://upload.wikimedia.org/wikipedia/commons/c/c0/Mexico_flag_icon.svg"
    if location in bra:
        return "https://upload.wikimedia.org/wikipedia/commons/8/8c/Brazil.png"
    if location in ven:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/HSVenezuela.svg/256px-HSVenezuela.svg.png"
    if location in col:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/HSColombia.svg/256px-HSColombia.svg.png"
    if location in tur:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Turkey_Emblem.png/480px-Turkey_Emblem.png"
    if location in sp:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/HSSpain.svg/256px-HSSpain.svg.png"
    return ""



def generateHtml():
    firstPart = """
<HTML>
	<HEAD>
		<script src="https://balkan.app/js/OrgChart.js"></script>		
		<style>
			html, body {
				margin: 0px;
				padding: 0px;
				width: 100%;
				height: 100%;
				overflow: hidden;
				font-family: Helvetica;
			}
			#tree {
				width: 100%;
				height: 100%;
			}
            [data-n-id='1'] rect {fill: #655d43;}
    """

    secondPart = """
		</style>
	</HEAD>
	<BODY>
		<div id="tree"></div>
		<script>

OrgChart.templates.ana.field_0 = '<text class="field_0" style="font-size: 15px;" fill="#eeeeee" x="130" y="90" text-anchor="middle">{val}</text>';
OrgChart.templates.ana.field_2 = '<text class="field_2" style="font-size: 15px;" fill="#333333" x="210" y="110" text-anchor="middle">{val}</text>';
OrgChart.templates.ana.field_3 = '<text class="field_3" style="font-size: 10px;" fill="#eeeeee" x="20" y="45" text-anchor="left">{val}</text>';
OrgChart.templates.ana.field_4 = '<text class="field_4" style="font-size: 10px;" fill="#eeeeee" x="20" y="60" text-anchor="right">{val}</text>';
OrgChart.templates.ana.field_5 = '<text class="field_5" style="font-size: 15px;" fill="#eeeeee" x="190" y="50" text-anchor="middle">{val}</text>';
OrgChart.templates.ana.field_6 = '<text class="field_4" style="font-size: 15px;" fill="#eeeeee" x="20" y="30" text-anchor="left">{val}</text>';
OrgChart.templates.ana.field_7 = '<text class="field_5" style="font-size: 10px;" fill="#eeeeee" x="20" y="45" text-anchor="left">{val}</text>';
OrgChart.templates.ana.img_1 = '<image preserveAspectRatio="xMidYMid slice" xlink:href="{val}" x="5" y="90" width="30" height="30"></image>';

var chart = new OrgChart(document.getElementById("tree"), {
    template: "ana",
    collapse: {
        level: 2,
        allChildren: true        
    },
    mouseScrool: OrgChart.none,
    nodeBinding: {
        field_0: "Employee Name",
        field_1: "Title",
        field_2: "Reports",
        field_3: "Vertical",
        field_4: "Project",
        field_5: "Company",
        field_6: "Department",
        field_7: "mail",
        img_1: "Flag"
    }
});

chart.load([        
    """

    middlePart = ""
    for node in htmlNodes:
        #print(node)
        middlePart = middlePart+node+"\n"
    
    Remove_last = middlePart[:-2]
    
    lastPart = """    
]);

		</script>
	</BODY>
</HTML>
"""

    return firstPart+generateColors()+secondPart+Remove_last+lastPart

def generateColors():
    str1 = ""
    for e in employees:

        if e.external:
            str1 = str1 + "[data-n-id='"+str(e.nodeId)+"'] rect {fill: #e32323f9;}"+"\n"
        else:
            if e.division=="Producto" and e.department=="UX":
                str1 = str1 + "[data-n-id='"+str(e.nodeId)+"'] rect {fill: #038a39;}"+"\n"
            else:
                if e.division=="Producto":
                    str1 = str1 + "[data-n-id='"+str(e.nodeId)+"'] rect {fill: #8d88e8f9;}"+"\n"

            if e.division=="BI":
                str1 = str1 + "[data-n-id='"+str(e.nodeId)+"'] rect {fill: #c9b906;}"+"\n"     

    return str1

transvertalTree(top,0,0)
html = generateHtml()
file2 = open("pipi.html", "w")
file2.write(html)
file2.close()