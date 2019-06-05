from comtele_sdk.textmessage_service import TextMessageService
__api_key = '664e67a9-5fdd-4718-9cc2-3bd2a54c9520'
textmessage_service = TextMessageService(__api_key)
result = textmessage_service.send('marcos', 'teste api sms para o envio de senha', ['85986771090'])
