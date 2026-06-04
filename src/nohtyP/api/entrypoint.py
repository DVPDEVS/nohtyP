from nohtyP.global_utilities.decorators import api_level
@api_level(1)
def entry() -> bool:
    #? this is called when running this package with "python -m nohtyP"
    # sanitize args and call funcs based on them.
    ...