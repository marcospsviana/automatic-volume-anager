import smtplib

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("marcospaulo.silvaviana", "microat8051")
server.sendmail(
  "marcospaulo.silvaviana@gmai.com", 
  "samaralivia.tomesousa@gmai.com", 
  "this message is from python")
server.quit()
