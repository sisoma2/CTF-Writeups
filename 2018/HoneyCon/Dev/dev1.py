#!/usr/bin/env python
import sys
def logo():
	print (chr(27) + "[1;31m" + """
.------..------..------..------..------.     .------..------..------..------..------.
|L.--. ||O.--. ||G.--. ||I.--. ||N.--. |.-.  |P.--. ||A.--. ||N.--. ||E.--. ||L.--. |
| :/\: || :/\: || :/\: || (\/) || :(): ((1)) | :/\: || (\/) || :(): || (\/) || :/\: |
| (__) || :\/: || :\/: || :\/: || ()() |'-.-.| (__) || :\/: || ()() || :\/: || (__) |
| '--'L|| '--'O|| '--'G|| '--'I|| '--'N| ((1)) '--'P|| '--'A|| '--'N|| '--'E|| '--'L|
`------'`------'`------'`------'`------'  '-'`------'`------'`------'`------'`------'
""" + chr(27) + "[0m")
	print (chr(27) + "[0;33m" + " :::::::::::::::::::::::::::::::::::::::  @naivenom\n" + chr(27) + "[0m")

logo()
userInput = raw_input("Introduzca password: ")
if len(userInput) < 21:
  print("Introduzca exactamente los caracteres necesarios")
  exit()


verificaPassword = [98, 130, 162, 195, 64, 7, 134, 166, 73, 104, 0, 161, 193, 226, 162, 132, 226, 130, 131, 73, 162, 192]
user = []
for char in userInput:
  user.append( (((ord(char) << 5) | (ord(char) >> 3)) ^ 111) & 255 )

if (user== verificaPassword):
  print("Login realizado con exito!")
  print("flag-->"+userInput)
else:
  print("Error")

