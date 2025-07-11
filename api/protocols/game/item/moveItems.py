from dataclasses import dataclass

@dataclass
class move_items:
    status_code: int
    previous_pos: any
    target_items: any
    
def item_moveItems(previous_pos, target_items):
    data = move_items(
        status_code=0,
        previous_pos=previous_pos,
        target_items=target_items
    )
    return data