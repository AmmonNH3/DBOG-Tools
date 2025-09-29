# DBOG-Tools
Macro for the DBOG gravity chamber.
It uses Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

------------  IMPORTANT -----------------
INSTALL TESSERACT OCR ON YOUR PC BEFORE USING, THE MACRO DOESN'T WORK WITHOUT IT -> https://github.com/UB-Mannheim/tesseract/wiki

Make sure it's installed on C:\Program Files\Tesseract-OCR\tesseract.exe
-------------------------------------------------------------------------------

-------- INTRODUCTION --------

Welcome to the DBOG gravity macro repo.
I made this because I really got tired of the dumb Gravity Chamber training system, it's hard to get all stats with only 40 minutes.
It uses Tesseract OCR, which basically reads the prompt on screen and plays the corresponding inputs.
I hope this helps you unlocking your max potential.

-------- HOW DO I USE IT --------
Watch the tutorial:

-------- TROUBLESHOOTING --------

- The macro doesn't recognize (X) letter

     Select a better area for the macro to read.

- The macro is typing too fast and the other prompts get affected

     Use the Health - Agility - Ki Control,etc presets I added, if that's too fast for you, just modify the Reading Speed slider to your liking.

- The macro is not working on the HTC, or it barely works

     It may happen when the WASD prompt box has a white BG, like this:

<img width="546" height="157" alt="image" src="https://github.com/user-attachments/assets/b36a565e-19f7-4ce8-8def-5731ba7929ec" />

Try using other colored backgrounds in the HTC, like these ones:

<img width="512" height="97" alt="image" src="https://github.com/user-attachments/assets/31a0f91b-f95a-484a-8463-afea8501cad6" />
<img width="511" height="92" alt="image" src="https://github.com/user-attachments/assets/519e80c4-39e7-4c5f-b816-39a0d2fbbec9" />
<img width="510" height="93" alt="image" src="https://github.com/user-attachments/assets/ea9d0e70-4cfa-43d7-b1f5-83dc4ecb36a0" />

- The macro says "Bot Stopped (Error or manually)" when I press F4/Start Macro

     It may be because you didn't open the app as administrator (the keyboard python library sometimes requires admin perms, idk why)
     Or you don't have Tesseract installed, you can get it here: https://github.com/UB-Mannheim/tesseract/wiki (that's the thing that reads the text on ur screen)


-------- CREDITS --------

 - AmmonNH3, main code
 - spxeedy, thanks a lot for helping me fix the white bg bug.

