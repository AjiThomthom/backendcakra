from lib.db import db
from helpers.history_helpers.search_helpers import SearchHelpersHistory
from helpers.history_helpers.all_history_helpers import AllHistoryHelpers
from helpers.history_helpers.update_history_helpers import UpdateHistoryHelpers
from helpers.history_helpers.create_history_helpers import CreateHistoryHelpers

async def get_search_name(request,s, page, limit):
    return await SearchHelpersHistory(request, page, limit, s, db)
    
async def get_all_history (
        request,
        status_history,
        date,
        page,
        limit
):
    return await AllHistoryHelpers(request, limit, page, date, status_history,db)

async def update_history (request,body,id):
   return UpdateHistoryHelpers(request,body, db,id)

async def created_history (body):
    return CreateHistoryHelpers(body,db)