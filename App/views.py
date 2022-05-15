from ast import Return
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    
    
    print(request.POST)
    logos = []
    names = []
    

    url_site = "https://www.avito.ma/auto/neuf/"

    r = requests.get(url_site)
    soup = BeautifulSoup(r.content, "html.parser")
    for link1 in soup.find_all(["img"], class_="list-iconstyled__BrandListLogoImg-sc-w9d03p-11 dMMFpl"):
        logos.append(link1.get("src"))

    for name in soup.find_all(class_ = "list-iconstyled__CarListLogoBrandName-sc-w9d03p-14 hxHdDc"):
        names.append(name.text)

    data_dict = list(zip(logos, names))
    

    return render(request, "index.html", {'data': data_dict, 'names': names, 'logos': logos})



def about(request):
    return render(request, "about.html")

def blog_details(request, blogDetails):
    
    data = []
    champs = []
    images = []
    prix = []
    marque = []

    recImage = []
    recLinks = []
    recPrices = []
    recMarques = []
    recAnnees = []
    recCarburant = []
    recKilometrage = []
    prixeuro = []

    re = requests.get("https://themoneyconverter.com/FR/MAD/EUR")
    newsoup = BeautifulSoup(re.content, "html.parser")

    for d in newsoup.find_all(id = "cc-ratebox"):
        madeuro = d.text.replace("EUR/MAD = ", "").replace(",", ".")
    try:
        madeuro = float(madeuro)
    except:
        madeuro = "convertion non disponible"

    r = requests.get(blogDetails.replace("%", "/"))
    soup = BeautifulSoup(r.content, "html.parser")

    for c in soup.find_all("span", {"class":"text_bold"}):
        data.append((c.text).replace('\t', '').replace('\n', '').replace('\r' ,' ').replace("  ", ""))

    for d in soup.find_all(class_="col-md-6 col-xs-6"):
        champs.append((d.text).replace('\t', '').replace('\n', '').replace('\r' ,' ').replace("  ", ""))

    for img in soup.find_all(class_="image-hb"):
        images.append(img['src'])
    for reclink in soup.find_all(class_="picture picture_show"):
        recLinks.append(reclink.findChildren()[0].get("href").replace("/", "%"))
        recImage.append(reclink.findChildren()[1].get("src"))
    try:
        prix.append(soup.find(class_="color_primary text_bold price-block").text.replace("\n", "").replace("\r", "").replace("\t", "").replace("  ", ""))
        prixeuro.append(str(round(float((prix[0].replace("Dhs","").replace(" ", ""))) * madeuro, 2))+" euro")
    except:
        prix.append("Appeler pour le prix")
        prixeuro.append("Appeler pour le prix")
    print(prix[0])

    marque.append(data[0].replace("\n", "").replace("\r", "").replace("\t", "").replace("  ", ""))
    data.pop(0)

    for recprice in soup.find_all("div", {"class":"price price_block"}):
        recPrices.append(recprice.text.replace("\n", "").replace("\r", "").replace("\t", "").replace("Afin de vous garantir les meilleurs échanges avec le vendeur, veuillez lui indiquer que vous avez vu son annonce sur Moteur.ma.  Faites attention ! Veuillez ne  jamais envoyer à un annonceur une avance d'argent lors du processus d'achat d'un véhicule disponible sur la Marketplace.  ", ""))
    for recmarque in soup.find_all("h3", {"class":"text-center title_mark_model"}):
        recMarques.append(recmarque.text.replace("\n", "").replace("\r", "").replace("  ", ""))

    for year in soup.find_all(class_="value_year"):
        recAnnees.append(year.text.replace("\n", "").replace("\r", "").replace("\t", "").replace("  ", ""))

    for reccarburant in soup.find_all(class_="value_fuel"):
        recCarburant.append(reccarburant.text.replace("\n", "").replace("\r", "").replace("\t", "").replace("  ", ""))

    for reckilometrage in soup.find_all(class_="value_km"):
        recKilometrage.append(reckilometrage.text.replace("\n", "").replace("\r", "").replace("\t", "").replace("  ", ""))
    
    carDetails = list(zip(data, champs))
    recDetails = list(zip(recImage, recLinks, recPrices, recMarques , recAnnees, recCarburant, recKilometrage))

    return render(request, "blog-details.html", {"carDetails":carDetails, "recDetails":recDetails, "prix":prix, "marque":marque, "images":images, "link":blogDetails.replace("%", "/"), "prixeuro":prixeuro})

