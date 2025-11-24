# DBOG-Tools

Download Latest Version (Version 1.1.0): [GitHub Release](https://github.com/AmmonNH3/DBOG-Tools/releases/tag/v1.1.0)

This tool provides a macro for the DBOG Gravity Chamber. It uses [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
to read on-screen prompts and automatically execute the correct inputs.

⚠️ Important

If the program does not run correctly for some reason, install TesseractOCR from: [Tesseract OCR Download](https://github.com/UB-Mannheim/tesseract/wiki)

Make sure it's installed at:

C:\Program Files\Tesseract-OCR\tesseract.exe

The code is fully open source. You may modify or improve it as you wish. Credits would be appreciated.

Windows may flag this program as malicious. I don't really know why, but this is not the case.

# UPDATE

Added a new option to switch between OLD and NEW OCRs, OLD code works perfectly with the GC's red floor, meanwhile the NEW code sometimes works with the HTC white background and stuff, only use it if you don't have any training partners, the new ocr is kinda weird.

YT Tutorial: https://www.youtube.com/watch?v=e2ePOKaFhwo

<img width="230" height="132" alt="image" src="https://github.com/user-attachments/assets/e37281a1-b040-41b0-a508-36e84744b225" />

Just select the OCR mode before starting the macro. With the OLD code always remember to look at the ground where the red floor is.

Like this:

<img width="1920" height="920" alt="image" src="https://github.com/user-attachments/assets/d2dd368f-ed52-4b81-944d-dffdc48faee2" />

Remember, this is with the OLD OCR code.

-------------------------------------------------------------------------------

-------- INTRODUCTION --------

Welcome to the DBOG gravity macro repo.
I made this because I really got tired of the dumb Gravity Chamber training system, it's hard to get all stats with only 40 minutes on the clock.
The macro uses Tesseract OCR to read prompts displayed on screen and perform the corresponding WASD inputs automatically, I hope this helps you unlock your full potential.

-------- HOW DO I USE IT --------

Watch the [tutorial](https://www.youtube.com/watch?v=EABeeFTEpxc).

-------- TROUBLESHOOTING --------

- The macro does not recognize a specific letter (e.g., A).

     Select a clearer area for OCR recognition. Tesseract works best when the prompt box is compact, like this:

<img width="587" height="83" alt="image" src="https://github.com/user-attachments/assets/70e260c1-03c0-431c-86b4-aac7d387a415" />

Instead of doing this, which may cause the OCR to go nuts:

<img width="682" height="128" alt="image" src="https://github.com/user-attachments/assets/cdf37b4a-964a-4b7f-b738-8f07f9232953" />


- The macro types too quickly, causing prompts to overlap or misfire.

     Use the built-in presets (Health, Agility, Ki Control, etc.). If that's too fast for you (due to lag or lower-end PC), adjust the Reading Speed slider to your liking.

  <img width="197" height="61" alt="image" src="https://github.com/user-attachments/assets/eeefff90-9708-49eb-9e7f-60daafa8955f" />


- The macro does not work in the HTC, or works inconsistently.

     It may happen when the WASD prompt box has a white background.

<img width="546" height="157" alt="image" src="https://github.com/user-attachments/assets/b36a565e-19f7-4ce8-8def-5731ba7929ec" />

Try using other colored backgrounds in the HTC, like these ones:

<img width="512" height="97" alt="image" src="https://github.com/user-attachments/assets/31a0f91b-f95a-484a-8463-afea8501cad6" />
<img width="511" height="92" alt="image" src="https://github.com/user-attachments/assets/519e80c4-39e7-4c5f-b816-39a0d2fbbec9" />
<img width="510" height="93" alt="image" src="https://github.com/user-attachments/assets/ea9d0e70-4cfa-43d7-b1f5-83dc4ecb36a0" />

- The macro displays "Bot Stopped (Error or manually)" when pressing F4/Start Macro.

     It may be because you didn't run the app as an administrator (the keyboard python library sometimes requires admin perms, idk why)
     Or you don't have Tesseract installed, you can get it [here](https://github.com/UB-Mannheim/tesseract/wiki). (Shouldn't be an issue because the exe already has tesseract incorporated onto it, still, just in case)


-------- CREDITS --------

 - AmmonNH3, main code
 - spxeedy, thanks a lot for helping me fix the white bg bug.

