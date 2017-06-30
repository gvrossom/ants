from django.shortcuts import render

def get_ref_id():
    """ Loop to get a unique ref id. """
    ref_id = str(uuid.uuid4())[:11].replace('-','').lower()
    try:
        id_exists = Landing.objects.get(ref_id=ref_id)
        get_ref_id()  ## creates a loop until the ref_id is not already in the db
    except:
        return ref_id
