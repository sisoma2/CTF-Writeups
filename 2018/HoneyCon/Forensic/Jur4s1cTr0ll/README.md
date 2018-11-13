# CTF honeycon 2018 - Jur4s1cTr0ll

First we load the file into a program that allows you to investigate disk images. In this case we will use Autopsy.
Searching the filesystem we find an executable named "Honeycon.exe" in the desktop of the user Th3_Tr0ll.

!['EXE Check'](Jur4s1cTr0ll/img/Autopsy.JPG)

Next step is to analyze this binary. We load it in PEStudio and we found that's a .NET Binary so we open it with dnSpy. 
The binary just checks the input from a TextBox and if it's correct it shows a MessageBox and changes the BackgroundImage.

!['EXE Check'](Jur4s1cTr0ll/img/Check.JPG)

We introduce the correct string "CORREQOAHHHPURASOCORAOOMDSJPT" an we push the button and the flag appears:

!['Flag'](Jur4s1cTr0ll/img/Flag.jpg)
