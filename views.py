from app import app
from flask import Flask, jsonify, make_response
from flask_api import status as st
import time
from threading import Thread
import sqlite3


class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM clientBase"
        cursor.execute(sql)
        accounts = cursor.fetchall()
        for e in range(len(accounts)):
            if accounts[e][4] == 0:
                continue
            if accounts[e][2] < accounts[e][3]:
                sql = """UPDATE clientBase SET holds=? WHERE number=?"""
                cursor.execute(sql, [accounts[e][3] - accounts[e][2], accounts[e][0]])
                sql = """UPDATE clientBase SET balance=? WHERE number=?"""
                cursor.execute(sql, [0, accounts[e][0]])
            else:
                sql = """UPDATE clientBase SET balance=? WHERE number=?"""
                cursor.execute(sql, [accounts[e][2] - accounts[e][3], accounts[e][0]])
                sql = """UPDATE clientBase SET holds=? WHERE number=?"""
                cursor.execute(sql, [0, accounts[e][0]])
        conn.commit()
        cursor.close()
        time.sleep(600)
        self.run()


my_thread = MyThread('mt')
my_thread.start()


@app.route('/api/status/<string:num>', methods=['GET'])
def get_status(num):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM clientBase WHERE number=?"
    cursor.execute(sql, [num])
    account = cursor.fetchall()
    cursor.close()
    if len(account) == 0:
        http_status = st.HTTP_404_NOT_FOUND
        result = False
        description = "Information not found."
        addition = None
    else:
        addition = {"number: ": account[0][0],
                    "fio: ": account[0][1],
                    "balance: ": account[0][2],
                    "holds: ": account[0][3],
                    "status: ": account[0][4]}
        http_status = st.HTTP_200_OK
        result = True
        description = "Status of this account."
    return make_response(jsonify({'http status:': http_status,
                                  'result:': result,
                                  'addition:': addition,
                                  "description:": description}), http_status)


@app.route('/api/ping', methods=['GET'])
def check_ping():
    return make_response(jsonify({'status:': st.HTTP_200_OK,
                                  'result:': True,
                                  'addition:': None,
                                  "description:": "Ping is Alright!"}), 200)


@app.route('/api/add/<string:num>/<int:sum>', methods=['GET'])
def add_money(num, sum):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM clientBase WHERE number=?"
    cursor.execute(sql, [num])
    account = cursor.fetchall()
    if len(account) != 0 and isinstance(sum, int) and sum >= 0 and account[0][4] == 1:
        sql = """UPDATE clientBase SET balance=? WHERE number=?"""
        cursor.execute(sql, [account[0][2] + sum, num])
        conn.commit()
        cursor.close()
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM clientBase WHERE number=?"
        cursor.execute(sql, [num])
        account = cursor.fetchall()
        addition = {"number: ": account[0][0],
                    "fio: ": account[0][1],
                    "balance: ": account[0][2],
                    "holds: ": account[0][3],
                    "status: ": account[0][4]}
        http_status = st.HTTP_202_ACCEPTED
        result = True
        description = "Receipt to the account was successful!"
    else:
        cursor.close()
        http_status = st.HTTP_412_PRECONDITION_FAILED
        result = False
        description = "Bad command or closed account."
        addition = None
    return make_response(jsonify({'status:': http_status,
                                  'result:': result,
                                  'addition:': addition,
                                  "description:": description}), http_status)


@app.route('/api/substract/<string:num>/<int:sum>', methods=['GET'])
def substruct_money(num, sum):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM clientBase WHERE number=?"
    cursor.execute(sql, [num])
    account = cursor.fetchall()
    result = int(account[0][2]) - int(account[0][3]) - sum
    if len(account) != 0 and isinstance(sum, int) and sum >= 0 and account[0][4] == 1 and result >= 0:
        sql = """UPDATE clientBase SET holds=? WHERE number=?"""
        cursor.execute(sql, [account[0][3] + sum, num])
        conn.commit()
        cursor.close()
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM clientBase WHERE number=?"
        cursor.execute(sql, [num])
        account = cursor.fetchall()
        addition = {"number: ": account[0][0],
                    "fio: ": account[0][1],
                    "balance: ": account[0][2],
                    "holds: ": account[0][3],
                    "status: ": account[0][4]}
        http_status = st.HTTP_202_ACCEPTED
        result = True
        description = "Debit was successful"
    else:
        cursor.close()
        http_status = st.HTTP_412_PRECONDITION_FAILED
        result = False
        description = "Bad command or closed account or insufficient funds."
        addition = None
    return make_response(jsonify({'status:': http_status,
                                  'result:': result,
                                  'addition:': addition,
                                  "description:": description}), http_status)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status:': st.HTTP_404_NOT_FOUND,
                                  'result:': False,
                                  'addition:': None,
                                  "description:": "Information not found."}), 404)
