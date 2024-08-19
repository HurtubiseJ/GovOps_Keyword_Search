#rg_search.py
#This file takes in search parameters and performs a search through local contact data to find matches
#Final version will assume .txt files already exsist within local storage
#The file currently uses PyMuPDF to covert PDF files to .txt

import subprocess
import json
import re
#Function RETURNS: a regex string to search for NAICS codes. Noter: this functs all 6 digit numbers.
def create_NAICS_regex():
    expression = "\\b(?i)(NAICS)\\b"
    return expression

#Function RETURNS: a regex string to search for preferred clients and customers. 
#TODO: This will most likly be a DB call, what info do I need to pass into func to make DB call?
#TODO: Change expression once this is figured out 
def create_Preferred_Clients_Customers_regex():
    expression = "Client List"
    return expression

#self explanitory
def create_PSC_regex():
    expression = "\\b(PSC|Product and Services Code|product and services code)\\b"
    return expression 

def create_Project_Location_regex():
    expression = "located|location"
    return expression

def create_Contract_Vehicles_regex():
    expression = "\\b(MAC|Government-wide|Multiple agency contract|governmentwide|MAC|IDIQ|GSA)\\b"
    return expression

#Socioeconomic status
def create_SES_regex():
    expression = 'cost|budget'
    return expression
#socioecomic program
def create_SEP_regex():
    expression = 'reserved for|program'
    return expression

#Department
def create_DEP_regex():
    expression = 'Department of'
    return expression

#Security Clearance
def create_SC_regex():
    expression = "Clearance|clearance"
    return expression

#Facility securtity clearance
def create_FacSC_regex():
    expression = "(?i)facility clearance"
    return expression

#Personnel Security Clearance
def create_PerSC_regex():
    expression = "(?i)personnel clearance"
    return expression

def create_PopStreetAddress_regex():
    expression = 'place of performance'
    return expression

def create_PopCity_regex():
    expression = 'place of performance'
    return expression

def create_PopState_regex():
    expression = 'place of performance'
    return expression

def create_PopZip_regex():
    expression = 'zip code|place of performance'
    return expression

def create_PopCountry_regex():
    expression = 'country|place of performance'
    return expression

def create_City_regex():
    expression = 'city'
    return expression

def create_State_regex():
    expression = 'state'
    return expression

def create_CountryCode_regex():
    expression = 'location|country|country code'
    return expression

def create_ZipCode_regex():
    expression = 'zipcode|zip-code'
    return expression

def create_AwardNumber_regex():
    expression = '(?i)(award).*(number)'
    return expression

def create_AwardDate_regex():
    expression = '(?i)(award).*(date)'
    return expression

def create_AwardMoney_regex():
    expression = '(?i)(award).*(amount|money|total)'
    return expression

def create_Awardee_regex():
    expression = 'awarded to|awardee'
    return expression

def create_PrimaryContactTitle_regex():
    expression = '(?i)(primary).*(title)|primary contact'
    return expression

def create_PrimaryContactFullname_regex():
    expression = '(?i)(primary).*(name)|primary contact'
    return expression

def create_PrimaryContactEmail_regex():
    expression = '(?i)(primary).*(email|contact)|primary contact'
    return expression

def create_PrimaryContactPhone_regex():
    expression = '(?i)(primary).*(number|phone)|primary contact'
    return expression

def create_PrimaryContactFax_regex():
    expression = '(?i)(primary).*(fax)|primary contact'
    return expression

def create_SecondaryContactTitle_regex():
    expression = '(?i)(secondary).*(title)|secondary contact'
    return expression

def create_SecondaryContactFullname_regex():
    expression = '(?i)(secondary).*(name)|secondary contact'
    return expression

def create_SecondaryContactEmail_regex():
    expression = '(?i)(secondary).*(email)|secondary contact'
    return expression

def create_SecondaryContactPhone_regex():
    expression = '(?i)(secondary).*(phone)|secondary contact'
    return expression

def create_SecondaryContactFax_regex():
    expression = '(?i)(secondary).*(fax)|secondary contact'
    return expression

def create_SetASideCode_regex():#same as SEP
    expression = 'reserved for|program'
    return expression

#Used to add regex expression together to search for multiple params
#might do this in function as calls are expensive
def add_or_regex():
    expression = "|"
    return expression

def checkKeyWords(keyWordsList, text):
    regex = keyWordsList[0]
    found = re.search(regex, text)
    if found != None:
        return True
    return False

#Function to create rg search command default is for all search params to be found, approach most likly will only work for string to string matches
def create_rg_search_command(deselectParam, filepath):
    #List of default search params
    find_NAICS = True 
    find_Preferred_Clients_Customers = True 
    find_PSC = True
    find_Project_Locations = True
    find_Contract_Vehicles = True 
    find_SES = True 
    find_SEP = True
    find_DEP = True
    find_SC = True
    find_PerSC = True
    find_FacSC = True
    find_SetASideCode = True

    #Location
    find_PopStreetAddress = True
    find_PopCity = True
    find_PopState = True
    find_PopZip = True
    find_PopCountry = True
    find_State = True
    find_City = True
    find_ZipCode = True
    find_CountryCode = True
    #Award details
    find_AwardNumber = True
    find_AwardDate = True
    find_AwardMoney = True
    find_Awardee = True
    #Contacts
    find_PrimaryContactTitle = True
    find_PrimaryContactFullname = True 
    find_PrimaryContactEmail = True 
    find_PrimaryContactPhone = True
    find_PrimaryContactFax = True
    find_SecondaryContactTitle = True
    find_SecondaryContactFullname = True 
    find_SecondaryContactEmail = True 
    find_SecondaryContactPhone = True
    find_SecondaryContactFax = True

    search_list = ['NaicsCode', 'PreferredClientsCustomers', 'PSC', "ProjectLocations", "ContractVehicles", 'SES', 'SEP', 'DEP', 'SC', 'PerSC', 'FacSC', 'PopStreetAddress', 'PopCity', 'PopState', 'PopZip', 'PopCountry', 'State', "City", 'ZipCode', "CountryCode", 'AwardNumber', 'AwardDate', 'AwardMoney', 'Awardee', 'PrimaryContactTitle', 'PrimaryContactFullname', "PrimaryContactEmail", "PrimaryContactPhone", 'PrimaryContactFax', 'SecondaryContactTitle', 'SecondaryContactFullname', 'SecondaryContactEmail', 'SecondaryContactPhone', 'SecondaryContactFax', 'SetASideCode']

    for param in deselectParam: 
        match param:
            case "NaicsCode": #NaicsCode
                find_NAICS = False 
                search_list.remove('NaicsCode')
            case "PreferredClientsCustomers":
                find_Preferred_Clients_Customers = False 
                search_list.remove('PreferredClientsCustomers')
            case "PSC":
                find_PSC = False
                search_list.remove('PSC')
            case "ProjectLocations":
                find_Project_Locations = False
                search_list.remove('ProjectLocations')
            case "ContractVehicles":
                find_Contract_Vehicles = False
                search_list.remove('ContractVehicles')
            case 'SES':
                find_SES = False
                search_list.remove('SES')
            case "SEP": #SetASide SetASideCode?
                find_SEP = False
                search_list.remove('SEP')
            case "DEP": #Department/Ind.Agency
                find_DEP = False
                search_list.remove('DEP')
            case "SC":
                find_SC = False
                search_list.remove('SC')
            case "PerSC":
                find_PerSC = False
                search_list.remove('PerSC')
            case "FacSC":
                find_FacSC = False
                search_list.remove('FacSC')
            case "PopStreetAddress":
                find_PopStreetAddress = False 
                search_list.remove('PopStreetAddress')
            case "PopCity":
                find_PopCity = False
                search_list.remove('PopCity')
            case "PopState":
                find_PopState = False 
                search_list.remove('PopState')
            case "PopZip":
                find_PopZip = False
                search_list.remove('PopZip')
            case "PopCountry":
                find_PopCountry = False
                search_list.remove('PopCountry')
            case "State":
                find_State = False
                search_list.remove('State')
            case "City":
                find_City = False
                search_list.remove('City')
            case "ZipCode":
                find_ZipCode = False
                search_list.remove('ZipCode')
            case "CountryCode":
                find_CountryCode = False
                search_list.remove('CountryCode')
            case "AwardNumber":
                find_AwardNumber = False
                search_list.remove('AwardNumber')
            case "AwardDate":
                find_AwardDate = False
                search_list.remove('AwardDate')
            case "AwardMoney":
                find_AwardMoney = False
                search_list.remove('AwardMoney')
            case "Awardee":
                find_Awardee = False
                search_list.remove('Awardee')
            case "PrimaryContactTitle":
                find_PrimaryContactTitle = False
                search_list.remove('PrimaryContactTitle')
            case "PrimaryContactFullname":
                find_PrimaryContactFullname = False
                search_list.remove('PrimaryContactFullname')
            case "PrimaryContactEmail":
                find_PrimaryContactEmail = False
                search_list.remove('PrimaryContactEmail')
            case "PrimaryContactPhone":
                find_PrimaryContactPhone = False
                search_list.remove('PrimaryContactPhone')
            case "PrimaryContactFax":
                find_PrimaryContactFax = False
                search_list.remove('PrimaryContactFax')
            case "SecondaryContactTitle":
                find_SecondaryContactTitle = False
                search_list.remove('SecondaryContactTitle')
            case "SecondaryContactFullname":
                find_SecondaryContactFullname = False
                search_list.remove('SecondaryContactFullname')
            case "SecondaryContactEmail":
                find_SecondaryContactEmail = False
                search_list.remove('SecondaryContactEmail')
            case "SecondaryContactPhone":
                find_SecondaryContactPhone = False
                search_list.remove('SecondaryContactPhone')
            case "SecondaryContactFax":
                find_SecondaryContactFax = False
                search_list.remove('SecondaryContactFax')
            case "SetASideCode":
                find_SetASideCode = False
                search_list.remove('SetASideCode')
    
    #section to create regex searches
    regex_expression = ""
    multi_search = False
    if find_NAICS:
        multi_search = True
        regex_expression += create_NAICS_regex()
    if find_Preferred_Clients_Customers:
        if multi_search: 
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_Preferred_Clients_Customers_regex()
    if find_PSC:
        if multi_search: 
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PSC_regex()
    if find_Project_Locations:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_Project_Location_regex()
    if find_Contract_Vehicles:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True 
        regex_expression += create_Contract_Vehicles_regex()
    if find_SES:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True 
        regex_expression += create_SES_regex()
    if find_SEP:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True 
        regex_expression += create_SEP_regex()
    if find_DEP:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_DEP_regex()
    if find_SC:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SC_regex()
    if find_PerSC:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PerSC_regex()
    if find_FacSC:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_FacSC_regex()
    if find_PopStreetAddress:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PopStreetAddress_regex()
    if find_PopCity:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PopCity_regex()
    if find_PopState:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PopCity_regex()
    if find_PopZip:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PopZip_regex()
    if find_PopCountry:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PopCountry_regex()
    if find_State:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_State_regex()
    if find_City:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PopCity_regex()
    if find_ZipCode:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_ZipCode_regex()
    if find_CountryCode:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_CountryCode_regex()
    if find_AwardNumber:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_AwardNumber_regex()
    if find_AwardDate:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_AwardDate_regex()
    if find_AwardMoney:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_AwardMoney_regex()
    if find_Awardee:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_Awardee_regex()
    if find_PrimaryContactTitle:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PrimaryContactTitle_regex()
    if find_PrimaryContactFullname:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PrimaryContactFullname_regex()
    if find_PrimaryContactEmail:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PrimaryContactEmail_regex()
    if find_PrimaryContactPhone:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PrimaryContactPhone_regex()
    if find_PrimaryContactFax:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_PrimaryContactFax_regex()
    if find_SecondaryContactTitle:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SecondaryContactTitle_regex()
    if find_SecondaryContactFullname:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SecondaryContactFullname_regex()
    if find_SecondaryContactEmail:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SecondaryContactEmail_regex()
    if find_SecondaryContactPhone:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SecondaryContactPhone_regex()
    if find_SecondaryContactFax:
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SecondaryContactFax_regex()
    if find_SetASideCode: 
        if multi_search:
            regex_expression += add_or_regex()
        multi_search = True
        regex_expression += create_SetASideCode_regex()
    
    rg_command = ["rg",  "--pre", r'/home/taco/Desktop/SearchScripts/preprocessor.sh', "--after-context=4", "--word-regexp", "--ignore-case",  rf'{regex_expression}', rf'{filepath}'] #removes preprocess overhead     
    return rg_command, search_list

