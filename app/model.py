from pydantic import BaseModel


class UpdateText(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    Properties:
        set_id (str): set_id
        text (str): text for update
        name (str): file name
    """
    
    set_id: str
    text: str
    name: str
