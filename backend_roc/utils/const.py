MSG_Email_Already = "This email already registered"
MSG_Mobile_Already = "This mobile number already registered"

OTP_API_URL = 'https://enterprise.cloudsvas.com/api/sendsms?route=Transactional&senderid=STARFD&message=<msg>&mobilenumber=<mobile_no>&userid=starfoods&password=starfoods@123'

OTP_TEMPLATE = "Your OTP is <OTP>"
ORDER_CANCEL = "sorry ! your order <order_id> have been canceled in case of online payment your amount will be refund in 2-3 working days "
ORDER_READY = "Your order is ready is Ready for pickup"
ORDER_OUT_FOR_DELIVERY = "Your order is out for delivery"

OWNER_EMAIL = "mayank.shukla@starfood.co.in"
# userid = starfoods
# pass = starfoods@123

POS_TEX_GET = 'http://213.136.68.196:809/api/values/Getrecord/9995'
POS_CAT_GET = 'http://213.136.68.196:809/api/values/Getrecord/9994'
POS_CREATE = 'http://213.136.68.196:819/api/MenuMappings'

FRANCHISEES_TEMPLATE = "you have request for franchisees \n <name> "

# AUTH_EMAIL = 'data@genrosys.com'
# AUTH_EMAIL_PWD = 'Qwert2ab@544321'
# AUTH_DOMAIN = 'mail.aativamail.com'

AUTH_EMAIL = 'contact@starfood.co.in'
AUTH_EMAIL_PWD = 'Meatfun@123'
AUTH_DOMAIN = 'smtp.zoho.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

OTP_NOT_MATCH_MSG = 'OTP does not matched'
USER_NOT_EXIST_MSG = 'User does not exist'
FAILED_OTP_SEND = 'Failed to send OTP'
OTP_EXPIRED_MSG = 'Your OTP has been expired'


OTP_EMAIL_TEMPLATE = "Your OTP is <OTP>"
OTP_EMAIL_SUBJECT = "ROC OTP"

LOGOUT_MSG = "successfully logout"

FRANCHISSES_SEND_FAILED = "message send failed"

POS_MACHINE_API = 'http://213.136.68.196:819/api/menuonlineorders'