async def analyse_order(orders:list):
    pending_count, finished_count, active_count = 0,0,0
    for order in orders:
        if order["status"] == "pending":
            pending_count +=1
        elif order["status"] == "active":
            active_count += 1
        if order["status"] == "finished":
            finished_count
    
    return {'pending':pending_count,
            'active':active_count,
            'finished': finished_count
            }