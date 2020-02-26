We are going to design a LINE chatbot.


## Features

1.Query about the summary of news in consideration of coronavirus.
  
  The news may cover: How many new confirmed cases today or on certain date; how many cases of new recovery or what's the recovery rate right now. With data of this, pubilc will have a basic understanding of what is going on right now.
  
  Moreover, we may capture some information about how many new confirmed cases worldwide. As we know, the coronavirus spread fast in China. But it seems to start spreading increasingly in some other countries to which people who contain coronavirus travel. Gathering this information will remind coronavirus for people who want to travel to these countries. 

2.Query about FAQ(frequently asked questions) of coronavirus diseases.

When the user tries to query some FAQ, the chatbot will display a set of questions about coronavirus diseases. For example, 
How to prevent COVID-19? When the user asks the question, the chatbot will display the answer. All FAQ and corresponding answers will be collected from government or WHO pages to guarantee they are trustworthy.

If there are too many FAQ, we may allow users to type in some keywords for question searching. Say, if the user type in 'mask', the chatbot will show 'What is the function of mask?'.

To extend this feature, we may use google API as an external service for expanding answers.


3.Query about nearby patients or suspected patients. 



When you ask the chat robot about the epidemic situation nearby, the robot will reply with a labeled map. 



Check which places around you have infected people, adjust your travel route and stay away from the epidemic area. For such tools, the accuracy of data is the most important. 
Rumors and false information will not only cause panic, but also hinder the spread of the epidemic. All data without official confirmation will not be adopted. Support the data display of fine to cell and street. You can check whether there are infected people in the community you live in. 



We can use the Google map API to extend this feature. 