def blog(request, blogpages):

    nbr = int(blogpages) - 1

    marque=[]
    carburant=[]
    modeleVilleCarburant=[]
    photos=[]

    pricess = []
    nlink = []

    links = []

    url = f"https://www.moteur.ma/fr/voiture/achat-voiture-occasion/"
    page=requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    for test1 in doc.find_all(['span'],class_="pull-right",style="font-size: 12px;margin-top: 15px;margin-right:2%;"):
        nbr_page=test1.findChildren()[1].text


    url = f"https://www.moteur.ma/fr/voiture/achat-voiture-occasion/{nbr * 15}"
    page=requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    for link in doc.find_all('a',class_="slide",href=True):
        links.append(link['href'].strip())

    for model in links:  # pour enlevez les informations dupliqué
        if model not in nlink:
            nlink.append(model.replace("/", "%"))

    for test in doc.find_all(['div'], class_="content-inner"):
        pricess.append(test.findChildren()[3].get_text(strip=True))

    for test in doc.find_all(['h3'],class_="title_mark_model"):
        marque.append(test.get_text(strip=True).split())

    for test in doc.find_all(['li'],style="line-height:24px;margin-bottom:3px;"):
        carburant.append(test.get_text(strip=True))

    for test in doc.find_all(['ul'],style="font-size:11px;"):
        modeleVilleCarburant.append(test.get_text().replace("Afficher l'annonce",' ').split())

        #for test in doc.find_all(['img'],class_="lz_img"):
            #photos.append(test['data-original'])

    for test in doc.find_all(['center']):
        try:
            photos.append(test.findChildren()[0]['data-original'])
        except:
            photos = len(marque) * ['https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM=']
    

        # modeleVilleCarburant = modeleVilleCarburant[:16]
    print(nlink)
    print(len(nlink))
    nlink = nlink[:30:2]
    
    mydata2 = list(zip(photos, modeleVilleCarburant, marque, pricess, nlink))
    print(len(nlink))
    return render(request, "blog.html", {'mydata2':mydata2, "nbrpages": int(blogpages), "pagesuivante": int(blogpages) + 2})

def car_details(request, marquesLinks):

    re = requests.get("https://themoneyconverter.com/FR/MAD/EUR")
    newsoup = BeautifulSoup(re.content, "html.parser")

    for d in newsoup.find_all(id = "cc-ratebox"):
        madeuro = d.text.replace("EUR/MAD = ", "").replace(",", ".")
    try:
        madeuro = float(madeuro)
    except:
        madeuro = "convertion non disponible"
    
    champs = []
    images = []

    data = []

    marques = []
    models = []
    prix =[]

    recImages = []
    recMrq = []
    recPrices = []
    recLinks = []

    myChamps = []
    prixeuro = []
    r = requests.get(marquesLinks.replace("%", "/"))
    soup = BeautifulSoup(r.content, "html.parser")

    donnees = soup.find_all(class_="indexstyled__ExtraValue-sc-nuvlnz-4 rCqTH")
    champsss = soup.find_all(class_="indexstyled__ExtraLabel-sc-nuvlnz-9 kLrYKV")
    imgs = soup.find_all("div", {"class":"indexstyled__Overview-sc-z5esq-1 dAHvoN"})
    mrq = soup.find_all(class_="indexstyled__VersionShortName-sc-z5esq-8 bfHvEI")
    mdl = soup.find_all(class_="indexstyled__VersionExtendedName-sc-z5esq-9 uWYvA")
    prx = soup.find_all(class_="indexstyled__PriceValue-sc-z5esq-13 elUbPx")

    for c in champsss:
        champs.append(c.text)
    for mq in mrq:
        marques.append(mq.text)
    for md in mdl:
        models.append(md.text)
    for pr in prx:
        prix.append(pr.text.replace('*', ''))
        prixeuro.append(str(round(float((prix[0].replace("DH","").replace(" ", ""))) * madeuro, 2))+" EUR €")
    if prix == []:
        prix = ["Prix non disponible"]
        prixeuro = ["Prix non disponible"]
    #data_dict = dict(zip(champs, data))
    myChamps.append(champs[0])
    t = 1
    while (champs[t] != "Carburant"):
        myChamps.append(champs[t])

        if t < len(champs) -1:
            t += 1
        else:
            break
    myChamps.pop()

    for d in donnees:
        if (len(data) == len(myChamps)):
            break
        data.append(d.text)

    for i in imgs:
        images.append(i.findChildren()[0]['src'])
    
    for s in soup.find_all("img", {"class":"modelsstyled__Picture-sc-1pawqcb-3 eCUFGF"}):
        recImages.append(s['src'])

    for recmrq in soup.find_all(class_="modelsstyled__Label-sc-1pawqcb-6 iWdbQO"):
        recMrq.append(recmrq.text)

    for recprices in soup.find_all(class_="modelsstyled__Price-sc-1pawqcb-10 hUyCyE"):
        recPrices.append(recprices.text)

    for reclink in soup.find_all(["a"], class_="modelsstyled__ModelContainer-sc-1pawqcb-1 emkgBn"):
        recLinks.append(("http://avito.ma" + reclink.get("href")).replace("/", "%"))
    
    myList = list(zip(data, myChamps))
    my2ndList = list(zip(recImages, recMrq, recPrices, recLinks))
    return render(request, "car-details.html", {"details": myList, "rec": my2ndList, "images": images, "marques": marques, "models": models, "prix": prix, "marquess": marquesLinks.replace("%", "/"), "prixeuro":prixeuro})