#This function runs ripgrep search using subprocess.run(), output behavior might change, currently RETURN:
#a string of the terminal output(ripgrep matches)
#INPUT: is a list of params to not search, default is to search all implemented params
#TODO: input param will deselect parameters to search, by inputing 'NAICS', rg call will not search for NAICS code. Default is to search all
def run_rg_search(deselectParam, filepath):
    inputCommand, search_list = create_rg_search_command(deselectParam, filepath)
    output = subprocess.run(inputCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    terminalText = output.stdout.decode('utf-8')
    return terminalText, search_list

#this function takes rg matches, INPUT: terminal output split by \n, and creates JSON of the matches. This is nessesary to get total matches and what searchParam matched.
#TODO: Change file paths once implimented
def create_AllMatches_JSON(textList, search_list, added_df):
    
    #clean textList
    cleanedtext = []
    for text in textList:
        newTxt = text.replace("\n", " ")
        file = newTxt.split(":")[0]
        newTxt = newTxt.replace(file, "")
        newTxt = newTxt.replace("-", " ")
        newTxt = newTxt.replace("•", " ")
        # newTxt = newTxt.replace("", "")
        newTxt = file + newTxt
        cleanedtext.append(newTxt) 
    ###Beginning of Search process###

    #avoid repeats
    myFileObjList = FileObjList()

    #regex strings for each param
    curRegex = ""
    #PSC does not have word boundary at end, need to account for ,. ect
    
    regexPerSC = '\\b(?i)(?P<SC>top secret|secret|confidential|Q|L)\\b'
    checkPerSC = create_PerSC_regex()
    regexFacSC = "\\b(?i)(?P<SC>top secret|secret|confidential|Q|L)\\b"
    checkFacSC = create_FacSC_regex()
    #TODO: figure out how to select contract vehicles
    regexContractVehicles = "con vehicles NONEPLACEHOLD"
    checkContractVehicles = create_Contract_Vehicles_regex()

    regexSetASideCode = '(?P<SetASideCode>FAR\s19\.\d{1,3}(?:-\d)?(?:-\d{1,3})?|DFARS?\s\d{3}\.\d{3,4})'
    checkSetASideCode = create_SetASideCode_regex()
    regexNAICS = "(?P<NAICS>111110|111120|111130|111140|111150|111160|111191|111199|111211|111219|111310|111320|111331|111332|111333|111334|111335|111336|111339|111411|111419|111421|111422|111910|111920|111930|111940|111991|111992|111998|112111|112112|112120|112130|112210|112310|112320|112330|112340|112390|112410|112420|112511|112512|112519|112910|112920|112930|112990|113110|113210|113310|114111|114112|114119|114210|115111|115112|115113|115114|115115|115116|115210|115310|211120|211130|212114|212115|212210|212220|212230|212290|212311|212312|212313|212319|212321|212322|212323|212390|213111|213112|213113|213114|213115|221111|221112|221113|221114|221115|221116|221117|221118|221121|221122|221210|221310|221320|221330|236115|236116|236117|236118|236210|236220|237110|237120|237130|237210|237310|237990|238110|238120|238130|238140|238150|238160|238170|238190|238210|238220|238290|238310|238320|238330|238340|238350|238390|238910|238990|311111|311119|311211|311212|311213|311221|311224|311225|311230|311313|311314|311340|311351|311352|311411|311412|311421|311422|311423|311511|311512|311513|311514|311520|311611|311612|311613|311615|311710|311811|311812|311813|311821|311824|311830|311911|311919|311920|311930|311941|311942|311991|311999|312111|312112|312113|312120|312130|312140|312230|313110|313210|313220|313230|313240|313310|313320|314110|314120|314910|314994|314999|315120|315210|315250|315990|316110|316210|316990|321113|321114|321211|321212|321215|321219|321911|321912|321918|321920|321991|321992|321999|322110|322120|322130|322211|322212|322219|322220|322230|322291|322299|323111|323113|323117|323120|324110|324121|324122|324191|324199|325110|325120|325130|325180|325193|325194|325199|325211|325212|325220|325311|325312|325314|325315|325320|325411|325412|325413|325414|325510|325520|325611|325612|325613|325620|325910|325920|325991|325992|325998|326111|326112|326113|326121|326122|326130|326140|326150|326160|326191|326199|326211|326212|326220|326291|326299|327110|327120|327211|327212|327213|327215|327310|327320|327331|327332|327390|327410|327420|327910|327991|327992|327993|327999|331110|331210|331221|331222|331313|331314|331315|331318|331410|331420|331491|331492|331511|331512|331513|331523|331524|331529|332111|332112|332114|332117|332119|332215|332216|332311|332312|332313|332321|332322|332323|332410|332420|332431|332439|332510|332613|332618|332710|332721|332722|332811|332812|332813|332911|332912|332913|332919|332991|332992|332993|332994|332996|332999|333111|333112|333120|333131|333132|333241|333242|333243|333248|333310|333413|333414|333415|333511|333514|333515|333517|333519|333611|333612|333613|333618|333912|333914|333921|333922|333923|333924|333991|333992|333993|333994|333995|333996|333998|334111|334112|334118|334210|334220|334290|334310|334412|334413|334416|334417|334418|334419|334510|334511|334512|334513|334514|334515|334516|334517|334519|334610|335131|335132|335139|335210|335220|335311|335312|335313|335314|335910|335921|335929|335931|335932|335991|335999|336110|336120|336211|336212|336213|336214|336310|336320|336330|336340|336350|336360|336370|336390|336411|336412|336413|336414|336415|336419|336510|336611|336612|336991|336992|336999|337110|337121|337122|337126|337127|337211|337212|337214|337215|337910|337920|339112|339113|339114|339115|339116|339910|339920|339930|339940|339950|339991|339992|339993|339994|339995|339999|423110|423120|423130|423140|423210|423220|423310|423320|423330|423390|423410|423420|423430|423440|423450|423460|423490|423510|423520|423610|423620|423690|423710|423720|423730|423740|423810|423820|423830|423840|423850|423860|423910|423920|423930|423940|423990|424110|424120|424130|424210|424310|424340|424350|424410|424420|424430|424440|424450|424460|424470|424480|424490|424510|424520|424590|424610|424690|424710|424720|424810|424820|424910|424920|424930|424940|424950|424990|425120|441110|441120|441210|441222|441227|441330|441340|444110|444120|444140|444180|444230|444240|445110|445131|445132|445230|445240|445250|445291|445292|445298|445320|449110|449121|449122|449129|449210|455110|455211|455219|456110|456120|456130|456191|456199|457110|457120|457210|458110|458210|458310|458320|459110|459120|459130|459140|459210|459310|459410|459420|459510|459910|459920|459930|459991|459999|481111|481112|481211|481212|481219|482111|482112|483111|483112|483113|483114|483211|483212|484110|484121|484122|484210|484220|484230|485111|485112|485113|485119|485210|485310|485320|485410|485510|485991|485999|486110|486210|486910|486990|487110|487210|487990|488111|488119|488190|488210|488310|488320|488330|488390|488410|488490|488510|488991|488999|491110|492110|492210|493110|493120|493130|493190|512110|512120|512131|512132|512191|512199|512230|512240|512250|512290|513110|513120|513130|513140|513191|513199|513210|516110|516120|517110|517210|517311|517312|517410|517911|517919|518210|519110|519120|519130|519190|521110|522110|522120|522130|522190|522210|522220|522291|522292|522293|522294|522298|522310|522320|522390|523110|523120|523130|523140|523210|523910|523920|523930|523991|523999|524113|524114|524126|524127|524128|524130|524210|524291|524292|524298|524311|524312|524313|524314|524318|525110|525120|525190|525910|525920|525990|531110|531120|531130|531190|531210|531311|531312|531320|531390|532111|532112|532120|532210|532281|532282|532283|532284|532289|532310|532490|533110|541110|541120|541191|541199|541211|541213|541214|541219|541310|541320|541330|541340|541350|541360|541370|541380|541410|541420|541430|541490|541511|541512|541513|541519|541611|541612|541613|541614|541618|541620|541690|541713|541714|541715|541720|541810|541820|541830|541840|541850|541860|541870|541890|541910|541921|541922|541930|541940|541990|551111|551112|551114|551115|551116|561110|561210|561311|561312|561320|561330|561410|561421|561422|561431|561439|561440|561450|561491|561492|561499|561510|561520|561591|561599|561611|561612|561613|561621|561622|561710|561720|561730|561740|561910|561920|561990|562111|562112|562119|562211|562212|562213|562219|562910|562920|562991|562998|611110|611210|611310|611410|611420|611430|611511|611512|611513|611519|611610|611620|611630|611691|611692|611699|611710|621111|621112|621210|621310|621320|621330|621340|621391|621399|621410|621420|621491|621492|621493|621498|621511|621512|621910|621991|621999|622110|622210|622310|623110|623210|623220|623311|623312|623990|624110|624120|624190|624210|624221|624229|624230|624310|624410|624430|711110|711120|711130|711190|711211|711212|711219|711310|711320|711410|711510|712110|712120|712130|712190|713110|713120|713210|713290|713910|713920|713930|713940|713950|713990|721110|721120|721191|721199|721211|721214|721310|722310|722320|722410|722511|722513|722514|722515|722516|722518|722519|811111|811112|811113|811118|811121|811122|811191|811192|811198|811210|811310|811411|811412|811420|811430|811490|812111|812112|812113|812191|812199|812210|812220|812230|812310|812320|812331|812332|812910|812921|812922|812930|812990|813110|813211|813212|813219|813311|813312|813319|813410|813910|813920|813930|813940|813990|814110|921110|921120|921130|921140|921150|921190|921210|921310|921320|921330|921340|921350|921410|921420|921430|921440|921450|921460|921470|921480|921490|921910|921920|921930|921990|922110|922120|922130|922140|922150|922160|922190|922210|922220|922230|922240|922250|922260|922310|922320|922330|922340|922350|922360|922390|923110|923120|923130|923140|923150|923160|923170|923190|923210|923220|923310|923320|923330|923340|923350|923360|923390|924110|924120|924130|924140|924150|924160|924170|924190|925110|925120|925130|925140|925150|925160|925170|925190|926110|926120|926130|926140|926150|926160|926170|926190|926210|926220|926310|926320|926330|926340|926350|926360|926390|927110|927120|927130|927140|927150|927160|927170|927190|928110|928120|928130|928140|928150|928160|928170|928190|928210|928220|928230|928240|928250|928260|928310|928320|928330|928340|928350|928360|928390)"
    checkNAICS = "((?i)NAICS)"
    regexPSC = "\\b(?P<PSC>1000|1005|1005|1010|1010|1015|1015|1020|1020|1025|1025|1030|1030|1035|1035|1040|1045|1055|1070|1075|1075|1080|1090|1090|1095|1105|1110|1115|1115|1120|1125|1127|1130|1135|1135|1140|1145|1145|1190|1190|1195|1210|1220|1220|1230|1240|1240|1250|1260|1260|1265|1265|1270|1270|1280|1280|1285|1285|1287|1290|1290|1305|1305|1310|1310|1315|1315|1320|1320|1325|1330|1336|1336|1337|1337|1338|1338|1340|1340|1345|1346|1350|1350|1351|1351|1352|1352|1353|1353|1355|1355|1356|1356|1360|1360|1361|1361|1365|1367|1370|1375|1376|1377|1377|1380|1385|1385|1386|1386|1390|1395|1398|1398|1410|1420|1425|1427|1430|1430|1440|1450|1450|1510|1520|1540|1550|1550|1555|1560|1610|1615|1615|1620|1630|1640|1650|1650|1660|1660|1670|1670|1675|1677|1680|1680|1710|1720|1725|1730|1735|1740|1740|1810|1820|1830|1830|1840|1850|1850|1860|1900|1901|1902|1903|1904|1905|1906|1907|1908|1909|1910|1910|1911|1915|1920|1921|1922|1923|1924|1925|1926|1927|1928|1929|1930|1935|1935|1940|1945|1950|1955|1990|2010|2020|2030|2040|2050|2060|2090|2090|2210|2220|2230|2230|2240|2240|2250|2305|2310|2320|2330|2340|2340|2350|2350|2355|2355|2410|2410|2420|2430|2510|2510|2520|2520|2530|2530|2540|2541|2541|2590|2610|2610|2620|2620|2630|2640|2640|2805|2805|2810|2810|2815|2820|2820|2825|2830|2830|2835|2835|2840|2840|2845|2850|2850|2895|2895|2910|2910|2915|2915|2920|2920|2925|2925|2930|2930|2935|2935|2940|2940|2945|2945|2950|2950|2990|2990|2995|2995|3010|3010|3020|3020|3030|3030|3040|3040|3110|3120|3130|3210|3220|3230|3230|3405|3408|3408|3410|3410|3411|3411|3412|3413|3414|3415|3416|3417|3418|3419|3422|3424|3424|3426|3431|3432|3432|3433|3433|3436|3436|3438|3439|3439|3441|3442|3442|3443|3444|3445|3446|3447|3447|3448|3449|3449|3450|3455|3456|3456|3460|3461|3461|3465|3465|3470|3470|3510|3520|3530|3530|3540|3550|3590|3590|3605|3605|3610|3610|3611|3615|3620|3620|3625|3630|3630|3635|3635|3640|3645|3645|3650|3650|3655|3655|3660|3670|3670|3680|3680|3685|3685|3690|3690|3693|3694|3694|3695|3695|3710|3720|3730|3730|3740|3740|3750|3760|3770|3770|3805|3805|3810|3815|3820|3820|3825|3825|3830|3835|3835|3895|3895|3910|3915|3920|3920|3930|3930|3940|3950|3950|3960|3990|3990|4010|4020|4030|4110|4120|4130|4130|4140|4140|4150|4150|4210|4220|4220|4230|4230|4235|4235|4240|4250|4310|4320|4330|4330|4410|4420|4420|4430|4430|4440|4440|4460|4470|4510|4520|4530|4540|4610|4620|4620|4630|4710|4720|4730|4730|4810|4820|4910|4910|4920|4920|4921|4921|4923|4923|4925|4925|4927|4927|4930|4930|4931|4931|4933|4933|4935|4935|4940|4940|4960|4960|4970|4970|5110|5120|5130|5133|5133|5136|5136|5140|5180|5180|5210|5220|5220|5280|5280|5305|5306|5307|5310|5315|5320|5325|5330|5331|5335|5340|5340|5341|5342|5345|5350|5355|5360|5365|5365|5410|5410|5411|5419|5420|5430|5440|5440|5445|5450|5450|5510|5510|5520|5530|5610|5610|5620|5620|5630|5640|5640|5650|5660|5660|5670|5675|5675|5680|5680|5805|5805|5810|5810|5811|5811|5811|5815|5820|5820|5821|5821|5825|5825|5826|5826|5830|5830|5831|5831|5835|5835|5836|5836|5840|5841|5845|5850|5850|5850|5855|5855|5860|5860|5865|5865|5895|5895|5895|5905|5910|5915|5920|5920|5925|5930|5935|5940|5940|5945|5950|5955|5955|5960|5960|5961|5961|5962|5963|5965|5965|5970|5970|5975|5977|5977|5980|5980|5985|5985|5990|5995|5995|5996|5998|5998|5999|5999|6004|6005|6006|6007|6008|6010|6010|6015|6015|6020|6020|6020|6021|6021|6025|6026|6029|6030|6030|6031|6032|6032|6032|6033|6034|6035|6035|6035|6040|6050|6060|6060|6070|6070|6070|6080|6080|6099|6099|6099|6105|6110|6115|6115|6116|6116|6117|6120|6120|6125|6130|6135|6140|6145|6150|6150|6160|6160|6210|6210|6220|6220|6230|6230|6240|6250|6260|6310|6320|6320|6330|6340|6350|6350|6505|6506|6506|6507|6508|6509|6510|6515|6515|6520|6520|6525|6525|6530|6530|6532|6532|6540|6540|6545|6545|6550|6550|6555|6605|6610|6615|6615|6620|6625|6625|6630|6632|6635|6635|6636|6636|6640|6645|6650|6650|6655|6660|6660|6665|6665|6670|6675|6675|6680|6680|6685|6685|6695|6695|6710|6720|6730|6740|6740|6750|6760|6760|6770|6780|6780|6810|6820|6830|6830|6835|6840|6840|6850|6910|6920|6930|6940|7010|7010|7020|7020|7020|7021|7021|7021|7022|7022|7022|7025|7025|7025|7030|7030|7035|7035|7040|7042|7042|7045|7045|7050|7050|7A20|7A21|7B20|7B21|7B22|7C20|7C21|7D20|7E20|7E20|7E21|7F20|7G20|7G21|7G22|7H20|7J20|7K20|7105|7110|7125|7125|7195|7195|7210|7220|7230|7240|7240|7290|7290|7310|7310|7320|7330|7340|7350|7360|7360|7420|7430|7430|7435|7450|7450|7460|7490|7510|7520|7530|7540|7610|7630|7640|7641|7641|7642|7642|7643|7643|7644|7644|7650|7660|7670|7690|7710|7720|7720|7730|7730|7735|7740|7810|7820|7830|7830|7910|7910|7920|7930|7930|8010|8010|8020|8030|8040|8105|8110|8115|8120|8120|8125|8130|8135|8135|8140|8140|8145|8145|8150|8305|8310|8310|8315|8320|8325|8330|8335|8340|8345|8405|8410|8415|8420|8425|8430|8435|8440|8440|8445|8445|8450|8450|8455|8457|8460|8465|8470|8475|8475|8510|8510|8520|8520|8530|8540|8710|8720|8730|8810|8820|8900|8905|8910|8915|8920|8925|8930|8935|8940|8940|8945|8950|8955|8960|8965|8970|8975|8999|9110|9130|9130|9135|9135|9140|9150|9150|9160|9310|9320|9330|9340|9350|9350|9390|9390|9410|9420|9420|9430|9430|9440|9440|9450|9505|9510|9515|9520|9525|9525|9530|9530|9535|9535|9540|9540|9545|9545|9610|9620|9630|9640|9640|9650|9650|9660|9670|9680|9905|9905|9910|9915|9915|9920|9925|9925|9930|9930|9998|9999|AA10|AA11|AA11|AA11|AA12|AA12|AA12|AA13|AA13|AA13|AA14|AA14|AA14|AA15|AA15|AA15|AA16|AA16|AA17|AA17|AA20|AA21|AA21|AA22|AA22|AA23|AA23|AA24|AA24|AA25|AA25|AA26|AA26|AA27|AA27|AA30|AA31|AA31|AA32|AA32|AA33|AA33|AA34|AA34|AA35|AA35|AA36|AA36|AA37|AA37|AA40|AA41|AA42|AA43|AA44|AA45|AA46|AA47|AA90|AA91|AA91|AA92|AA92|AA93|AA93|AA94|AA94|AA95|AA95|AA96|AA96|AA97|AA97|AB10|AB11|AB11|AB11|AB12|AB12|AB12|AB13|AB13|AB13|AB14|AB14|AB14|AB15|AB15|AB15|AB16|AB16|AB17|AB17|AB20|AB21|AB21|AB21|AB22|AB22|AB22|AB23|AB23|AB23|AB24|AB24|AB24|AB25|AB25|AB25|AB26|AB26|AB27|AB27|AB30|AB31|AB31|AB32|AB32|AB33|AB33|AB34|AB34|AB35|AB35|AB36|AB36|AB37|AB37|AB40|AB41|AB41|AB42|AB42|AB43|AB43|AB44|AB44|AB45|AB45|AB46|AB46|AB47|AB47|AB90|AB91|AB91|AB92|AB92|AB93|AB93|AB94|AB94|AB95|AB95|AB96|AB96|AB97|AB97|AC10|AC11|AC11|AC11|AC12|AC12|AC12|AC13|AC13|AC13|AC14|AC14|AC14|AC15|AC15|AC15|AC16|AC16|AC17|AC17|AC20|AC21|AC21|AC21|AC22|AC22|AC22|AC23|AC23|AC24|AC24|AC24|AC25|AC25|AC25|AC26|AC26|AC27|AC27|AC30|AC31|AC31|AC31|AC32|AC32|AC32|AC33|AC33|AC33|AC34|AC34|AC34|AC35|AC35|AC35|AC36|AC36|AC37|AC37|AC40|AC41|AC41|AC42|AC42|AC43|AC43|AC44|AC44|AC45|AC45|AC46|AC46|AC47|AC47|AC50|AC51|AC51|AC52|AC52|AC53|AC53|AC54|AC54|AC55|AC55|AC56|AC56|AC57|AC57|AC60|AC61|AC61|AC62|AC62|AC63|AC63|AC64|AC64|AC65|AC65|AC66|AC66|AC67|AC67|AC90|AC91|AC91|AC92|AC92|AC93|AC93|AC94|AC94|AC95|AC95|AC96|AC96|AC97|AC97|AD10|AD11|AD11|AD12|AD12|AD13|AD13|AD14|AD14|AD15|AD15|AD16|AD16|AD17|AD17|AD20|AD21|AD21|AD22|AD22|AD23|AD23|AD24|AD24|AD25|AD25|AD26|AD26|AD27|AD27|AD30|AD31|AD31|AD32|AD32|AD33|AD33|AD34|AD34|AD35|AD35|AD36|AD36|AD37|AD37|AD40|AD41|AD41|AD42|AD42|AD43|AD43|AD44|AD44|AD45|AD45|AD46|AD46|AD47|AD47|AD50|AD51|AD51|AD52|AD52|AD53|AD53|AD54|AD54|AD55|AD55|AD56|AD56|AD57|AD57|AD60|AD61|AD61|AD62|AD62|AD63|AD63|AD64|AD64|AD65|AD65|AD66|AD66|AD67|AD67|AD90|AD91|AD91|AD92|AD92|AD93|AD93|AD94|AD94|AD95|AD95|AD96|AD96|AD97|AD97|AE10|AE11|AE11|AE12|AE12|AE13|AE13|AE14|AE14|AE15|AE15|AE16|AE16|AE17|AE17|AE20|AE21|AE21|AE22|AE22|AE23|AE23|AE24|AE24|AE25|AE25|AE26|AE26|AE27|AE27|AE30|AE31|AE31|AE32|AE32|AE33|AE33|AE34|AE34|AE35|AE35|AE36|AE36|AE37|AE37|AE90|AE91|AE91|AE92|AE92|AE93|AE93|AE94|AE94|AE95|AE95|AE96|AE96|AE97|AE97|AF10|AF11|AF11|AF11|AF12|AF12|AF12|AF13|AF13|AF13|AF14|AF14|AF14|AF15|AF15|AF15|AF16|AF16|AF17|AF17|AF21|AF22|AF23|AF24|AF25|AF31|AF32|AF33|AF34|AF35|AG10|AG11|AG11|AG11|AG12|AG12|AG12|AG13|AG13|AG13|AG14|AG14|AG14|AG15|AG15|AG15|AG16|AG16|AG17|AG17|AG20|AG21|AG21|AG21|AG22|AG22|AG22|AG23|AG23|AG23|AG24|AG24|AG24|AG25|AG25|AG25|AG26|AG26|AG27|AG27|AG30|AG31|AG31|AG31|AG32|AG32|AG32|AG33|AG33|AG33|AG34|AG34|AG34|AG35|AG35|AG35|AG36|AG36|AG37|AG37|AG40|AG41|AG41|AG41|AG42|AG42|AG42|AG43|AG43|AG43|AG44|AG44|AG44|AG45|AG45|AG45|AG46|AG46|AG47|AG47|AG50|AG51|AG51|AG52|AG52|AG53|AG53|AG54|AG54|AG55|AG55|AG56|AG56|AG57|AG57|AG60|AG61|AG61|AG62|AG62|AG63|AG63|AG64|AG64|AG65|AG65|AG66|AG66|AG67|AG67|AG70|AG71|AG71|AG72|AG72|AG73|AG73|AG74|AG74|AG75|AG75|AG76|AG76|AG77|AG77|AG80|AG81|AG81|AG82|AG82|AG83|AG83|AG84|AG84|AG85|AG85|AG86|AG86|AG87|AG87|AG90|AG91|AG91|AG92|AG92|AG93|AG93|AG94|AG94|AG95|AG95|AG96|AG96|AG97|AG97|AH10|AH11|AH11|AH11|AH12|AH12|AH12|AH13|AH13|AH13|AH14|AH14|AH14|AH15|AH15|AH15|AH16|AH16|AH17|AH17|AH20|AH21|AH21|AH21|AH22|AH22|AH22|AH23|AH23|AH23|AH24|AH24|AH24|AH25|AH25|AH25|AH26|AH26|AH27|AH27|AH30|AH31|AH31|AH31|AH32|AH32|AH32|AH33|AH33|AH33|AH34|AH34|AH34|AH35|AH35|AH35|AH36|AH36|AH37|AH37|AH40|AH41|AH41|AH41|AH42|AH42|AH42|AH43|AH43|AH43|AH44|AH44|AH44|AH45|AH45|AH45|AH46|AH46|AH47|AH47|AH50|AH51|AH51|AH52|AH52|AH53|AH53|AH54|AH54|AH55|AH55|AH56|AH57|AH90|AH91|AH91|AH92|AH92|AH93|AH93|AH94|AH94|AH95|AH95|AH96|AH96|AH97|AH97|AJ10|AJ11|AJ11|AJ11|AJ12|AJ12|AJ12|AJ13|AJ13|AJ13|AJ14|AJ14|AJ14|AJ15|AJ15|AJ15|AJ16|AJ16|AJ17|AJ17|AJ21|AJ21|AJ22|AJ22|AJ23|AJ23|AJ24|AJ24|AJ25|AJ25|AJ26|AJ26|AJ27|AJ27|AJ31|AJ31|AJ32|AJ32|AJ33|AJ33|AJ34|AJ34|AJ35|AJ35|AJ36|AJ36|AJ37|AJ37|AJ41|AJ41|AJ42|AJ42|AJ43|AJ43|AJ44|AJ44|AJ45|AJ45|AJ46|AJ46|AJ47|AJ47|AJ51|AJ51|AJ52|AJ52|AJ53|AJ53|AJ54|AJ54|AJ55|AJ55|AJ56|AJ56|AJ57|AJ57|AJ61|AJ61|AJ62|AJ62|AJ63|AJ63|AJ64|AJ64|AJ65|AJ65|AJ66|AJ66|AJ67|AJ67|AJ71|AJ71|AJ72|AJ72|AJ73|AJ73|AJ74|AJ74|AJ75|AJ75|AJ76|AJ76|AJ77|AJ77|AJ90|AJ91|AJ91|AJ92|AJ92|AJ93|AJ93|AJ94|AJ94|AJ95|AJ95|AJ96|AJ96|AJ97|AJ97|AK10|AK11|AK11|AK11|AK12|AK12|AK12|AK13|AK13|AK13|AK14|AK14|AK14|AK15|AK15|AK15|AK16|AK16|AK17|AK17|AL10|AL11|AL11|AL11|AL12|AL12|AL12|AL13|AL13|AL13|AL14|AL14|AL14|AL15|AL15|AL15|AL16|AL16|AL17|AL17|AL20|AL21|AL21|AL22|AL22|AL23|AL23|AL24|AL24|AL25|AL25|AL26|AL26|AL27|AL27|AL90|AL91|AL91|AL92|AL92|AL93|AL93|AL94|AL94|AL95|AL95|AL96|AL96|AL97|AL97|AM10|AM11|AM11|AM11|AM12|AM12|AM12|AM13|AM13|AM13|AM14|AM14|AM14|AM15|AM15|AM15|AM16|AM16|AM17|AM17|AN10|AN11|AN11|AN11|AN12|AN12|AN12|AN13|AN13|AN13|AN14|AN14|AN14|AN15|AN15|AN15|AN16|AN16|AN17|AN17|AN20|AN21|AN21|AN21|AN22|AN22|AN22|AN23|AN23|AN23|AN24|AN24|AN24|AN25|AN25|AN25|AN26|AN26|AN27|AN27|AN30|AN31|AN31|AN31|AN32|AN32|AN32|AN33|AN33|AN33|AN34|AN34|AN34|AN35|AN35|AN35|AN36|AN36|AN37|AN37|AN40|AN41|AN41|AN41|AN42|AN42|AN42|AN43|AN43|AN43|AN44|AN44|AN44|AN45|AN45|AN45|AN46|AN46|AN47|AN47|AN50|AN51|AN51|AN52|AN52|AN53|AN53|AN54|AN54|AN55|AN55|AN56|AN56|AN57|AN57|AN60|AN61|AN61|AN62|AN62|AN63|AN63|AN64|AN64|AN65|AN65|AN66|AN66|AN67|AN67|AN70|AN71|AN71|AN72|AN72|AN73|AN73|AN74|AN74|AN75|AN75|AN76|AN76|AN77|AN77|AN81|AN81|AN82|AN82|AN83|AN83|AN84|AN84|AN85|AN85|AN86|AN86|AN87|AN87|AN90|AN91|AN91|AN92|AN92|AN93|AN93|AN94|AN94|AN95|AN95|AN96|AN96|AN97|AN97|AP10|AP11|AP12|AP13|AP14|AP15|AP16|AP17|AP20|AP21|AP21|AP22|AP22|AP23|AP23|AP24|AP24|AP25|AP25|AP26|AP26|AP27|AP27|AP30|AP31|AP31|AP32|AP32|AP33|AP33|AP34|AP34|AP35|AP35|AP36|AP36|AP37|AP37|AP40|AP41|AP41|AP42|AP42|AP43|AP43|AP44|AP44|AP45|AP45|AP46|AP46|AP47|AP47|AP50|AP51|AP51|AP52|AP52|AP53|AP53|AP54|AP54|AP55|AP55|AP56|AP56|AP57|AP57|AP61|AP61|AP62|AP62|AP63|AP63|AP64|AP64|AP65|AP65|AP66|AP66|AP67|AP67|AP71|AP71|AP72|AP72|AP73|AP73|AP74|AP74|AP75|AP75|AP76|AP76|AP77|AP77|AP90|AP91|AP91|AP92|AP92|AP93|AP93|AP94|AP94|AP95|AP95|AP96|AP96|AP97|AP97|AQ10|AQ11|AQ11|AQ12|AQ12|AQ13|AQ13|AQ14|AQ14|AQ15|AQ15|AQ16|AQ16|AQ17|AQ17|AQ90|AQ91|AQ91|AQ92|AQ92|AQ93|AQ93|AQ94|AQ94|AQ95|AQ95|AQ96|AQ96|AQ97|AQ97|AR10|AR11|AR11|AR11|AR12|AR12|AR12|AR13|AR13|AR13|AR14|AR14|AR14|AR15|AR15|AR15|AR16|AR16|AR17|AR17|AR20|AR21|AR21|AR22|AR22|AR23|AR23|AR24|AR24|AR25|AR25|AR26|AR26|AR27|AR27|AR30|AR31|AR31|AR32|AR32|AR33|AR33|AR34|AR34|AR35|AR35|AR36|AR36|AR37|AR37|AR40|AR41|AR41|AR42|AR42|AR43|AR43|AR44|AR44|AR45|AR45|AR46|AR46|AR47|AR47|AR50|AR51|AR52|AR53|AR54|AR55|AR56|AR57|AR60|AR61|AR61|AR62|AR62|AR63|AR63|AR64|AR64|AR65|AR65|AR66|AR66|AR67|AR67|AR70|AR71|AR71|AR72|AR72|AR73|AR73|AR74|AR74|AR75|AR75|AR76|AR76|AR77|AR77|AR90|AR91|AR91|AR92|AR92|AR93|AR93|AR94|AR94|AR95|AR95|AR96|AR96|AR97|AR97|AS10|AS11|AS11|AS11|AS12|AS12|AS12|AS13|AS13|AS13|AS14|AS14|AS14|AS15|AS15|AS15|AS16|AS16|AS17|AS17|AS20|AS21|AS21|AS21|AS22|AS22|AS22|AS23|AS23|AS23|AS24|AS24|AS24|AS25|AS25|AS25|AS26|AS26|AS27|AS27|AS30|AS31|AS31|AS31|AS32|AS32|AS32|AS33|AS33|AS33|AS34|AS34|AS34|AS35|AS35|AS35|AS36|AS36|AS37|AS37|AS40|AS41|AS41|AS41|AS42|AS42|AS42|AS43|AS43|AS43|AS44|AS44|AS44|AS45|AS45|AS45|AS46|AS46|AS47|AS47|AS90|AS91|AS91|AS92|AS92|AS93|AS93|AS94|AS94|AS95|AS95|AS96|AS96|AS97|AS97|AT10|AT11|AT11|AT12|AT12|AT13|AT13|AT14|AT14|AT15|AT15|AT16|AT16|AT17|AT17|AT20|AT21|AT21|AT22|AT22|AT23|AT23|AT24|AT24|AT25|AT25|AT26|AT26|AT27|AT27|AT30|AT31|AT31|AT32|AT32|AT33|AT33|AT34|AT34|AT35|AT35|AT36|AT36|AT37|AT37|AT40|AT41|AT41|AT42|AT42|AT43|AT43|AT44|AT44|AT45|AT45|AT46|AT46|AT47|AT47|AT50|AT51|AT51|AT52|AT52|AT53|AT53|AT54|AT54|AT55|AT55|AT56|AT56|AT57|AT57|AT60|AT61|AT61|AT62|AT62|AT63|AT63|AT64|AT64|AT65|AT65|AT66|AT66|AT67|AT67|AT70|AT71|AT71|AT72|AT72|AT73|AT73|AT74|AT74|AT75|AT75|AT76|AT76|AT77|AT77|AT81|AT81|AT82|AT82|AT83|AT83|AT84|AT84|AT85|AT85|AT86|AT86|AT87|AT87|AT90|AT91|AT91|AT92|AT92|AT93|AT93|AT94|AT94|AT95|AT95|AT96|AT96|AT97|AT97|AU10|AU11|AU12|AU13|AU14|AU15|AU16|AU17|AU90|AU91|AU92|AU93|AU94|AU95|AU96|AU97|AV10|AV11|AV11|AV12|AV12|AV13|AV13|AV14|AV14|AV15|AV15|AV16|AV16|AV17|AV17|AV20|AV21|AV21|AV22|AV22|AV23|AV23|AV24|AV24|AV25|AV25|AV26|AV26|AV27|AV27|AV30|AV31|AV31|AV32|AV32|AV33|AV33|AV34|AV34|AV35|AV35|AV36|AV36|AV37|AV37|AV40|AV41|AV41|AV42|AV42|AV43|AV43|AV44|AV44|AV45|AV45|AV46|AV46|AV47|AV47|AV50|AV51|AV51|AV52|AV52|AV53|AV53|AV54|AV54|AV55|AV55|AV56|AV56|AV57|AV57|AV60|AV61|AV61|AV62|AV62|AV63|AV63|AV64|AV64|AV65|AV65|AV66|AV66|AV67|AV67|AV70|AV71|AV71|AV72|AV72|AV73|AV73|AV74|AV74|AV75|AV75|AV76|AV76|AV77|AV77|AV90|AV91|AV91|AV92|AV92|AV93|AV93|AV94|AV94|AV95|AV95|AV96|AV96|AV97|AV97|AZ10|AZ11|AZ11|AZ12|AZ12|AZ13|AZ13|AZ14|AZ14|AZ15|AZ15|AZ16|AZ16|AZ17|AZ17|B502|B502|B503|B503|B504|B504|B505|B505|B506|B506|B507|B507|B509|B509|B510|B510|B511|B512|B513|B513|B516|B516|B517|B517|B518|B518|B519|B519|B520|B520|B521|B521|B522|B522|B524|B524|B525|B525|B526|B526|B527|B527|B528|B528|B529|B529|B530|B530|B532|B532|B533|B533|B534|B534|B537|B537|B538|B538|B539|B539|B540|B540|B541|B541|B542|B542|B543|B543|B544|B544|B545|B545|B546|B546|B547|B547|B548|B548|B549|B549|B550|B550|B551|B551|B552|B552|B553|B553|B554|B554|B555|B555|B599|B599|C111|C112|C113|C114|C115|C116|C117|C118|C119|C121|C122|C123|C124|C129|C130|C1AA|C1AB|C1AZ|C1BA|C1BB|C1BC|C1BD|C1BE|C1BF|C1BG|C1BZ|C1CA|C1CZ|C1DA|C1DB|C1DZ|C1EA|C1EB|C1EC|C1ED|C1EE|C1EZ|C1FA|C1FB|C1FC|C1FD|C1FE|C1FF|C1FZ|C1GA|C1GB|C1GC|C1GD|C1GZ|C1HA|C1HB|C1HC|C1HZ|C1JA|C1JB|C1JZ|C1KA|C1KB|C1KC|C1KD|C1KE|C1KF|C1KZ|C1LA|C1LB|C1LC|C1LZ|C1MA|C1MB|C1MC|C1MD|C1ME|C1MF|C1MG|C1MH|C1MZ|C1NA|C1NB|C1NC|C1ND|C1NE|C1NZ|C1PA|C1PB|C1PC|C1PD|C1PZ|C1QA|C211|C211|C212|C212|C213|C213|C214|C214|C215|C215|C216|C216|C217|C218|C219|C219|C220|C221|C222|C223|D301|D301|D302|D302|D303|D303|D304|D304|D305|D305|D305|D306|D306|D307|D307|D308|D308|D309|D309|D310|D310|D311|D311|D312|D312|D313|D313|D314|D314|D315|D315|D316|D316|D317|D317|D318|D319|D320|D321|D322|D324|D325|D399|D399|DA01|DA10|DB01|DB02|DB10|DC01|DC10|DD01|DE01|DE01|DE02|DE10|DE10|DE11|DF01|DF10|DG01|DG10|DG11|DG11|DH01|DH10|DJ01|DJ01|DJ10|DJ10|DK01|DK10|E111|E112|E119|E121|E122|E123|E124|E125|E126|E127|E129|E131|E139|E141|E142|E149|E151|E152|E153|E154|E155|E159|E161|E162|E163|E164|E165|E166|E169|E171|E172|E173|E174|E179|E181|E182|E183|E184|E191|E192|E199|E1AA|E1AB|E1AZ|E1BA|E1BB|E1BC|E1BD|E1BE|E1BF|E1BG|E1BZ|E1CA|E1CZ|E1DA|E1DB|E1DZ|E1EA|E1EB|E1EC|E1ED|E1EE|E1EZ|E1FA|E1FB|E1FC|E1FD|E1FE|E1FF|E1FZ|E1GA|E1GB|E1GC|E1GD|E1GZ|E1HA|E1HB|E1HC|E1HZ|E1JA|E1JB|E1JZ|E1KA|E1KB|E1KC|E1KD|E1KE|E1KF|E1KZ|E1LA|E1LB|E1LC|E1LZ|E1MA|E1MB|E1MC|E1MD|E1ME|E1MF|E1MG|E1MH|E1MZ|E1NA|E1NB|E1NC|E1ND|E1NE|E1NZ|E1PA|E1PB|E1PC|E1PD|E1PZ|E1QA|E211|E212|E213|E214|E215|E216|E219|E221|E222|E223|E224|E231|E232|E233|E234|E235|E236|E237|E239|E241|E242|E243|E244|E245|E249|E291|E292|E293|E294|E299|E300|F001|F001|F002|F002|F003|F003|F004|F004|F005|F005|F006|F006|F007|F007|F008|F008|F009|F009|F010|F010|F011|F011|F012|F012|F013|F013|F014|F014|F015|F015|F016|F016|F018|F018|F019|F019|F020|F020|F021|F021|F022|F022|F099|F099|F101|F101|F102|F103|F103|F104|F105|F105|F106|F107|F107|F108|F108|F109|F109|F110|F110|F111|F111|F112|F112|F113|F114|F115|F199|F201|F202|F203|F299|F301|F401|F501|F502|F503|F504|F599|F901|F902|F903|F999|F999|G001|G001|G002|G002|G003|G003|G004|G004|G005|G005|G006|G006|G007|G007|G008|G008|G009|G009|G010|G010|G099|G099|H110|H110|H111|H111|H112|H112|H113|H113|H114|H114|H115|H115|H116|H116|H117|H117|H118|H118|H119|H119|H120|H120|H122|H122|H123|H123|H124|H124|H125|H125|H126|H126|H128|H128|H129|H129|H130|H130|H131|H131|H132|H132|H134|H134|H135|H135|H136|H136|H137|H137|H138|H138|H139|H139|H140|H140|H141|H141|H142|H142|H143|H143|H144|H144|H145|H145|H146|H146|H147|H147|H148|H148|H149|H149|H151|H151|H152|H152|H153|H153|H154|H154|H155|H155|H156|H156|H158|H158|H159|H159|H160|H160|H161|H161|H162|H162|H163|H163|H165|H165|H166|H166|H167|H167|H168|H168|H169|H169|H170|H170|H171|H171|H172|H172|H173|H173|H174|H174|H175|H175|H176|H176|H177|H177|H178|H178|H179|H179|H180|H180|H181|H181|H183|H183|H184|H184|H185|H185|H187|H187|H188|H188|H189|H189|H191|H191|H193|H193|H194|H194|H195|H195|H196|H196|H199|H199|H210|H210|H211|H211|H212|H212|H213|H213|H214|H214|H215|H215|H216|H216|H217|H217|H218|H218|H219|H219|H220|H220|H222|H222|H223|H223|H224|H224|H225|H225|H226|H226|H228|H228|H229|H229|H230|H230|H231|H231|H232|H232|H234|H234|H235|H235|H236|H236|H237|H237|H238|H238|H239|H239|H240|H240|H241|H241|H242|H242|H243|H243|H244|H244|H245|H245|H246|H246|H247|H247|H248|H248|H249|H249|H251|H251|H252|H252|H253|H253|H254|H254|H255|H255|H256|H256|H258|H258|H259|H259|H260|H260|H261|H261|H262|H262|H263|H263|H265|H265|H266|H266|H267|H267|H268|H268|H269|H269|H270|H270|H271|H271|H272|H272|H273|H273|H274|H274|H275|H275|H276|H276|H277|H277|H278|H278|H279|H279|H280|H280|H281|H281|H283|H283|H284|H284|H285|H285|H287|H287|H288|H288|H289|H289|H291|H291|H293|H293|H294|H294|H295|H295|H296|H296|H299|H299|H310|H310|H311|H311|H312|H312|H313|H313|H314|H314|H315|H315|H316|H316|H317|H317|H318|H318|H319|H319|H320|H320|H322|H322|H323|H323|H324|H324|H325|H325|H326|H326|H328|H328|H329|H329|H330|H330|H331|H331|H332|H332|H334|H334|H335|H335|H336|H336|H337|H337|H338|H338|H339|H339|H340|H340|H341|H341|H342|H342|H343|H343|H344|H344|H345|H345|H346|H346|H347|H347|H348|H348|H349|H349|H351|H351|H352|H352|H353|H353|H354|H354|H355|H355|H356|H356|H358|H358|H359|H359|H360|H360|H361|H361|H362|H362|H363|H363|H365|H365|H366|H366|H367|H367|H368|H368|H369|H369|H370|H370|H371|H371|H372|H372|H373|H373|H374|H374|H375|H375|H376|H376|H377|H377|H378|H378|H379|H379|H380|H380|H381|H381|H383|H383|H384|H384|H385|H385|H387|H387|H388|H388|H389|H389|H391|H391|H393|H393|H394|H394|H395|H395|H396|H396|H399|H399|H910|H910|H911|H911|H912|H912|H913|H913|H914|H914|H915|H915|H916|H916|H917|H917|H918|H918|H919|H919|H920|H920|H922|H922|H923|H923|H924|H924|H925|H925|H926|H926|H928|H928|H929|H929|H930|H930|H931|H931|H932|H932|H934|H934|H935|H935|H936|H936|H937|H937|H938|H938|H939|H939|H940|H940|H941|H941|H942|H942|H943|H943|H944|H944|H945|H945|H946|H946|H947|H947|H948|H948|H949|H949|H951|H951|H952|H952|H953|H953|H954|H954|H955|H955|H956|H956|H958|H958|H959|H959|H960|H960|H961|H961|H962|H962|H963|H963|H965|H965|H966|H966|H967|H967|H968|H968|H969|H969|H970|H970|H971|H971|H972|H972|H973|H973|H974|H974|H975|H975|H976|H976|H977|H977|H978|H978|H979|H979|H980|H980|H981|H981|H983|H983|H984|H984|H985|H985|H987|H987|H988|H988|H989|H989|H991|H991|H993|H993|H994|H994|H995|H995|H996|H996|H999|H999|J010|J010|J011|J011|J012|J012|J013|J013|J014|J014|J015|J015|J016|J016|J017|J017|J018|J018|J019|J019|J020|J020|J022|J022|J023|J023|J024|J024|J025|J025|J026|J026|J028|J028|J029|J029|J030|J030|J031|J031|J032|J032|J034|J034|J035|J035|J036|J036|J037|J037|J038|J038|J039|J039|J040|J040|J041|J041|J042|J042|J043|J043|J044|J044|J045|J045|J046|J046|J047|J047|J048|J048|J049|J049|J051|J051|J052|J052|J053|J053|J054|J054|J055|J055|J056|J056|J058|J058|J059|J059|J060|J060|J061|J061|J062|J062|J063|J063|J065|J065|J066|J066|J067|J067|J068|J068|J069|J069|J070|J070|J071|J071|J072|J072|J073|J073|J074|J074|J075|J075|J076|J076|J077|J077|J078|J078|J079|J079|J080|J080|J081|J081|J083|J083|J084|J084|J085|J085|J087|J087|J088|J088|J089|J089|J091|J091|J093|J093|J094|J094|J095|J095|J096|J096|J099|J099|J998|J999|K010|K010|K011|K011|K012|K012|K013|K013|K014|K014|K015|K015|K016|K016|K017|K017|K018|K018|K019|K019|K020|K020|K022|K022|K023|K023|K024|K024|K025|K025|K026|K026|K028|K028|K029|K029|K030|K030|K031|K031|K032|K032|K034|K034|K035|K035|K036|K036|K037|K037|K038|K038|K039|K039|K040|K040|K041|K041|K042|K042|K043|K043|K044|K044|K045|K045|K046|K046|K047|K047|K048|K048|K049|K049|K051|K051|K052|K052|K053|K053|K054|K054|K055|K055|K056|K056|K058|K058|K059|K059|K060|K060|K061|K061|K062|K062|K063|K063|K065|K065|K066|K066|K067|K067|K068|K068|K069|K069|K070|K070|K071|K071|K072|K072|K073|K073|K074|K074|K075|K075|K076|K076|K077|K077|K078|K078|K079|K079|K080|K080|K081|K081|K083|K083|K084|K084|K085|K085|K087|K087|K088|K088|K089|K089|K091|K091|K093|K093|K094|K094|K095|K095|K096|K096|K099|K099|L010|L010|L011|L011|L012|L012|L013|L013|L014|L014|L015|L015|L016|L016|L017|L017|L018|L018|L019|L019|L020|L020|L022|L022|L023|L023|L024|L024|L025|L025|L026|L026|L028|L028|L029|L029|L030|L030|L031|L031|L032|L032|L034|L034|L035|L035|L036|L036|L037|L037|L038|L038|L039|L039|L040|L040|L041|L041|L042|L042|L043|L043|L044|L044|L045|L045|L046|L046|L047|L047|L048|L048|L049|L049|L051|L051|L052|L052|L053|L053|L054|L054|L055|L055|L056|L056|L058|L058|L059|L059|L060|L060|L061|L061|L062|L062|L063|L063|L065|L065|L066|L066|L067|L067|L068|L068|L069|L069|L070|L070|L071|L071|L072|L072|L073|L073|L074|L074|L075|L075|L076|L076|L077|L077|L078|L078|L079|L079|L080|L080|L081|L081|L083|L083|L084|L084|L085|L085|L087|L087|L088|L088|L089|L089|L091|L091|L093|L093|L094|L094|L095|L095|L096|L096|L099|L099|M111|M112|M119|M121|M122|M123|M124|M125|M126|M127|M129|M131|M139|M141|M142|M149|M151|M152|M153|M154|M155|M159|M161|M162|M163|M164|M165|M166|M169|M171|M172|M173|M174|M179|M181|M182|M183|M184|M191|M192|M199|M1AA|M1AB|M1AZ|M1BA|M1BB|M1BC|M1BD|M1BE|M1BF|M1BG|M1BZ|M1CA|M1CZ|M1DA|M1DB|M1DZ|M1EA|M1EB|M1EC|M1ED|M1EE|M1EZ|M1FA|M1FB|M1FC|M1FD|M1FE|M1FF|M1FZ|M1GA|M1GB|M1GC|M1GD|M1GZ|M1HA|M1HB|M1HC|M1HZ|M1JA|M1JB|M1JZ|M1KA|M1KB|M1KC|M1KD|M1KE|M1KF|M1KZ|M1LA|M1LB|M1LC|M1LZ|M1MA|M1MB|M1MC|M1MD|M1ME|M1MF|M1MG|M1MH|M1MZ|M1NA|M1NB|M1NC|M1ND|M1NE|M1NZ|M1PA|M1PB|M1PC|M1PD|M1PZ|M1QA|M2AA|M2AB|M2AC|M2AD|M2AE|M2AF|M2BA|M2BB|M2BZ|M2CA|M211|M212|M213|M214|M215|M216|M219|M221|M222|M223|M224|M231|M232|M233|M234|M235|M236|M237|M239|M241|M242|M243|M244|M245|M249|M291|M292|M293|M294|M299|M300|N010|N010|N011|N011|N012|N012|N013|N013|N014|N014|N015|N015|N016|N016|N017|N017|N018|N018|N019|N019|N020|N020|N022|N022|N023|N023|N024|N024|N025|N025|N026|N026|N028|N028|N029|N029|N030|N030|N031|N031|N032|N032|N034|N034|N035|N035|N036|N036|N037|N037|N038|N038|N039|N039|N040|N040|N041|N041|N042|N042|N043|N043|N044|N044|N045|N045|N046|N046|N047|N047|N048|N048|N049|N049|N051|N051|N052|N052|N053|N053|N054|N054|N055|N055|N056|N056|N058|N058|N059|N059|N060|N060|N061|N061|N062|N062|N063|N063|N065|N065|N066|N066|N067|N067|N068|N068|N069|N069|N070|N070|N071|N071|N072|N072|N073|N073|N074|N074|N075|N075|N076|N076|N077|N077|N078|N078|N079|N079|N080|N080|N081|N081|N083|N083|N084|N084|N085|N085|N087|N087|N088|N088|N089|N089|N091|N091|N093|N093|N094|N094|N095|N095|N096|N096|N099|N099|P100|P100|P200|P200|P300|P300|P400|P400|P500|P500|P999|P999|Q101|Q101|Q201|Q201|Q201|Q301|Q301|Q301|Q401|Q401|Q401|Q402|Q402|Q402|Q403|Q403|Q403|Q501|Q501|Q501|Q502|Q502|Q502|Q503|Q503|Q503|Q504|Q504|Q504|Q505|Q505|Q505|Q506|Q506|Q507|Q507|Q507|Q508|Q508|Q508|Q509|Q509|Q509|Q510|Q510|Q510|Q511|Q511|Q511|Q512|Q512|Q513|Q513|Q513|Q514|Q514|Q514|Q515|Q515|Q515|Q516|Q516|Q516|Q517|Q517|Q517|Q518|Q518|Q518|Q519|Q519|Q519|Q520|Q520|Q520|Q521|Q521|Q521|Q522|Q522|Q522|Q523|Q523|Q523|Q524|Q524|Q524|Q525|Q525|Q525|Q526|Q526|Q527|Q527|Q527|Q528|Q529|Q530|Q531|Q532|Q533|Q601|Q601|Q602|Q602|Q603|Q603|Q701|Q701|Q702|Q702|Q801|Q801|Q802|Q802|Q901|Q901|Q901|Q999|Q999|R111|R112|R113|R114|R115|R116|R117|R118|R119|R121|R122|R123|R124|R129|R199|R211|R212|R213|R214|R215|R216|R219|R301|R302|R303|R304|R305|R306|R307|R399|R401|R401|R402|R402|R403|R404|R404|R405|R405|R406|R406|R407|R408|R408|R409|R410|R411|R411|R412|R412|R413|R413|R414|R415|R415|R416|R416|R418|R418|R419|R420|R420|R421|R422|R422|R423|R423|R424|R424|R425|R425|R426|R426|R427|R427|R428|R428|R429|R430|R431|R497|R497|R498|R498|R499|R499|R502|R503|R504|R505|R506|R507|R509|R510|R511|R512|R513|R516|R517|R518|R519|R520|R521|R522|R524|R525|R526|R527|R528|R529|R530|R532|R533|R534|R537|R538|R539|R540|R541|R542|R543|R544|R545|R546|R547|R548|R549|R550|R551|R552|R553|R554|R599|R601|R602|R602|R603|R603|R604|R604|R605|R605|R606|R606|R607|R607|R608|R608|R609|R609|R610|R610|R611|R611|R612|R612|R613|R613|R614|R614|R615|R616|R617|R699|R699|R701|R701|R702|R702|R703|R703|R704|R704|R705|R705|R706|R706|R707|R707|R708|R708|R709|R710|R710|R711|R711|R712|R712|R713|R713|R799|R799|S111|S111|S112|S112|S113|S114|S114|S119|S119|S201|S201|S202|S202|S203|S203|S204|S204|S205|S205|S206|S206|S207|S207|S208|S208|S209|S209|S211|S211|S212|S212|S213|S214|S214|S215|S215|S216|S216|S217|S217|S218|S218|S219|S220|S221|S222|S222|S299|S299|T001|T001|T002|T002|T003|T003|T004|T004|T005|T005|T006|T006|T007|T007|T008|T008|T009|T009|T010|T010|T011|T011|T012|T012|T013|T013|T014|T014|T015|T015|T016|T016|T099|T099|U001|U001|U002|U002|U003|U003|U004|U004|U005|U005|U006|U006|U007|U007|U008|U008|U009|U009|U010|U010|U011|U011|U012|U012|U013|U014|U099|U099|V001|V001|V002|V002|V003|V003|V111|V111|V112|V112|V113|V113|V114|V114|V115|V115|V119|V119|V121|V121|V122|V122|V123|V123|V124|V124|V125|V125|V126|V126|V127|V127|V129|V129|V211|V211|V212|V212|V213|V213|V214|V214|V221|V221|V222|V222|V223|V223|V224|V224|V225|V225|V226|V226|V227|V227|V228|V229|V230|V231|V231|V241|V241|V251|V251|V301|V301|V302|V302|V999|V999|W010|W010|W011|W011|W012|W012|W013|W013|W014|W014|W015|W015|W016|W016|W017|W017|W018|W018|W019|W019|W020|W020|W022|W022|W023|W023|W024|W024|W025|W025|W026|W026|W028|W028|W029|W029|W030|W030|W031|W031|W032|W032|W034|W034|W035|W035|W036|W036|W037|W037|W038|W038|W039|W039|W040|W040|W041|W041|W042|W042|W043|W043|W044|W044|W045|W045|W046|W046|W047|W047|W048|W048|W049|W049|W051|W051|W052|W052|W053|W053|W054|W054|W055|W055|W056|W056|W058|W058|W059|W059|W060|W060|W061|W061|W062|W062|W063|W063|W065|W065|W066|W066|W067|W067|W068|W068|W069|W069|W070|W070|W070|W071|W071|W072|W072|W073|W073|W074|W074|W075|W075|W076|W076|W077|W077|W078|W078|W079|W079|W080|W080|W081|W081|W083|W083|W084|W084|W085|W085|W087|W087|W088|W088|W089|W089|W091|W091|W093|W093|W094|W094|W095|W095|W096|W096|W099|W099|X111|X112|X119|X121|X122|X123|X124|X125|X126|X127|X129|X131|X139|X141|X142|X149|X151|X152|X153|X154|X155|X159|X161|X162|X163|X164|X165|X166|X169|X171|X172|X173|X174|X179|X181|X182|X183|X184|X191|X192|X199|X1AA|X1AB|X1AZ|X1BA|X1BB|X1BC|X1BD|X1BE|X1BF|X1BG|X1BZ|X1CA|X1CZ|X1DA|X1DB|X1DZ|X1EA|X1EB|X1EC|X1ED|X1EE|X1EZ|X1FA|X1FB|X1FC|X1FD|X1FE|X1FF|X1FZ|X1GA|X1GB|X1GC|X1GD|X1GZ|X1HA|X1HB|X1HC|X1HZ|X1JA|X1JB|X1JZ|X1KA|X1KB|X1KC|X1KD|X1KE|X1KF|X1KZ|X1LA|X1LB|X1LC|X1LZ|X1MA|X1MB|X1MC|X1MD|X1ME|X1MF|X1MG|X1MH|X1MZ|X1NA|X1NB|X1NC|X1ND|X1NE|X1NZ|X1PA|X1PB|X1PC|X1PD|X1PZ|X1QA|X211|X212|X213|X214|X215|X216|X219|X221|X222|X223|X224|X231|X232|X233|X234|X235|X236|X237|X239|X241|X242|X243|X244|X245|X249|X291|X292|X293|X294|X299|X300|Y111|Y112|Y119|Y121|Y122|Y123|Y124|Y125|Y126|Y127|Y129|Y131|Y139|Y141|Y142|Y149|Y151|Y152|Y153|Y154|Y155|Y159|Y161|Y162|Y163|Y164|Y165|Y166|Y169|Y171|Y172|Y173|Y174|Y179|Y181|Y182|Y183|Y184|Y191|Y192|Y199|Y1AA|Y1AB|Y1AZ|Y1BA|Y1BB|Y1BC|Y1BD|Y1BE|Y1BF|Y1BG|Y1BZ|Y1CA|Y1CZ|Y1DA|Y1DB|Y1DZ|Y1EA|Y1EB|Y1EC|Y1ED|Y1EE|Y1EZ|Y1FA|Y1FB|Y1FC|Y1FD|Y1FE|Y1FF|Y1FZ|Y1GA|Y1GB|Y1GC|Y1GD|Y1GZ|Y1HA|Y1HB|Y1HC|Y1HZ|Y1JA|Y1JB|Y1JZ|Y1KA|Y1KB|Y1KC|Y1KD|Y1KE|Y1KF|Y1KZ|Y1LA|Y1LB|Y1LC|Y1LZ|Y1MA|Y1MB|Y1MC|Y1MD|Y1ME|Y1MF|Y1MG|Y1MH|Y1MZ|Y1NA|Y1NB|Y1NC|Y1ND|Y1NE|Y1NZ|Y1PA|Y1PB|Y1PC|Y1PD|Y1PZ|Y1QA|Y211|Y212|Y213|Y214|Y215|Y216|Y217|Y219|Y221|Y222|Y223|Y224|Y231|Y232|Y233|Y234|Y235|Y236|Y237|Y239|Y241|Y242|Y243|Y244|Y245|Y249|Y291|Y292|Y293|Y294|Y299|Y300|Z111|Z112|Z119|Z121|Z122|Z123|Z124|Z125|Z126|Z127|Z128|Z129|Z131|Z139|Z141|Z142|Z149|Z151|Z152|Z153|Z154|Z155|Z159|Z161|Z162|Z163|Z164|Z165|Z166|Z169|Z171|Z172|Z173|Z174|Z179|Z181|Z182|Z183|Z184|Z191|Z192|Z199|Z1AA|Z1AB|Z1AZ|Z1BA|Z1BB|Z1BC|Z1BD|Z1BE|Z1BF|Z1BG|Z1BZ|Z1CA|Z1CZ|Z1DA|Z1DB|Z1DZ|Z1EA|Z1EB|Z1EC|Z1ED|Z1EE|Z1EZ|Z1FA|Z1FB|Z1FC|Z1FD|Z1FE|Z1FF|Z1FZ|Z1GA|Z1GB|Z1GC|Z1GD|Z1GZ|Z1HA|Z1HB|Z1HC|Z1HZ|Z1JA|Z1JB|Z1JZ|Z1KA|Z1KB|Z1KC|Z1KD|Z1KE|Z1KF|Z1KZ|Z1LA|Z1LB|Z1LC|Z1LZ|Z1MA|Z1MB|Z1MC|Z1MD|Z1ME|Z1MF|Z1MG|Z1MH|Z1MZ|Z1NA|Z1NB|Z1NC|Z1ND|Z1NE|Z1NZ|Z1PA|Z1PB|Z1PC|Z1PD|Z1PZ|Z1QA|Z211|Z212|Z213|Z214|Z215|Z216|Z217|Z219|Z221|Z222|Z223|Z224|Z231|Z232|Z233|Z234|Z235|Z236|Z237|Z239|Z241|Z242|Z243|Z244|Z245|Z249|Z291|Z292|Z293|Z294|Z299|Z2AA|Z2AB|Z2AZ|Z2BA|Z2BB|Z2BC|Z2BD|Z2BE|Z2BF|Z2BG|Z2BZ|Z2CA|Z2CZ|Z2DA|Z2DB|Z2DZ|Z2EA|Z2EB|Z2EC|Z2ED|Z2EE|Z2EZ|Z2FA|Z2FB|Z2FC|Z2FD|Z2FE|Z2FF|Z2FZ|Z2GA|Z2GB|Z2GC|Z2GD|Z2GZ|Z2HA|Z2HB|Z2HC|Z2HZ|Z2JA|Z2JB|Z2JZ|Z2KA|Z2KB|Z2KC|Z2KD|Z2KE|Z2KF|Z2KZ|Z2LA|Z2LB|Z2LC|Z2LZ|Z2MA|Z2MB|Z2MC|Z2MD|Z2ME|Z2MF|Z2MG|Z2MH|Z2MZ|Z2NA|Z2NB|Z2NC|Z2ND|Z2NE|Z2NZ|Z2PA|Z2PB|Z2PC|Z2PD|Z2PZ|Z2QA|Z300)\\b"
    checkPSC = 'PSC'
    regexDEP = "(?P<DEP>Agriculture|Office of Civil Rights|Buildings and Facilities|Animal and Plant Health Inspection|Agricultural Marketing|Risk Management Agency|Farm Service Agency|Natural Resources Conservation|Rural Development|Rural Housing|Rural Business|Rural Utilities Service|Foreign Agricultural|Food and Nutrition|Forest|Commerce|Departmental Management|Economic Development|Bureau of the Census|Economics and Statistics|International Trade and Investment|Bureau of Industry and Security|Minority Business Development|National Oceanic and Atmospheric|U.S. Patent and Trademark|National Technical Information|National Institute of Standards and Technology|National Telecommunications and Information|Defense|Military Personnel|Operation and Maintenance|International Reconstruction|Research, Development, Test, and Evaluation|Military Construction|Family Housing|Revolving and Management Funds|Navy|Marine Corps|Allowances|Trust Funds|Army|Air Force|Defense-wide|Education|Elementary and Secondary Education|Innovation and Improvement|English Language Acquisition|Energy|National Nuclear Security|Health and Human Services|Homeland Security|Housing and Urban Development|the Interior|Justice|Labor|State|Transportation|Treasury|Veterans Affairs)"
    checkDEP = '(?i)department'
    regexSEP = "(?i)(?P<SEP>Indian Small Business Economic Enterprise|Women-owned|women owned|Women-Owned Small Business|WOSB|Service-Disabled Veteran-Owned small business|Veteran Owned|veteran owned|SDVOSB|Historically UnderUtilized|historically underutilized|HUBZone|Small Disadvantaged Buiness|small disadvantaged buiness|SDB|servicedisabled veteranowned small|economically disadvantaged womenowned small)"
    checkSEP = '(?i)program|reserved for'
    regexSC = "\\b(?i)(?P<SC>top secret|secret|confidential|Q|L)\\b" #TODO:might need to be search not find all, top secret and secret conflict
    checkSC = "(?i)clearance"
    regexPopStreetAddress = '/\\b\d{1,6} +.{2,25}\\b(avenue|ave|court|ct|street|st|drive|dr|lane|ln|road|rd|blvd|plaza|parkway|pkwy)[.,]?(.{0,25} +\\b\d{5}\\b)?/ig'
    checkPopStreetAddress = '(?i)place of performance'
    regexPopCity = '(?P<City>\\b(New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose|Austin|Jacksonville|Fort Worth|Columbus|Charlotte|San Francisco|Indianapolis|Seattle|Denver|Washington|Boston|El Paso|Nashville|Detroit|Oklahoma City|Portland|Las Vegas|Memphis|Louisville|Baltimore|Milwaukee|Albuquerque|Tucson|Fresno|Mesa|Sacramento|Atlanta|Kansas City|Colorado Springs|Omaha|Raleigh|Miami|Long Beach|Virginia Beach|Oakland|Minneapolis|Tulsa|Arlington|Tampa|New Orleans|Wichita|Cleveland|Bakersfield|Aurora|Anaheim|Honolulu|Santa Ana|Riverside|Corpus Christi|Lexington|Stockton|Henderson|Saint Paul|St. Louis|Cincinnati|Pittsburgh|Greensboro|Anchorage|Plano|Lincoln|Orlando|Irvine|Newark|Toledo|Durham|Chula Vista|Fort Wayne|Jersey City|St. Petersburg|Laredo|Madison|Chandler|Buffalo|Lubbock|Scottsdale|Reno|Glendale|Gilbert|Winston-Salem|North Las Vegas|Norfolk|Chesapeake|Garland|Irving|Hialeah|Fremont|Boise|Richmond|Baton Rouge|Spokane|Des Moines|Tacoma|San Bernardino|Modesto|Fontana|Santa Clarita|Birmingham|Oxnard|Fayetteville|Moreno Valley|Rochester|Glendale|Huntington Beach|Salt Lake City|Grand Rapids|Amarillo|Yonkers|Aurora|Montgomery|Akron|Little Rock|Huntsville|Augusta|Port St. Lucie|Grand Prairie|Columbus|Tallahassee|Overland Park|Tempe|McKinney|Mobile|Cape Coral|Shreveport|Frisco|Knoxville|Worcester|Brownsville|Vancouver|Fort Lauderdale|Sioux Falls|Ontario|Chattanooga|Providence|Newport News|Rancho Cucamonga|Santa Rosa|Peoria|Oceanside|Elk Grove|Salem|Pembroke Pines|Eugene|Garden Grove|Cary|Fort Collins|Corona|Springfield|Jackson|Alexandria|Hayward|Clarksville|Lakewood|Lancaster|Salinas|Palmdale|Hollywood|Springfield|Macon|Kansas City|Sunnyvale|Pomona|Killeen|Escondido|Pasadena|Naperville|Bellevue|Joliet|Murfreesboro|Midland|Rockford|Paterson|Savannah|Bridgeport|Torrance|McAllen|Syracuse|Surprise|Denton|Roseville|Thornton|Miramar|Pasadena|Mesquite|Olathe|Dayton|Carrollton|Waco|Orange|Fullerton|Charleston|West Valley City|Visalia|Hampton|Gainesville|Warren|Coral Springs|Cedar Rapids|Round Rock|Sterling Heights|Kent|Columbia|Santa Clara|New Haven|Stamford|Concord|Elizabeth|Athens|Thousand Oaks|Lafayette|Simi Valley|Topeka|Norman|Fargo|Wilmington|Abilene|Odessa|Columbia|Pearland|Victorville|Hartford|Vallejo|Allentown|Berkeley|Richardson|Arvada|Ann Arbor|Rochester|Cambridge|Sugar Land|Lansing|Evansville|College Station|Fairfield|Clearwater|Beaumont|Independence|Provo|West Jordan|Murrieta|Palm Bay|El Monte|Carlsbad|North Charleston|Temecula|Clovis|Springfield|Meridian|Westminster|Costa Mesa|High Point|Manchester|Pueblo|Lakeland|Pompano Beach|West Palm Beach|Antioch|Everett|Downey|Lowell|Centennial|Elgin|Richmond|Peoria|Broken Arrow|Miami Gardens|Billings|Jurupa Valley|Sandy Springs|Gresham|Lewisville|Hillsboro|Ventura|Greeley|Inglewood|Waterbury|League City|Santa Maria|Tyler|Davie|Lakewood|Daly City|Boulder|Allen|West Covina|Sparks|Wichita Falls|Green Bay|San Mateo|Norwalk|Rialto|Las Cruces|Chico|El Cajon|Burbank|South Bend|Renton|Vista|Davenport|Edinburg|Tuscaloosa|Carmel|Spokane Valley|San Angelo|Vacaville|Clinton|Bend|Woodbridge|Richmond|Boulder|Lewisville|Greeley|Las Cruces|South Bend|Tuscaloosa|Renton|El Cajon|Vista|Davenport|Edinburg|Carmel|Spokane Valley|San Angelo|Vacaville|Clinton|Bend|Woodbridge)\\b)'
    checkPopCity = '(?i)place of performance'
    regexPopState = '(?P<States>\\b(?i)(AL|Alabama|AK|Alaska|AZ|Arizona|AR|Arkansas|CA|California|CO|Colorado|CT|Connecticut|DE|Delaware|FL|Florida|GA|Georgia|HI|Hawaii|ID|Idaho|IL|Illinois|IN|Indiana|IA|Iowa|KS|Kansas|KY|Kentucky|LA|Louisiana|ME|Maine|MD|Maryland|MA|Massachusetts|MI|Michigan|MN|Minnesota|MS|Mississippi|MO|Missouri|MT|Montana|NE|Nebraska|NV|Nevada|NH|New Hampshire|NJ|New Jersey|NM|New Mexico|NY|New York|NC|North Carolina|ND|North Dakota|OH|Ohio|OK|Oklahoma|OR|Oregon|PA|Pennsylvania|RI|Rhode Island|SC|South Carolina|SD|South Dakota|TN|Tennessee|TX|Texas|UT|Utah|VT|Vermont|VA|Virginia|WA|Washington|WV|West Virginia|WI|Wisconsin|WY|Wyoming)\\b)'
    checkPopState = '(?i)place of performance'
    regexPopZip = '(?P<Zipcode>\\b\d{5}(?:-\d{4})?\\b)'
    checkPopZip = '(?i)zip code|place of performance'
    checkPopCountry = '(?i)country|place of performance'
    regexPopCountry = '(?P<Country>\\b(?i)(afghanistan|albania|algeria|andorra|angola|antigua and barbuda|argentina|armenia|australia|austria|azerbaijan|bahamas|bahrain|bangladesh|barbados|belarus|belgium|belize|benin|bhutan|bolivia|bosnia and herzegovina|botswana|brazil|brunei|bulgaria|burkina faso|burundi|cabo verde|cambodia|cameroon|canada|central african republic|chad|chile|china|colombia|comoros|congo democratic republic|congo republic|costa rica|croatia|cuba|cyprus|czech republic|denmark|djibouti|dominica|dominican republic|east timor|ecuador|egypt|el salvador|equatorial guinea|eritrea|estonia|eswatini|ethiopia|fiji|finland|france|gabon|gambia|georgia|germany|ghana|greece|grenada|guatemala|guinea|guinea bissau|guyana|haiti|honduras|hungary|iceland|india|indonesia|iran|iraq|ireland|israel|italy|jamaica|japan|jordan|kazakhstan|kenya|kiribati|korea north|korea south|kosovo|kuwait|kyrgyzstan|laos|latvia|lebanon|lesotho|liberia|libya|liechtenstein|lithuania|luxembourg|madagascar|malawi|malaysia|maldives|mali|malta|marshall islands|mauritania|mauritius|micronesia|moldova|monaco|mongolia|montenegro|morocco|mozambique|myanmar|namibia|nauru|nepal|netherlands|new zealand|nicaragua|niger|nigeria|north macedonia|norway|oman|pakistan|palau|panama|papua new guinea|paraguay|peru|philippines|poland|portugal|qatar|romania|russia|rwanda|saint kitts and nevis|saint lucia|saint vincent and the grenadines|samoa|san marino|sao tome and principe|saudi arabia|senegal|serbia|seychelles|sierra leone|singapore|slovakia|slovenia|solomon islands|somalia|south africa|south sudan|spain|sri lanka|sudan|suriname|sweden|switzerland|syria|taiwan|tajikistan|tanzania|thailand|togo|tonga|trinidad and tobago|tunisia|turkey|turkmenistan|tuvalu|uganda|ukraine|united arab emirates|united kingdom|united states|uruguay|uzbekistan|vanuatu|vatican city|venezuela|vietnam|yemen|zambia|zimbabwe)\\b)'
    regexState = '(?P<States>\\b(?i)(AL|Alabama|AK|Alaska|AZ|Arizona|AR|Arkansas|CA|California|CO|Colorado|CT|Connecticut|DE|Delaware|FL|Florida|GA|Georgia|HI|Hawaii|ID|Idaho|IL|Illinois|IN|Indiana|IA|Iowa|KS|Kansas|KY|Kentucky|LA|Louisiana|ME|Maine|MD|Maryland|MA|Massachusetts|MI|Michigan|MN|Minnesota|MS|Mississippi|MO|Missouri|MT|Montana|NE|Nebraska|NV|Nevada|NH|New Hampshire|NJ|New Jersey|NM|New Mexico|NY|New York|NC|North Carolina|ND|North Dakota|OH|Ohio|OK|Oklahoma|OR|Oregon|PA|Pennsylvania|RI|Rhode Island|SC|South Carolina|SD|South Dakota|TN|Tennessee|TX|Texas|UT|Utah|VT|Vermont|VA|Virginia|WA|Washington|WV|West Virginia|WI|Wisconsin|WY|Wyoming)\\b)'
    checkState = '(?i)state'
    regexCity = '(?P<City>\\b(New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose|Austin|Jacksonville|Fort Worth|Columbus|Charlotte|San Francisco|Indianapolis|Seattle|Denver|Washington|Boston|El Paso|Nashville|Detroit|Oklahoma City|Portland|Las Vegas|Memphis|Louisville|Baltimore|Milwaukee|Albuquerque|Tucson|Fresno|Mesa|Sacramento|Atlanta|Kansas City|Colorado Springs|Omaha|Raleigh|Miami|Long Beach|Virginia Beach|Oakland|Minneapolis|Tulsa|Arlington|Tampa|New Orleans|Wichita|Cleveland|Bakersfield|Aurora|Anaheim|Honolulu|Santa Ana|Riverside|Corpus Christi|Lexington|Stockton|Henderson|Saint Paul|St. Louis|Cincinnati|Pittsburgh|Greensboro|Anchorage|Plano|Lincoln|Orlando|Irvine|Newark|Toledo|Durham|Chula Vista|Fort Wayne|Jersey City|St. Petersburg|Laredo|Madison|Chandler|Buffalo|Lubbock|Scottsdale|Reno|Glendale|Gilbert|Winston-Salem|North Las Vegas|Norfolk|Chesapeake|Garland|Irving|Hialeah|Fremont|Boise|Richmond|Baton Rouge|Spokane|Des Moines|Tacoma|San Bernardino|Modesto|Fontana|Santa Clarita|Birmingham|Oxnard|Fayetteville|Moreno Valley|Rochester|Glendale|Huntington Beach|Salt Lake City|Grand Rapids|Amarillo|Yonkers|Aurora|Montgomery|Akron|Little Rock|Huntsville|Augusta|Port St. Lucie|Grand Prairie|Columbus|Tallahassee|Overland Park|Tempe|McKinney|Mobile|Cape Coral|Shreveport|Frisco|Knoxville|Worcester|Brownsville|Vancouver|Fort Lauderdale|Sioux Falls|Ontario|Chattanooga|Providence|Newport News|Rancho Cucamonga|Santa Rosa|Peoria|Oceanside|Elk Grove|Salem|Pembroke Pines|Eugene|Garden Grove|Cary|Fort Collins|Corona|Springfield|Jackson|Alexandria|Hayward|Clarksville|Lakewood|Lancaster|Salinas|Palmdale|Hollywood|Springfield|Macon|Kansas City|Sunnyvale|Pomona|Killeen|Escondido|Pasadena|Naperville|Bellevue|Joliet|Murfreesboro|Midland|Rockford|Paterson|Savannah|Bridgeport|Torrance|McAllen|Syracuse|Surprise|Denton|Roseville|Thornton|Miramar|Pasadena|Mesquite|Olathe|Dayton|Carrollton|Waco|Orange|Fullerton|Charleston|West Valley City|Visalia|Hampton|Gainesville|Warren|Coral Springs|Cedar Rapids|Round Rock|Sterling Heights|Kent|Columbia|Santa Clara|New Haven|Stamford|Concord|Elizabeth|Athens|Thousand Oaks|Lafayette|Simi Valley|Topeka|Norman|Fargo|Wilmington|Abilene|Odessa|Columbia|Pearland|Victorville|Hartford|Vallejo|Allentown|Berkeley|Richardson|Arvada|Ann Arbor|Rochester|Cambridge|Sugar Land|Lansing|Evansville|College Station|Fairfield|Clearwater|Beaumont|Independence|Provo|West Jordan|Murrieta|Palm Bay|El Monte|Carlsbad|North Charleston|Temecula|Clovis|Springfield|Meridian|Westminster|Costa Mesa|High Point|Manchester|Pueblo|Lakeland|Pompano Beach|West Palm Beach|Antioch|Everett|Downey|Lowell|Centennial|Elgin|Richmond|Peoria|Broken Arrow|Miami Gardens|Billings|Jurupa Valley|Sandy Springs|Gresham|Lewisville|Hillsboro|Ventura|Greeley|Inglewood|Waterbury|League City|Santa Maria|Tyler|Davie|Lakewood|Daly City|Boulder|Allen|West Covina|Sparks|Wichita Falls|Green Bay|San Mateo|Norwalk|Rialto|Las Cruces|Chico|El Cajon|Burbank|South Bend|Renton|Vista|Davenport|Edinburg|Tuscaloosa|Carmel|Spokane Valley|San Angelo|Vacaville|Clinton|Bend|Woodbridge|Richmond|Boulder|Lewisville|Greeley|Las Cruces|South Bend|Tuscaloosa|Renton|El Cajon|Vista|Davenport|Edinburg|Carmel|Spokane Valley|San Angelo|Vacaville|Clinton|Bend|Woodbridge)\\b)'
    checkCity = '(?i)city'
    regexZipCode = '\\b(?P<Zipcode>\\b\d{5}(?:-\d{4})?\\b)\\b'
    checkZipCode = '(?i)zipcode|zip-code'
    regexCountryCode = '\\b(?P<CountryCode>AFG|ALB|DZA|AND|AGO|ATG|ARG|ARM|AUS|AUT|AZE|BHS|BHR|BGD|BRB|BLR|BEL|BLZ|BEN|BTN|BOL|BIH|BWA|BRA|BRN|BGR|BFA|BDI|CPV|KHM|CMR|CAN|CAF|TCD|CHL|CHN|COL|COM|COD|COG|CRI|HRV|CUB|CYP|CZE|DNK|DJI|DMA|DOM|TLS|ECU|EGY|SLV|GNQ|ERI|EST|SWZ|ETH|FJI|FIN|FRA|GAB|GMB|GEO|DEU|GHA|GRC|GRD|GTM|GIN|GNB|GUY|HTI|HND|HUN|ISL|IND|IDN|IRN|IRQ|IRL|ISR|ITA|JAM|JPN|JOR|KAZ|KEN|KIR|PRK|KOR|KWT|KGZ|LAO|LVA|LBN|LSO|LBR|LBY|LIE|LTU|LUX|MDG|MWI|MYS|MDV|MLI|MLT|MHL|MRT|MUS|MEX|FSM|MDA|MCO|MNG|MNE|MAR|MOZ|MMR|NAM|NRU|NPL|NLD|NZL|NIC|NER|NGA|MKD|NOR|OMN|PAK|PLW|PAN|PNG|PRY|PER|PHL|POL|PRT|QAT|ROU|RUS|RWA|KNA|LCA|VCT|WSM|SMR|STP|SAU|SEN|SRB|SYC|SLE|SGP|SVK|SVN|SLB|SOM|ZAF|SSD|ESP|LKA|SDN|SUR|SWE|CHE|SYR|TWN|TJK|TZA|THA|TGO|TON|TTO|TUN|TUR|TKM|TUV|UGA|UKR|ARE|GBR|USA|URY|UZB|VUT|VAT|VEN|VNM|YEM|ZMB|ZWE)\\b'
    checkCountryCode = '(?i)location|country|country code|place of performance'
    regexAwardNumber = '(?P<AwardNumber>\\b\d[RUP][A-Z]{2}\d{6}-\d{2}[A-Z0-9]?\\b|[A-Z]\d{2}[A-Z]{2}-\d{2}-[A-Z0-9]-\d{4}\\b|NNC\d{2}[A-Z]{4}\d{2}[A-Z]\\b|[A-Z]\d{3}[A-Z]\d{2}\d{6}\\b)'
    checkAwardNumber = '(?i)(award).*(number)'
    regexAwardDate = '(?P<AwardID>\\b\d[RUP][A-Z]{2}\d{6}-\d{2}[A-Z0-9]?\b|[A-Z]\d{2}[A-Z]{2}-\d{2}-[A-Z0-9]-\d{4}\\b|NNC\d{2}[A-Z]{4}\d{2}[A-Z]\\b|[A-Z]\d{3}[A-Z]\d{2}\d{6}\\b)'
    checkAwardDate = '(?i)(award).*(date)'
    regexAwardMoney = '(?P<AwardMoney>\\b\$\d{1,3}(,\d{3})*(\.\d{2})?|(\d+(\.\d+)?[KMB]))\\b'
    checkAwardMoney = '(?i)((award).*(amount|money|total)((?i)size standard)))'
    regexAwardee = 'regexAwardee NONEPLACEHOLD'
    checkAwardee = '(?i)awarded to|awardee'
    regexPrimaryContactTitle = '\\b(CEO|CFO|CTO|President|Vice President|VP|Director|Manager|Assistant Manager|Team Lead|Lead|Senior|Junior|Analyst|Coordinator|Specialist|Associate|Executive|Officer|Consultant|Developer|Engineer|Technician|Intern|Admin|Administrator|Secretary|Clerk|Supervisor|Head of [a-zA-Z]+|Chief [a-zA-Z]+ Officer|Principal)\\b'
    checkPrimaryContactTitle = '(?i)(primary).*(title)|primary contact'
    regexPrimaryContactFullname = 'pri name NONEPLACEHOLD'
    checkPrimaryContactFullname = '(?i)(primary).*(name)|primary contact'
    regexPrimaryContactEmail = '(?i)(?P<Email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    checkPrimaryContactEmail = '(?i)(primary).*(email|contact)|primary contact'
    regexPrimaryContactPhone = "(?P<Phone>\\b(?:\+?\d{1,3}[ .-]?)?(?:\(?\d{1,4}\)?[ .-]?)?\d{3,4}[ .-]?\d{4,9}\\b)"
    checkPrimaryContactPhone = create_PrimaryContactPhone_regex()
    regexPrimaryContactFax = '(?P<Fax>(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
    checkPrimaryContactFax = create_PrimaryContactFax_regex()
    regexSecondaryContactTitle = '\\b(CEO|CFO|CTO|President|Vice President|VP|Director|Manager|Assistant Manager|Team Lead|Lead|Senior|Junior|Analyst|Coordinator|Specialist|Associate|Executive|Officer|Consultant|Developer|Engineer|Technician|Intern|Admin|Administrator|Secretary|Clerk|Supervisor|Head of [a-zA-Z]+|Chief [a-zA-Z]+ Officer|Principal)\\b'
    checkSecondaryContactTitle = create_SecondaryContactTitle_regex()
    regexSecondaryContactFullname = 'sec name NONEPLACEHOLD'
    checkSecondaryContactFullname = create_SecondaryContactFullname_regex()
    regexSecondaryContactEmail = '(?i)(?P<Email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    checkSecondaryContactEmail = create_SecondaryContactEmail_regex()
    regexSecondaryContactPhone = '(?P<Phone>\\b(?:\+?\d{1,3}[ .-]?)?(?:\(?\d{1,4}\)?[ .-]?)?\d{3,4}[ .-]?\d{4,9}\\b)'
    checkSecondaryContactPhone = create_SecondaryContactPhone_regex()
    regexSecondaryContactFax = '(?P<Fax>\\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\\b)'
    checkSecondaryContactFax = create_SecondaryContactFax_regex()

    # Women-Owned Small Buiness (WOSB), Service-Disabled Verteran-Owened small business (SDVOSB), Historically UnderUtilized Buiness Zones (HUBZones), Small Disadvantaged Buisness (SDB)
    #search
    for text in cleanedtext:
        text_split = text.split(":", 1)
        if len(text_split) < 2:
            continue
        filepath = text_split[0]
        content = text_split[1]

        #See if noticeID exsists in dict and saves value, creates if not
        try:
            split_filepath = filepath.split("/") #gets top path, noticeID #TODO:must change index if path changes
            noticeID = split_filepath[5]
        except:
            print("Error extracting file path")
            continue 
        curObj = myFileObjList.get(noticeID)
        if curObj == None:
            curObj = FileObj()
            curObj.noticeID = noticeID
            myFileObjList.addFileObj(curObj)

        for param in search_list: 
            keyWords = ''
            match param:
                case "NaicsCode": #NaicsCode
                    keyWords = checkNAICS
                    curRegex = regexNAICS
                case "PreferredClientsCustomers":
                    pass
                case "PSC":
                    keyWords = checkPSC
                    curRegex = regexPSC
                case "ProjectLocations":
                    pass
                case "ContractVehicles":
                    keyWords = checkContractVehicles
                    curRegex = regexContractVehicles
                case 'SetASideCode':
                    keyWords = checkSetASideCode
                    curRegex = regexSetASideCode
                case "SEP": #SetASide SetASideCode?
                    keyWords = checkSEP
                    curRegex = regexSEP
                case "DEP": #Department/Ind.Agency
                    keyWords = checkDEP
                    curRegex = regexDEP
                case "SC":
                    keyWords = checkSC
                    curRegex = regexSC
                case "PerSC":
                    keyWords = checkPerSC 
                    curRegex = regexPerSC
                case "FacSC":
                    keyWords = checkFacSC
                    curRegex = regexFacSC
                case "PopStreetAddress":
                    keyWords = checkPopStreetAddress
                    curRegex = regexPopStreetAddress
                case "PopCity":
                    keyWords = checkPopCity
                    curRegex = regexPopCity
                case "PopState":
                    keyWords = checkPopState
                    curRegex = regexPopState
                case "PopZip":
                    keyWords = checkPopZip 
                    curRegex = regexPopZip
                case "PopCountry":
                    keyWords = checkPopCountry
                    curRegex = regexPopCountry
                case "State":
                    keyWords = checkState
                    curRegex = regexState
                case "City":
                    keyWords = checkCity 
                    curRegex = regexCity
                case "ZipCode":
                    keyWords = checkZipCode
                    curRegex = regexZipCode
                case "CountryCode":
                    keyWords = checkCountryCode
                    curRegex = regexCountryCode
                case "AwardNumber":
                    keyWords = checkAwardNumber
                    curRegex = regexAwardNumber
                case "AwardDate":
                    keyWords = checkAwardDate
                    curRegex = regexAwardDate
                case "AwardMoney":
                    keyWords = checkAwardMoney
                    curRegex = regexAwardMoney
                case "Awardee":
                    keyWords = checkAwardee
                    curRegex = regexAwardee
                case "PrimaryContactTitle":
                    keyWords = checkPrimaryContactTitle
                    curRegex = regexPrimaryContactTitle
                case "PrimaryContactFullname":
                    keyWords = checkPrimaryContactFullname
                    curRegex = regexPrimaryContactFullname
                case "PrimaryContactEmail":
                    keyWords = checkPrimaryContactEmail
                    curRegex = regexPrimaryContactEmail
                case "PrimaryContactPhone":
                    keyWords = checkPrimaryContactPhone
                    curRegex = regexPrimaryContactPhone
                case "PrimaryContactFax":
                    keyWords = checkPrimaryContactFax
                    curRegex = regexPrimaryContactFax
                case "SecondaryContactTitle":
                    keyWords = checkSecondaryContactTitle
                    curRegex = regexSecondaryContactTitle
                case "SecondaryContactFullname":
                    keyWords = checkSecondaryContactFullname
                    curRegex = regexSecondaryContactFullname
                case "SecondaryContactEmail":
                    keyWords = checkSecondaryContactEmail
                    curRegex = regexSecondaryContactEmail
                case "SecondaryContactPhone":
                    keyWords = checkSecondaryContactPhone
                    curRegex = regexSecondaryContactPhone
                case "SecondaryContactFax":
                    keyWords = checkSecondaryContactFax
                    curRegex = regexSecondaryContactFax

            keyWords = keyWords.split(",")
            if checkKeyWords(keyWords, text):
                foundVal = re.findall(curRegex, text)
                added_file = open("/home/taco/Desktop/SearchScripts/added_file.txt", "a")
                if foundVal:
                    if ".pdf" in split_filepath[6]:
                        filepath = (split_filepath [5] + "/" + split_filepath[6]).split(".pdf")[0] + ".pdf" #path to found location
                    elif ".txt" in split_filepath[6]:
                        filepath = (split_filepath [5] + "/" + split_filepath[6]).split(".txt")[0] + ".txt" #path to found location
                    curContext = content
                    if type(foundVal) is list: 
                        foundVal = set(foundVal)
                        for val in foundVal:
                            if type(val) is tuple:
                                val = val[0]
                            sub = [val, filepath, curContext]
                            if param == 'DEP':
                                curObj.updateObj(sub, param, False)
                            else:
                                curObj.updateObj(sub, param)
                                added_file.write(filepath + " : " + sub[0] + " : " + sub[2] +"\n")

                    else: 
                        sub = []
                        if type(foundVal.group(0)) is tuple: 
                            sub =  [foundVal.group(0)[0], filepath, curContext]
                        else: 
                            sub = [foundVal.group(0), filepath, curContext]
                        if param == "DEP":
                            curObj.updateObj(sub, param, False)
                        else:
                            curObj.updateObj(sub, param)
                            added_file.write(filepath + " : " + sub[0] + " : " + sub[2] + "\n")               
    return curObj, added_df

#class to hold all FileObj 
class FileObjList:
    def __init__(self):
        self.dict = dict() #format {"NoticeID":FileObj}

    #This function adds the fileobj to the dict if not present
    #Input: NoticeID, File obj
    def addFileObj(self, FileObj):
        noticeID = FileObj.noticeID
        self.dict[noticeID] = FileObj
    
    #returns fileobj from dict if it exsists, none if not
    def get(self, noticeID):
        return self.dict.get(noticeID)
    
    # Convert the FileObjList to a dictionary
    def to_dict(self):
        return {noticeID: fileObj.to_dict() for noticeID, fileObj in self.dict.items()}


#File Object class to store information found for each file(NoticeID)
#provides functions to add and get information aswell as format to JSON
class FileObj:
    def __init__(self):
        self.noticeId = ""
        self.NaicsCode = [] #Structure [[NAICSCode, filepath, context]...]
        self.PSC = []
        self.ProjectLocations = []
        self.ContractVehicles = []
        self.SetASideCode = []
        self.DEP = []
        self.SES = []
        self.SEP = []
        self.SC = []
        self.FacSC = []
        self.PerSC = []
        self.PopStreetAddress = [] 
        self.PopCity = []
        self.PopState = []
        self.PopZip = []
        self.PopCountry = []
        self.State = []
        self.City = []
        self.ZipCode = []
        self.CountryCode = []
        self.AwardNumber = []
        self.AwardDate = []
        self.AwardMoney = []
        self.Awardee = []
        self.PrimaryContactTitle = []
        self.PrimaryContactFullname = []
        self.PrimaryContactEmail = []
        self.PrimaryContactPhone = []
        self.PrimaryContactFax = []
        self.SecondaryContactTitle = []
        self.SecondaryContactFullname = []
        self.SecondaryContactEmail = []
        self.SecondaryContactPhone = []
        self.SecondaryContactFax = []

    def get(self, param):
        match param:
            case "SetASideCode":
                return self.SetASideCode
            case "PerSC":
                return self.PerSC
            case "FacSC":
                return self.FacSC
            case "SEP":
                return self.SEP
            case "PSC":
                return self.PSC
            case "NaicsCode":
                return self.NaicsCode
            case 'PopStreetAddress':
                return self.PopStreetAddress
            case "PopCity":
                return self.PopCity
            case "PopZip":
                return self.PopZip 
            case "PopCountry":
                return self.PopCountry 
            case "State":
                return self.State
            case "City":
                return self.City
            case "ZipCode":
                return self.ZipCode
            case "CountryCode":
                return self.CountryCode
            case "AwardNumber":
                return self.AwardNumber
            case "AwardDate":
                return self.AwardDate
            case "AwardMoney":
                return self.AwardMoney
            case "Awardee":
                return self.Awardee
            case "PrimaryContactTitle":
                return self.PrimaryContactTitle
            case "PrimaryContactFullname":
                return self.PrimaryContactFullname
            case "PrimaryContractEmail":
                return self.PrimaryContactEmail
            case "PrimaryContactPhone":
                return self.PrimaryContactPhone
            case "PrimaryContactFax":
                return self.PrimaryContactFax
            case "SecondaryContactTitle":
                return self.SecondaryContactTitle
            case "SecondaryContactFullname":
                return self.SecondaryContactFullname
            case "SecondaryContactEmail":
                return self.SecondaryContactEmail
            case "SecondaryContactPhone":
                return self.SecondaryContactPhone
            case "SecondaryContactFax":
                return self.SecondaryContactFax
        
    #TODO: This might not update obj list, just its copy
    def updateObj(self, subItem, param, considerFilePath=True): 
        subItemList = self.get(param)

        #TODO -> Added
        if subItemList == None:
            subItemList = []
        print(subItemList)

        #Common Skips 
        if param == 'PopZip' and (subItem[0] == "21414" or subItem[0] == "23304"):
            print("Common PopZip passed: 21414")
            return
        if param == "PSC" and (subItem[0] == '5510' or subItem[0] == '6665' or subItem[0] == "9620" or subItem[0] == "9620" or subItem[0] == "9630" or subItem[0] == "9610" or subItem[0] == "9440" or subItem[0] == "9410" or subItem[0] == "9430" or subItem[0] == "5510" or subItem[0] == "2020" or subItem[0] == '1000'):
            print("Common PSC passed")
            return

        subItem = conversions(param, subItem)
        if subItemList == None:
            if param == "AwardMoney":
                subItemList.append(subItem[0])
                return
            subItemList.append(subItem)
        else:
            for sub in subItemList:
                if considerFilePath:
                    if sub[0] == subItem[0] and sub[1] == subItem[1]:
                        return
                else:
                    if sub[0] == subItem[0]:
                        return
                    
        if param == "AwardMoney":
            subItemList.append(subItem[0])
            return
        subItemList.append(subItem)
            
    # Convert the FileObj to a dictionary
    def to_dict(self):
        return {
            "noticeId": self.noticeId,
            "NaicsCode": self.NaicsCode,
            "PSC": self.PSC,
            "ProjectLocations": self.ProjectLocations,
            "ContractVehicles": self.ContractVehicles, 
            'SocioEconomic Status': self.SES, 
            'SocioEconomic Program': self.SEP, 
            'Department': self.DEP,
            'SecurityClearance': self.SC,
            "FacilitySecurityClearance": self.FacSC, 
            "PersonnelSecurityClearance": self.PerSC,
            "PopStreetAddress": self.PopStreetAddress, 
            "PopCity": self.PopCity, 
            "PopState": self.PopState, 
            "PopZip": self.PopZip, 
            "PopCountry": self.PopCountry, 
            "State": self.PopState, 
            "City": self.City,
            "ZipCode": self.ZipCode,
            "CountryCode": self.CountryCode,
            "AwardNumber": self.AwardNumber, 
            "AwardDate": self.AwardDate, 
            "AwardMoney": self.AwardMoney, 
            "Awardee": self.Awardee, 
            "PrimaryContactTitle": self.PrimaryContactTitle, 
            "PrimaryContactFullname": self.PrimaryContactFullname, 
            "PrimaryContactEmail": self.PrimaryContactEmail, 
            "PrimaryContactPhone": self.PrimaryContactPhone, 
            "PrimaryContactFax": self.PrimaryContactFax, 
            "SecondaryContactTitle": self.SecondaryContactTitle, 
            "SecondaryContactFullname": self.SecondaryContactFullname, 
            "SecondaryContactEmail": self.SecondaryContactEmail, 
            "SecondaryContactPhone": self.SecondaryContactPhone, 
            "SecondaryContactFax": self.SecondaryContactFax
        }

def conversions(param, subItem):
    temp = subItem 
    match param:
        case "SEP":
            if subItem[0].strip() == "Servicedisabled veteranowned small" or subItem[0].strip() == 'servicedisabled veteranowned small':
                temp[0] = 'SDVOSB'
            elif subItem[0].strip() == "economically disadvantaged womenowned small" or subItem[0].strip() == "Economically disadvantaged womenowned small":
                temp[0] = 'EDWOSB'
            elif  subItem[0].strip() == 'Small disadvantaged buisness' or subItem[0].strip() == "small disadvantaged buisness":
                temp[0] = 'SDB'
            elif subItem[0].strip() == 'Indian Small Business Economic Enterprise':
                temp[0] = 'ISBEE'
            elif temp[0].strip() == "Women Owned" or temp[0].strip() == 'women owned' or temp[0].strip() == 'Women owned':
                temp[0] = 'WO'
            elif temp[0].strip() == "VETERAN OWNED" or temp[0].strip() == 'Verteran Owned':
                temp[0] = 'VO'
    
    return temp
