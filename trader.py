#coding=utf-8

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui  import *  
from PyQt4.QtCore import * 

from trader_ui import Ui_MainWindow
import uqer
import easytrader

import json

import datetime as dt
import tushare as ts



class uqWindow(QtGui.QMainWindow, Ui_MainWindow):    
    def __init__(self):    
        super(uqWindow,self).__init__()    
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.login_account)   
        self.strategy_comboBox.activated.connect(self.strategy_select)
        self.place_order_btn.clicked.connect(self.order_place)

        self.uqer_username_lineEdit.textChanged.connect(self.edit_change_uqer)
        self.uqer_pwd_lineEdit.textChanged.connect(self.edit_change_uqer)

        self.uqer_username_lineEdit.textChanged.connect(self.edit_change_broker)
        self.broker_trade_pwd_lineEdit.textChanged.connect(self.edit_change_broker)
        self.broker_c_pwd_lineEdit.textChanged.connect(self.edit_change_broker)

        self.login_frame.show()
        self.table_frame.hide()

        self.load_config()

    def edit_change_uqer(self):
        self.uqer_verify_label.setText('')

    def edit_change_broker(self):
        self.broker_verify_label.setText('')

    def login_account(self):

        uqer_user = str(self.uqer_username_lineEdit.text())
        uqer_pwd  = str(self.uqer_pwd_lineEdit.text())

        broker_account = str(self.broker_account_lineEdit.text())
        broker_trade_pwd = str(self.broker_trade_pwd_lineEdit.text())
        broker_c_pwd = str(self.broker_c_pwd_lineEdit.text())

        self.percent = 0.01
        if not uqer_user or not uqer_pwd:
            self.uqer_verify_label.setText(u'字段不能为空!')
            self.uqer_verify_label.setStyleSheet('color: red')

        if not broker_account or not broker_trade_pwd or not broker_c_pwd:
            self.broker_verify_label.setText(u'字段不能为空!')
            self.broker_verify_label.setStyleSheet('color: red')
        try:
            self.uqer_instance = uqer.Uqer(uqer_user, uqer_pwd, self.percent)
            self.uqer_verify_label.setText('')
        except Exception,e:
            self.uqer_verify_label.setText(u'登陆失败，请检查用户名密码!')
            self.uqer_verify_label.setStyleSheet('color: red')
            return
        

        self.account_instance = easytrader.use('ht')
        self.account_instance.account_config = {
              "userName": broker_account,
              "servicePwd": broker_c_pwd,
              "trdpwd": broker_trade_pwd
            }

        try:
            self.account_instance.autologin()
            raw_name = self.account_instance.account_config['userName']
            self.account_instance.fund_account = raw_name[1:] if raw_name.startswith('08') else raw_name
        except Exception,e:
            print e
            self.broker_verify_label.setText(u'登陆失败，请检查用户名密码!')
            self.broker_verify_label.setStyleSheet('color: red')
            return

        self.init_strategy_cmbobox()

        self.strategy_select()

        if self.checkBox.isChecked():
            self.dump_config()

        self.login_frame.hide()
        self.table_frame.show()

        # self.
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)
                self.uqer_username_lineEdit.setText(data.get('uqer_user'))
                self.uqer_pwd_lineEdit.setText(data.get('uqer_pwd'))
                self.broker_account_lineEdit.setText(data.get('broker_account'))
                self.broker_trade_pwd_lineEdit.setText(data.get('broker_trade_pwd'))
                self.broker_c_pwd_lineEdit.setText(data.get('broker_c_pwd'))

                if data:
                    self.checkBox.setChecked(True)
        except Exception,e:
            print e
            pass
        

    def dump_config(self):
        data = {
          "uqer_user": str(self.uqer_username_lineEdit.text()),
          "uqer_pwd": str(self.uqer_pwd_lineEdit.text()),
          "broker_account" : str(self.broker_account_lineEdit.text()),
          "broker_trade_pwd" : str(self.broker_trade_pwd_lineEdit.text()),
          "broker_c_pwd" : str(self.broker_c_pwd_lineEdit.text())
        }
        with open('config.json', 'w') as f:
            json.dump(data, f)

    @QtCore.pyqtSlot(QtGui.QWidget)
    def buy_sell_changed(self, comboBox):
        self.tableWidget.setItem(comboBox.row, 2, QTableWidgetItem(comboBox.currentText()))

    def get_order(self):
        
        orders = self.uqer_instance.get_order(self.active_strategy_id, False)

        self.tableWidget.setRowCount(len(orders))

        table = self.tableWidget

        for index, order in enumerate(orders):
            table.setItem(index, 0, QTableWidgetItem(order.get('ticker')))
            table.setItem(index, 1, QTableWidgetItem(order.get('name')))

            self.signalMapper = QtCore.QSignalMapper(self)
            self.signalMapper.mapped[QtGui.QWidget].connect(self.buy_sell_changed)
            
            temp_combobox = QtGui.QComboBox()
            temp_combobox.addItem(u'卖')
            temp_combobox.addItem(u'买')
            
            temp_combobox.currentIndexChanged.connect(self.signalMapper.map)
            temp_combobox.row = index

            table.setItem(index, 2, QTableWidgetItem(order.get('side') == u'BUY' and u'买' or u'卖'))
            if order.get('side') == u'BUY':
                temp_combobox.setCurrentIndex(1)
            else:
                temp_combobox.setCurrentIndex(0)

            table.setCellWidget(index, 2, temp_combobox)
            self.signalMapper.setMapping(temp_combobox, temp_combobox)

            table.setItem(index, 3, QTableWidgetItem(str(order.get('amount'))))
            
            place_time = dt.datetime.fromtimestamp(int(order.get('place_time'))/1000)
            table.setItem(index, 4, QTableWidgetItem(place_time.strftime('%H:%M:%S')))


    def init_strategy_cmbobox(self):
        cmbobox = self.strategy_comboBox
        self.strategy_dict = self.uqer_instance.get_strategy_list()
        for name in self.strategy_dict:
            cmbobox.addItem(name)


    def strategy_select(self):
        text = self.strategy_comboBox.currentText()
        self.active_strategy_id = self.strategy_dict[unicode(text)]
        self.get_order()


    def order_place(self):
        table = self.tableWidget

        count = table.rowCount()
        orders = []
        for x in xrange(count):

            ticker = unicode(table.item(x, 0).text())
            side   = unicode(table.item(x, 2).text())
            
            amount = unicode(table.item(x, 3).text())

            price = float(ts.get_realtime_quotes(ticker).price)
            percent = self.percent
            price = round(price*(side==u'买' and 1.+percent or 0.99-percent), 2)
            amount = int(round((int(amount)/100)*100, -2))

            orders.append((side, ticker, str(amount), str(price)))

        message = '\r\n'.join([u'%s %s: %s@%s'%order for order in orders])

        reply = QtGui.QMessageBox.question(self, u'下单确认', 
                     message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply != QtGui.QMessageBox.Yes:
            return

        for side, ticker, amount, price in orders:

            if side == u'买':
                self.account_instance.buy(ticker, price, amount)
            else:
                self.account_instance.sell(ticker, price, amount)

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    ui = uqWindow()
    ui.show()
    sys.exit(app.exec_())