def car(request, marquepage):

    min_data = []
    big_data = []
    prices = []

    links = []
    images = []

    marques = []
    marquesLinks = []
    lien_parent = "https://www.avito.ma/auto/neuf/"
    lien_parent += marquepage + "/?annee="

    r = requests.get(lien_parent)
    soup = BeautifulSoup(r.content, "html.parser")

    for link1 in soup.find_all(["a"], class_="modelsstyled__ModelContainer-sc-1pawqcb-1 emkgBn"):
        links.append("http://avito.ma" + link1.get("href"))

    for a in links:
        r1 = requests.get(a)
        soup1 = BeautifulSoup(r1.content, "html.parser")

        for l in soup1.find_all(["a"], class_="sc-1cf7u6r-0 cnA-dzZ"):
            marquesLinks.append(("http://avito.ma" + l.get("href")).replace("/", "%"))

        for d in soup1.find_all(class_="indexstyled__ExtraValue-sc-nuvlnz-4 rCqTH"):
            min_data.append(d.text)

        for i in range(0, len(min_data), 4):
            big_data.append(min_data[i:i+4])
        min_data = []

        for prix in soup1.find_all(class_="indexstyled__Price-sc-qk2ak8-8 dwDUei"):
            prices.append(prix.text)
        try:
            image = soup1.find(class_="indexstyled__ModelPicture-sc-bpz6xp-6 jHrfRA").findChildren()[0]['src']
        except:
            image = "https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM="

        for marq in soup1.find_all(class_="indexstyled__VersionName-sc-qk2ak8-4 hqIUew"):

            marques.append(marq.text)



        if len(prices) != len(marquesLinks):
            for i in range(len(marquesLinks)-len(prices)):
                prices.append("Prix non disponible")

        for i in range(len(prices) - len(images)):
            images.append(image)
    
    myList = list(zip(prices,marques,images,big_data, marquesLinks))

    return render(request, "car.html", {'myList':myList})  

def contact(request):
    return render(request, "contact.html")

def main(request):
    return render(request, "main.html")

def saisie(request):
    
    lien_parent = "https://www.avito.ma/auto/neuf"

    marque = request.GET.get('marque')
    modele = request.GET.get('model')
    annee = request.GET.get('annee')
    carburant = request.GET.get('carburant')
    boiteVitesse = request.GET.get("bVitesse")
    prixmin = request.GET.get('prixmin')
    prixmax = request.GET.get('prixmax')
    pfmin = request.GET.get('pfmin')
    pfmax = request.GET.get('pfmax')

    if marque:
        marque = "/"+marque
    if modele:
        modele = ("/"+modele).replace(" ", "-")
    if prixmin:
        prixmin = "&prix_min="+prixmin
    if prixmax:
        prixmax = "&prix_max="+prixmax
    if carburant:
        carburant = "&carburant="+carburant
    if boiteVitesse:
        boiteVitesse = "&transmission="+boiteVitesse
    if pfmin:
        pfmin = "&chevaux_fiscaux_min="+pfmin
    if pfmax:
        pfmax = "&chevaux_fiscaux_max="+pfmax

    min_data = []
    big_data = []
    prices = []

    links = []
    images = []

    marques = []
    marquesLinks = []

    
    lien_parent += (marque + modele + "/?o=1"+prixmin + prixmax + carburant + boiteVitesse + pfmin + pfmax + "&annee=2022")
    print(lien_parent)
    r = requests.get(lien_parent)
    soup = BeautifulSoup(r.content, "html.parser")

    for l in soup.find_all(["a"], class_="sc-1cf7u6r-0 cnA-dzZ"):
        marquesLinks.append(("http://avito.ma" + l.get("href")).replace("/", "%"))
    for d in soup.find_all(class_="indexstyled__ExtraValue-sc-nuvlnz-4 rCqTH"):
        min_data.append(d.text)

    for prix in soup.find_all(class_="indexstyled__Price-sc-qk2ak8-8 dwDUei"):
        prices.append(prix.text)

    for marq in soup.find_all(class_="indexstyled__SEOName-sc-qk2ak8-5 fntUMS"):
        marques.append(marq.text)

    try:
        image = soup.find(class_="indexstyled__ModelPicture-sc-bpz6xp-6 jHrfRA").findChildren()[0]['src']
    except:
        image = "https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM="
    if image == "":
        image = "https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM="



    for i in range(0, len(min_data), 4):
        big_data.append(min_data[i:i+4])
            

    if len(prices) != len(big_data):
        for i in range(len(big_data)-len(prices)):
            prices.append("Prix non disponible")

    for i in range(len(big_data)-len(images)):
        images.append(image)
    
    myList = list(zip(prices,marques,images,big_data, marquesLinks))
    print(lien_parent)

    return render(request, 'saisie.html', {'myList':myList, 'annee':annee})

