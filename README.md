<div style="text-align: center"><h1>352 Project</h1></div>
<div style="text-align: center"><h3>Final project for EECS 352
  <br>
  Taught by Bryan Pardo at Northwestern University</h3></div>
<div style="text-align: center"><h4>
  Chloe Brown | chloebrown2020@u.northwestern.edu
  <br>
  Katrina Parekh | katrinaparekh2020@u.northwestern.edu
  <br>
  Jack Warshaw | jackwarshaw2020@u.northwestern.edu
</h4>
</div>
<br>
<br>
<h4>PROJECT SUMMARY:</h4>
<p>
Our goal for this project was to create a simple runner game wherein the player can control their avatar with the pitch of their voice. We aimed above all to create a fun, responsive, challenging game. The nature of the game also means that those with motor disadvantages (ie, shaky hands or poor coordination) can still play.
</p>
<p>
In order to make the game work for all human vocal ranges (and even some instrument ones), the game calibrates before each play instance by asking the user to make a low pitch and then a high pitch. Then, as the game plays, it takes input from a microphone, detects the pitch of the input in real time, and translates that pitch to a position on the game screen relative to the calibrated low and high pitches. The player's avatar follows that position, allowing real-time input based on pitch.
</p>
<p>
We coded this game using Python 3.7 with the pyaudio, aubio, and pygame packages. Pyaudio allows us to take input from a microphone as a stream while aubio allows us to detect the pitch in real time. Pygame is a Python library for making games in Python. We picked these packages because they let us work all in Python.
</p>
