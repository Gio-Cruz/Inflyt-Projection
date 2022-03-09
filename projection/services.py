import requests
import lxml.html as lh

# takes latitude and longitude in decimal degrees and returns list of object IDs
def get_object_ids(ra,dec):
    # set radius in arcminn
    radius = "10";
    # add priorities for searching ID (for N element array, Nth element has highest priority) max 3 letters
    const_ls = ["Cyg","Lac","HD"]
    #ra_ls = ra.split(" ")
    #dec_ls = dec.split(" ")
    coord_str = ra + "+" + dec
    url = "http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord=" + coord_str + "&CooFrame=ICRS&CooEpoch=J2000&&Radius=" + radius + "&Radius.unit=arcmin"
    print(url)
    response = requests.get(url)
    doc = lh.fromstring(response.content)
    tr_elements = doc.xpath('//tr')
    if len(tr_elements) == 1:
        return {'IDs': [], 'Types': [], 'Ra': [], 'Dec': []}
    tr_elements = tr_elements[4:]
    object_IDs = []
    object_types = []
    object_ra = []
    object_dec = []
    swap_fl = 0; #check if already swapped
    for i in range(1,len(tr_elements)):
        if '*' in tr_elements[i][3].text_content() or 'G' in tr_elements[i][3].text_content():
            ID = tr_elements[i][1].text_content().replace("\n","").rstrip()
            Type = tr_elements[i][3].text_content().replace("\n","").rstrip()
            obj_ra = tr_elements[i][4].text_content().replace("\n22","").rstrip()
            obj_dec = tr_elements[i][5].text_content().replace("\n","").rstrip()

            object_IDs.append(ID)
            object_types.append(Type)
            object_ra.append(obj_ra)
            object_dec.append(obj_dec)

            # if no priority element has been swapped, check object ID for priority
            if swap_fl == 0:
                for const_id in const_ls:
                    if const_id in ID:
                        # swap element to 0th index in object_IDs
                        i1 = object_IDs.index(ID)
                        i2 = 0 #0th element to swap
                        object_IDs[i1],object_IDs[i2] = object_IDs[i2],object_IDs[i1]
                        object_types[i1],object_types[i2] = object_types[i2],object_types[i1]
                        object_ra[i1],object_ra[i2] = object_ra[i2],object_ra[i1]
                        object_dec[i1],object_dec[i2] = object_dec[i2],object_dec[i1]

                        swap_fl = 1
                        break #end search, we have found priority object
                    
                        
                    
    rtn_dict = {'IDs':object_IDs, 'Types':object_types, 'Ra': object_ra, 'Dec': object_dec}
    return rtn_dict