def logos(request, logospage):
    
    lien_parent = "https://www.avito.ma/auto/neuf/"
    marque = logospage
    annee = ""

    min_data = []
    big_data = []
    prices = []

    links = []
    images = []

    marques = []
    marquesLinks = []
    lien_parent += marque + "/?annee=" + str(annee)

    r = requests.get(lien_parent)
    soup = BeautifulSoup(r.content, "html.parser")

    for link1 in soup.find_all(["a"], class_="modelsstyled__ModelContainer-sc-1pawqcb-1 emkgBn"):
        links.append("http://avito.ma" + link1.get("href"))

    for a in links:
        r1 = requests.get(a)
        soup1 = BeautifulSoup(r1.content, "html.parser")

        for l in soup1.find_all(["a"], class_="sc-1cf7u6r-0 cnA-dzZ"):
            marquesLinks.append(("http://avito.ma" + l.get("href")).replace("/", "%"))

        for d in soup1.find_all(class_="indexstyled__ExtraValue-sc-nuvlnz-4 rCqTH"):
            min_data.append(d.text)

        for i in range(0, len(min_data), 4):
            big_data.append(min_data[i:i+4])
        min_data = []

        for prix in soup1.find_all(class_="indexstyled__Price-sc-qk2ak8-8 dwDUei"):
            prices.append(prix.text)
        try:
            image = soup1.find(class_="indexstyled__ModelPicture-sc-bpz6xp-6 jHrfRA").findChildren()[0]['src']
        except:
            image = "https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM="

        for marq in soup1.find_all(class_="indexstyled__VersionName-sc-qk2ak8-4 hqIUew"):

            marques.append(marq.text)



        if len(prices) != len(marquesLinks):
            for i in range(len(marquesLinks)-len(prices)):
                prices.append("Prix non disponible")

        for i in range(len(prices) - len(images)):
            images.append(image)

    myList = list(zip(prices,marques,images,big_data, marquesLinks))
    

    return render(request, 'logos.html', {'myList':myList})
    
def rec(request, recpage):


    min_data = []
    big_data = []
    prices = []

    links = []
    images = []

    marques = []
    marquesLinks = []

    
    lien_parent = recpage.replace("%", "/")+ "/?annee="

    r = requests.get(lien_parent)
    soup = BeautifulSoup(r.content, "html.parser")

    for l in soup.find_all(["a"], class_="sc-1cf7u6r-0 cnA-dzZ"):
        marquesLinks.append(("http://avito.ma" + l.get("href")).replace("/", "%"))
    for d in soup.find_all(class_="indexstyled__ExtraValue-sc-nuvlnz-4 rCqTH"):
        min_data.append(d.text)

    for prix in soup.find_all(class_="indexstyled__Price-sc-qk2ak8-8 dwDUei"):
        prices.append(prix.text)

    for marq in soup.find_all(class_="indexstyled__SEOName-sc-qk2ak8-5 fntUMS"):
        marques.append(marq.text)

    try:
        image = soup.find(class_="indexstyled__ModelPicture-sc-bpz6xp-6 jHrfRA").findChildren()[0]['src']
    except:
        image = "https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM="



    for i in range(0, len(min_data), 4):
        big_data.append(min_data[i:i+4])
            

    if len(prices) != len(big_data):
        for i in range(len(big_data)-len(prices)):
            prices.append("Prix non disponible")

    for i in range(len(big_data)-len(images)):
        images.append(image)

    myList = list(zip(prices,marques,images,big_data, marquesLinks))
    print(lien_parent)
    return render(request, "rec.html", {"myList":myList})

