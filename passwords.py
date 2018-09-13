import os

# Set your api tokens and keys through environmental variables
# (add lines to your .bashrc and restart terminal):
# export LOMONOSOV_AUTH_LOGIN='first_name.second_name'
# export LOMONOSOV_AUTH_PSWD='corp_password'
#
# OR
#
# Manually through defaults in this file
# Important: untrack file to prevent accidential private token pushing:
# 'git update-index --assume-unchanged tokens.py'

# [ Required ]

default_auth_login = ''
auth_login = os.getenv('LOMONOSOV_AUTH_LOGIN', default_auth_login)

default_auth_pswd = ''
auth_pswd = os.getenv('LOMONOSOV_AUTH_PSWD', default_auth_pswd)
