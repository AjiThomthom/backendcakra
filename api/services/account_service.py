from fastapi import  Response
from helpers.account_helpers.sign_in_helpers import SignInHelper
from helpers.account_helpers.sign_up_helpers import SignUpHelpers
from helpers.account_helpers.sign_out_helpers import SignOutHelpers
from lib.db import db

async def sign_in_account(body, response: Response):
    return await SignInHelper(body, db, response)

async def create_account(body):
    return await SignUpHelpers(db, body)

async def sign_out_account(response: Response):
    return await SignOutHelpers(response)