def saisieOccasion(request, pageNbr):
    marque = request.GET.get("marque")
    modele = request.GET.get("model").replace(" ", "-").lower()
    ville = request.GET.get("ville").replace(" ", "_").lower()
    regdate_min = request.GET.get("datemin")
    regdate_max = request.GET.get("datemax")
    mielage_min = request.GET.get("kmin")
    mielage_max = request.GET.get("kmax")
    fuel = request.GET.get("carburant")
    doors = request.GET.get("porte")
    gear_box = request.GET.get("bVitesse")
    price_min = request.GET.get("prixmin")
    price_max = request.GET.get("prixmax")
    puissance_fiscale_min = request.GET.get("pfmin")
    puissance_fiscale_max = request.GET.get("pfmax")

    dict_marques = {"Dacia": 13, "Renault":49, "Hyundai":24, "Peugeot":46, "Fiat":17, "Volkswagen":58, "Citroen":12, "Ford":18, "Toyota":56, "Nissan":44, "Mercedes-benz":41, "Bmw":5, "Audi":3, "Jeep":29, "Land-rover":33, "Alfa romeo":1, "Jaguar":28, "Seat":50, "Opel":45, "Abarth":6, "Byd":6, "Chevrolet":10, "Daewoo":61, "Daihatsu":14, "Dodge":15, "Isuzu":26, "Honda":22, "Lancia":32, "Lexus":34, "Mahindra":36, "Mazda":40, "Mitsubishi":43, "Mini":42, "Skoda":51, "Ssangyong":53, "Subaro":54, "Fuso":54, "Gazelle":54, "Hino":54, "Iveco":27, "Tata":27, "Kaicene":27}
    dict_dates = {"1981":1, "1982":2, "1983":3, "1984":4, "1985":5, "1986":6, "1987":7, "1988":8, "1989":9, "1990":10, "1991":11, "1992":12, "1993":13, "1994":14, "1995":15, "1996":16, "1997":17, "1998":18, "1999":19, "2000":20, "2001":21, "2002":22, "2003":23, "2004":24, "2005":25, "2006":26, "2007":27, "2008":28, "2009":29, "2010":30, "2011":31, "2012":32, "2013":33, "2014":34, "2015":35, "2016":36, "2017":37, "2018":38, "2019":39, "2020":40, "2021":41, "2022":42}
    dict_mielage = {"10000":2, "20000":4, "30000":6, "40000":8, "50000":10, "60000":12, "70000":14, "80000":16, "90000":18, "100000":20, "110000":21, "120000":22, "130000":23, "140000":24, "150000":25, "160000":26, "170000":27, "180000":28, "190000":29, "200000":30, "250000":31, "300000":32, "350000":33, "400000":34, "450000":35, "500000":36}
    dict_fuel = {"Diesel":1, "Essence":2, "Electrique":3, "LPG":4, "Hybride":5}
    dict_doors = {"3 Portes": 0, "5 Portes":1}
    dict_gear_box = {"Automatique":0, "Manuelle":1}
    dict_puissance_fiscale = {"4":1, "5":2, "6":3, "7":4, "8":5, "9":6, "10":7, "11":8, "12":9, "13":10, "14":11}

    if mielage_max:
        if int(mielage_max) <10000:
            mielage_max = 10000
        elif int(mielage_max) <20000:
            mielage_max = 20000
        elif int(mielage_max) <30000:
            mielage_max = 30000
        elif int(mielage_max) <40000:
            mielage_max = 40000
        elif int(mielage_max) <50000:
            mielage_max = 50000
        elif int(mielage_max) <60000:
            mielage_max = 60000
        elif int(mielage_max) <70000:
            mielage_max = 70000
        elif int(mielage_max) <80000:
            mielage_max = 80000
        elif int(mielage_max) <90000:
            mielage_max = 90000
        elif int(mielage_max) <100000:
            mielage_max = 100000
        elif int(mielage_max) <110000:
            mielage_max = 110000
        elif int(mielage_max) <120000:
            mielage_max = 120000
        elif int(mielage_max) <130000:
            mielage_max = 130000
        elif int(mielage_max) <140000:
            mielage_max = 140000
        elif int(mielage_max) <150000:
            mielage_max = 150000
        elif int(mielage_max) <160000:
            mielage_max = 160000
        elif int(mielage_max) <170000:
            mielage_max = 170000
        elif int(mielage_max) <180000:
            mielage_max = 180000
        elif int(mielage_max) <190000:
            mielage_max = 190000
        elif int(mielage_max) <200000:
            mielage_max = 200000
        elif int(mielage_max) <250000:
            mielage_max = 250000
        elif int(mielage_max) <300000:
            mielage_max = 300000
        elif int(mielage_max) <350000:
            mielage_max = 350000
        elif int(mielage_max) <400000:
            mielage_max = 400000
        elif int(mielage_max) <450000:
            mielage_max = 450000
        elif int(mielage_max) <500000:
            mielage_max = 500000

    if mielage_min:
        if int(mielage_min) <10000:
            mielage_min = 10000
        elif int(mielage_min) <20000:
            mielage_min = 20000
        elif int(mielage_min) <30000:
            mielage_min = 30000
        elif int(mielage_min) <40000:
            mielage_min = 40000
        elif int(mielage_min) <50000:
            mielage_min = 50000
        elif int(mielage_min) <60000:
            mielage_min = 60000
        elif int(mielage_min) <70000:
            mielage_min = 70000
        elif int(mielage_min) <80000:
            mielage_min = 80000
        elif int(mielage_min) <90000:
            mielage_min = 90000
        elif int(mielage_min) <100000:
            mielage_min = 100000
        elif int(mielage_min) <110000:
            mielage_min = 110000
        elif int(mielage_min) <120000:
            mielage_min = 120000
        elif int(mielage_min) <130000:
            mielage_min = 130000
        elif int(mielage_min) <140000:
            mielage_min = 140000
        elif int(mielage_min) <150000:
            mielage_min = 150000
        elif int(mielage_min) <160000:
            mielage_min = 160000
        elif int(mielage_min) <170000:
            mielage_min = 170000
        elif int(mielage_min) <180000:
            mielage_min = 180000
        elif int(mielage_min) <190000:
            mielage_min = 190000
        elif int(mielage_min) <200000:
            mielage_min = 200000
        elif int(mielage_min) <250000:
            mielage_min = 250000
        elif int(mielage_min) <300000:
            mielage_min = 300000
        elif int(mielage_min) <350000:
            mielage_min = 350000
        elif int(mielage_min) <400000:
            mielage_min = 400000
        elif int(mielage_min) <450000:
            mielage_min = 450000
        elif int(mielage_min) <500000:
            mielage_min = 500000
    
    if ville :
        ville+= "/voitures-à_vendre?"+"o="+str(pageNbr)
    else:
        ville+= "maroc/voitures-à_vendre?"+"o="+str(pageNbr)
    if fuel :
        fuel = "fuel=" + str(dict_fuel[fuel])
    if gear_box:
        gear_box = "&gear_box="+str(dict_gear_box[gear_box])
    if doors:
        doors = "&doors="+str(dict_doors[doors])
    if marque:
        marque = "&brand="+str(dict_marques[marque])
    if modele:
        modele = "&model="+modele
    if price_min:
        price_min = "&price_min="+price_min
    if price_max:
        price_max = "&price_max="+price_max
    if mielage_min:
        mielage_min = "&mileage_min="+str(dict_mielage[mielage_min])
    if mielage_max:
        mielage_max = "&mileage_max="+str(dict_mielage[mielage_max])
    if regdate_min:
        regdate_min = "&regdate_min="+str(dict_dates[regdate_min])
    if regdate_max:
        regdate_max = "&regdate_max="+str(dict_dates[regdate_max])
    if puissance_fiscale_min:
        puissance_fiscale_min = "&pfiscale_min="+str(dict_puissance_fiscale[puissance_fiscale_min])
    if puissance_fiscale_max:
        puissance_fiscale_max = "&pfiscale_max="+str(dict_puissance_fiscale[puissance_fiscale_max])

    parent_link = "https://www.avito.ma/fr/"
    parent_link += (ville + fuel + gear_box + doors + marque + modele + price_min + price_max + mielage_min + mielage_max + regdate_min + regdate_max + puissance_fiscale_min + puissance_fiscale_max)


    prices = []
    pageLink = []
    images = []
    myImages = []
    myImages1 = []
    listMarques = []
    listDates = []
    villes = []
    dates = []
    links = []

    r = requests.get(parent_link)
    soup = BeautifulSoup(r.content, "html.parser")

    conteneur_prix = soup.find_all(class_="sc-1x0vz2r-0 izsKzL oan6tk-15 cdJtEx")


    for prix in conteneur_prix:
        prices.append(prix.text)

    for mrq in soup.find_all(class_="oan6tk-17 ewuNqy"):
        listMarques.append(mrq.text)
    for dt in soup.find_all(class_="sc-1x0vz2r-0 hCOOjL"):
        listDates.append(dt.text)

    villes = listDates[1::2]
    dates = listDates[::2]

    for link in soup.find_all(["a"], class_="oan6tk-1 fFOxTQ"):
        pageLink.append(link.get("href"))
        links.append(link.get("href").replace("/", "%"))
    
    for description_Link in pageLink:
        re = requests.get(description_Link)
        newsoup = BeautifulSoup(re.content, "html.parser")

        for i in newsoup.find_all(class_="sc-1gjavk-0 kkNvdK"):
            images.append(i.get("src"))
        if (len(images))>=2:
            myImages.append(images[0])
            myImages1.append(images[1])
        else :
            myImages.append("https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM=")
            myImages1.append("https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM=")
        images = []
    myList3 = list(zip(prices,listMarques,myImages,dates,villes,links, myImages1))
    print(parent_link)
    return render(request, "saisieOccasion.html", {"myList":myList3, "parentlink":[parent_link.replace("/", "%")]})

