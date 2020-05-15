import pymysql
# from rpc4django import rpcmethod

pymysql.install_as_MySQLdb()

# The doc string supports reST if docutils is installed
# @rpcmethod(name='mynamespace.add', signature=['int', 'int', 'int'])
# def add(a, b):
#     """Adds two numbers together
#     >>> add(1, 2)
#     3
#     """
#
#     return a + b
