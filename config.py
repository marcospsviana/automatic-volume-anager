SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://'root':'m1cr0@t805i'@'localhost/coolbag'"
DEBUG = True

SANDBOX = True
if SANDBOX:
    __URL_PAGSEGURO = "https://ws.sandbox.pagseguro.uol.com.br/v2/"
    __SCRIPT_PAGSEGURO = "https://stc.sandbox.pagseguro.uol.com.br/pagseguro/api/v2/checkout/pagseguro.directpayment.js"
else:
    __URL_PAGSEGURO = "https://ws.pagseguro.uol.com.br/v2/"
    __SCRIPT_PAGSEGURO = "https://stc.pagseguro.uol.com.br/pagseguro/api/v2/checkout/pagseguro.directpayment.js"