def occasion_details(request, detailsLink):

    re = requests.get("https://themoneyconverter.com/FR/MAD/EUR")
    newsoup = BeautifulSoup(re.content, "html.parser")

    for d in newsoup.find_all(id = "cc-ratebox"):
        madeuro = d.text.replace("EUR/MAD = ", "").replace(",", ".")
    try:
        madeuro = float(madeuro)
    except:
        madeuro = "convertion non disponible"
    
    images = []
    recImages = []
    recLink = []
    data_array1 = []
    data_array2 = []

    villeAnnonce = []
    dateAnnonce = []
    datevilleannonce = []
    donnesannonce = []
    description = []
    price = []
    marque = []
    prixeuro = []
    description_Link = detailsLink.replace("%", "/")
    re = requests.get(description_Link)
    newsoup = BeautifulSoup(re.content, "html.parser")

    for i in newsoup.find_all(class_="sc-1gjavk-0 kkNvdK"):
        images.append(i.get("src"))
    

    for b in newsoup.find_all("span", {"class": "sc-1x0vz2r-0 gCIGeB"}):
        datevilleannonce.append(b.text)
    for d in newsoup.find_all("span", {"class": "sc-1x0vz2r-0 kUjmne"}):
        donnesannonce.append(d.text)
    for desc in newsoup.find("p", {"class": "sc-ij98yj-0 iMUDvH"}):
        description.append(desc.text)
    for v in newsoup.find_all(class_="sc-1x0vz2r-0 iVDpDk"):
        data_array1.append(v.text)
    try:
        for p in newsoup.find("p", {"class": "sc-1x0vz2r-0 bGMGAj"}):
            price.append((p.text).replace("\u202f", " "))
            prixeuro.append(str(round(float((price[0].replace("DH","").replace(" ", ""))) * madeuro, 2))+" EUR €")
    except:
        price.append("prix non spécifié")
        prixeuro.append("prix non spécifié")
    for m in newsoup.find_all(class_="sc-1x0vz2r-0 glWiuP"):
        marque.append(m.text)

    for c in newsoup.find_all(class_="sc-1x0vz2r-0 brylYP"):
        data_array2.append(c.text)


    if len(datevilleannonce) == 0:
        villeAnnonce.append("nom de la ville non spécifié")
        dateAnnonce.append("date d'annonce non spécifié")
    else:

        villeAnnonce = datevilleannonce[::2]
        dateAnnonce = datevilleannonce[1::2]
    myList4 = list(zip(data_array1, data_array2))
    return render(request, "occasion-details.html", {"myList": myList4, "villeAnnonce":villeAnnonce, "dateAnnonce":dateAnnonce, "images":images, "donnesAnnonce":donnesannonce, "description":description, "descriptionLink":description_Link, "price":price, "marque":marque, "prixeuro":prixeuro})

