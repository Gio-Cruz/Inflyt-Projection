import requests
import lxml.html as lh

# takes latitude and longitude in decimal degrees and returns list of object IDs
def get_object_ids(ra,dec):
    # set radius in arcminn
    radius = "10";
    #ra_ls = ra.split(" ")
    #dec_ls = dec.split(" ")
    coord_str = ra + "+" + dec
    url = "http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord=" + coord_str + "&CooFrame=ICRS&CooEpoch=J2000&&Radius=" + radius + "&Radius.unit=arcmin"
    print(url)
    response = requests.get(url)
    doc = lh.fromstring(response.content)
    tr_elements = doc.xpath('//tr')
    if len(tr_elements) == 1:
        return {'IDs': [], 'Types': []}
    tr_elements = tr_elements[4:]
    object_IDs = []
    object_types = []
    for i in range(1,len(tr_elements)):
        if '*' in tr_elements[i][3].text_content() or 'G' in tr_elements[i][3].text_content():
            object_IDs.append(tr_elements[i][1].text_content().replace("\n","").rstrip())
            object_types.append(tr_elements[i][3].text_content().replace("\n","").rstrip())
    rtn_dict = {'IDs':object_IDs, 'Types':object_types}
    return rtn_dict