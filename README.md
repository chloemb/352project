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
We coded this game using Python 3.7 with the pyaudio, aubio, and pygame packages. Pyaudio allows us to take input from a microphone as a stream, while aubio allows us to detect the pitch in real time. Pygame is a Python library for making games in Python. We picked these packages because they work together in a Python environment, allowing us to integrate them seamlessly with one another.
</p>
<h4> STATISTICAL ANALYSIS</h4>
<p>
In order to analyze the performance of our pitch detection through aubio, we used the dataset of VocalSet, which contains actual singing in a variety of methods by several different singers. We used this dataset for the diversity of testing that it allowed us to choose from, and ultimately decided on using both male and female voices for straight A scales. We used the straight a scales for male_1, male_2, female_1, and female_2, and took 10 samples of each voice, recording with the same method each time for consistency. Overall, we found that the pitch processing worked fairly well, as each singer's mean and mode tracks ended up maintaining the same rough shape of their component recordings. Though the mean and mode of the tracks are both fairly accurate, we found the mode to follow the shape of a scale better than the mean, and have based our assesment mainly on those. 
</p>
<p>
In terms of possible errors for data collection, one may be the the technique used to get this testing data. The testing data was collected manually, meaning that the speaker quality will impact the pitch detection based on well how the microphone can intake the range and quality of sound output. Additionally, because the process was done manually, there is some error based on holding up the microphone directly to the speaker as it was not in exactly the same location each time. Overall these problems could be solved through automated testing, though these tests were manual because we wanted to test in the same way that we were taking in data, through the speakers, and automated testing would've had to have been directly through file stream inputs. 
</p>
![Male_One_All_Takes](/Images/Male_One_All_Takes.png)
<p>
 Figure 1. Here is an overlay of all 10 testing takes of the Male One straight scale track from VocalSet, showing a high degree of similarity across each recording with some variation confined to areas of large spikes. 
 </p>