def statistics(request):
    return render(request, "statistics.html")

def paginationOccasion(request, linkPage):
    parent_link = (linkPage.replace("%", "/")).replace("?o=1", "?o=2")

    prices = []
    pageLink = []
    images = []
    myImages = []
    myImages1 = []
    listMarques = []
    listDates = []
    villes = []
    dates = []
    links = []

    r = requests.get(parent_link)
    soup = BeautifulSoup(r.content, "html.parser")

    conteneur_prix = soup.find_all(class_="sc-1x0vz2r-0 izsKzL oan6tk-15 cdJtEx")


    for prix in conteneur_prix:
        prices.append(prix.text)

    for mrq in soup.find_all(class_="oan6tk-17 ewuNqy"):
        listMarques.append(mrq.text)
    for dt in soup.find_all(class_="sc-1x0vz2r-0 hCOOjL"):
        listDates.append(dt.text)

    villes = listDates[1::2]
    dates = listDates[::2]

    for link in soup.find_all(["a"], class_="oan6tk-1 fFOxTQ"):
        pageLink.append(link.get("href"))
        links.append(link.get("href").replace("/", "%"))
    
    for description_Link in pageLink:
        re = requests.get(description_Link)
        newsoup = BeautifulSoup(re.content, "html.parser")

        for i in newsoup.find_all(class_="sc-1gjavk-0 kkNvdK"):
            images.append(i.get("src"))
        if (len(images))>=2:
            myImages.append(images[0])
            myImages1.append(images[1])
        else :
            myImages.append("https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM=")
            myImages1.append("https://media.istockphoto.com/vectors/default-image-icon-vector-missing-picture-page-for-website-design-or-vector-id1357365823?b=1&k=20&m=1357365823&s=170667a&w=0&h=y6ufWZhEt3vYWetga7F33Unbfta2oQXCZLUsEa67ydM=")
        images = []
    myList3 = list(zip(prices,listMarques,myImages,dates,villes,links, myImages1))
    print(parent_link)
    
    return render(request, "paginationOccasion.html", {"myList":myList3})

