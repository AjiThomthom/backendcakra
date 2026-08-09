from helpers.user_helpers.search_user_helpers import SearchUserHelpers
from helpers.user_helpers.all_users_helpers import AllUsersHelpers
from helpers.user_helpers.update_selected_user_helpers import SelectedUserHelpers
from helpers.user_helpers.summary_helpers import SummaryHelpers
from lib.db import db

async def search_user(username : str, request):
    return await SearchUserHelpers(request, username, db)

async def get_all_users(request):
    return await AllUsersHelpers(request,db)
  
async def update_selected_users(id,body, request):
    return await SelectedUserHelpers(request,db, body, id)

async def get_summary_data(request):
    return await SummaryHelpers(request,db)