def comparaison(request):

    dict_marques = {"Dacia": 13, "Renault": 49, "Hyundai": 24, "Peugeot": 46, "Fiat": 17, "Volkswagen": 58, "Citroen": 12,
                    "Ford": 18, "Toyota": 56, "Nissan": 44, "Mercedes-benz": 41, "Bmw": 5, "Audi": 3, "Jeep": 29,
                    "Land-rover": 33, "Alfa romeo": 1, "Jaguar": 28, "Seat": 50, "Opel": 45, "Abarth": 6, "Byd": 6,
                    "Chevrolet": 10, "Daewoo": 61, "Daihatsu": 14, "Dodge": 15, "Isuzu": 26, "Honda": 22, "Lancia": 32,
                    "Lexus": 34, "Mahindra": 36, "Mazda": 40, "Mitsubishi": 43, "Mini": 42, "Skoda": 51, "Ssangyong": 53,
                    "Subaro": 54, "Fuso": 54, "Gazelle": 54, "Hino": 54, "Iveco": 27, "Tata": 27, "Kaicene": 27}
    dict_dates = {"1981": 1, "1982": 2, "1983": 3, "1984": 4, "1985": 5, "1986": 6, "1987": 7, "1988": 8, "1989": 9,
                "1990": 10, "1991": 11, "1992": 12, "1993": 13, "1994": 14, "1995": 15, "1996": 16, "1997": 17,
                "1998": 18, "1999": 19, "2000": 20, "2001": 21, "2002": 22, "2003": 23, "2004": 24, "2005": 25,
                "2006": 26, "2007": 27, "2008": 28, "2009": 29, "2010": 30, "2011": 31, "2012": 32, "2013": 33,
                "2014": 34, "2015": 35, "2016": 36, "2017": 37, "2018": 38, "2019": 39, "2020": 40, "2021": 41,
                "2022": 42}

    marque = request.GET.get("marque2")
    model = request.GET.get("model2").lower()
    regdate_min = request.GET.get("annee2")

    marques = "brand=" + str(dict_marques[marque])
    regdate_mins = str(dict_dates[regdate_min])

    url = f"https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre?{marques}&model={model}&regdate_min={regdate_mins}&regdate_max={regdate_mins}"
    

    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    prix_avito = []
    images_avito = []
    link_avito = []
    image_avito = []

    for test in doc.find_all('span', class_="sc-1x0vz2r-0 izsKzL oan6tk-15 cdJtEx"):
        prix_avito.append(test.get_text().replace("DH", "").replace(" ", ""))

    for i in doc.find_all(["a"], class_="oan6tk-1 fFOxTQ"):
        link_avito.append(i['href'])

    erreur = []
    prix_moteur = []
    link_moteur = []
    images_moteur = []

    url_moteur = f"https://www.moteur.ma/fr/voiture/achat-voiture-occasion/recherche/?marque={marque}&modele={model}&annee_min={regdate_min}&annee_max={regdate_min}"
    page = requests.get(url_moteur).text
    doc = BeautifulSoup(page, "html.parser")

    for test in doc.find_all('div', class_="text"):
        erreur.append(test.get_text(strip=True))

    err = erreur

    a = True
    while (a == True):
        if err == "Désolé ! aucune annonce ne correspond à votre recherche.retrouvez ci-dessous les résultats de recherche obtenus en éliminant les critères suivants :":
            print("aucune annonce ne correspond à votre recherche dans moteur.ma")
            break


        else:
            for test in doc.find_all('div', class_="price color_primary PriceListing"):
                prix_moteur.append(test.get_text(strip=True).replace("Dhs", "").replace(" ", ""))

            for test in doc.find_all(['div'], class_="content-inner"):
                link_moteur.append(test.findChildren()[1]['href'])

            a = False

    print(prix_avito)
    for i in range(len(prix_avito)):
        if prix_avito[i] == "Prixnonspecifié":
            prix_avito[i] = 1000000000000
        else:
            prix_avito[i] = int(prix_avito[i])
    if not err:
        try:
            for i in range(len(prix_moteur)):
                prix_moteur[i] = int(prix_moteur[i])
        except:
            prix_moteur.append(1000000000000)

        moteur = list(zip(prix_moteur, link_moteur))
        #
        try:
            min_moteur = min(moteur)
        except:
            min_moteur = (1000000000000, "#")
        lien_moteur = min_moteur[1]
        price_moteur = [min_moteur[0]]
    else:
        moteur = [(1000000000000000000, "#")]
        min_moteur = (1000000000000000000, "#")
        lien_moteur = ("#")
        price_moteur = [1000000000000000000]

    avito = list(zip(prix_avito, link_avito))
    try:
        min_avito = min(avito)
    except:
        min_avito = (1000000000000, "#")
    lien_avito = min_avito[1]
    price_avito = [min_avito[0]]

    min_sites = min(min_moteur, min_avito)
    best_price = [min_sites[0]]
    liste_comparaison = moteur + avito
    try:
        b = min(liste_comparaison)
    except:
        b = (1000000000000, "#")
    lien_min_site = b[1]


    try:
        page = requests.get(lien_avito).text
        doc = BeautifulSoup(page, "html.parser")

        for test in doc.find_all(['img'], class_="sc-1gjavk-0 kkNvdK"):
            images_avito.append(test['src'])
        image_avito.append(images_avito)
    except:
        images_avito.append("no image")

    try:
        page = requests.get(lien_moteur).text
        doc = BeautifulSoup(page, "html.parser")
        for img in doc.find_all(class_="image-hb"):
            images_moteur.append(img['src'])
    except:
        images_moteur.append("no image")
    #myList5 = list(zip(prices,listMarques,myImages,dates,villes,links, myImages1))
    return render(request, "comparaison.html", {"price_avito":price_avito, "price_moteur":price_moteur, "best_price":best_price, "images_moteur":images_moteur, "images_avito":images_avito, "lien_moteur":lien_moteur.replace("/", "%"), "lien_avito":lien_avito.replace("/", "%"), "marque":marque, "model":model, "annee":regdate_min})