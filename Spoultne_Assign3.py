#Spencer Poultney, November 13th 2017
#'''This program reads a text file filled with tweets and the time zones they were posted from and produces a sentiment score by matching keywords with words in the tweets'''

import time
#Creating lists to organize each keyword based on its sentiment value
list1 = []
list5 = []
list7 = []
list10 = []
#Initializing Sentiment scores as integers with no value yet.
pacificSent = 0
numOfPacificTweets = 0
mountainSent = 0
numOfMountainTweets = 0
centralSent = 0
numOfCentralTweets = 0
easternSent = 0
numOfEasternTweets = 0

#Gets name of tweet file that will be read
fileName = input("Please enter the name of the file with the tweets in it: ")
#Adds .txt to the file name if you did not include it
if ".txt" not in fileName:
    fileName = fileName + ".txt"
 #Opens the tweet file to read it, prompts error if file does not exist
try:
    TWEETFILE = open(fileName, "r")
except IOError:
    print('The tweets file "{}" does not exist.'.format(fileName))
    time.sleep(1.5)
    raise IOError
    quit()

#Gets the keywords file
givenKeywordsFile = input("Please enter your keywords file: ")
if ".txt" not in givenKeywordsFile:
    givenKeywordsFile = givenKeywordsFile + ".txt"
try:
    KEYWORDSFILE = open(givenKeywordsFile, "r")
except IOError:
    print('The keywords file "{}" does not exist'.format(givenKeywordsFile))
    time.sleep(1.5)
    raise IOError
    quit()

#Runs loop for each seperate line in keywords file
for line in KEYWORDSFILE:
    #Splits keyword from its corresponding sentiment value
    keywordsEntries = line.split(",")
    #Sorts each keyword into lists based on their corresponding setiment value
    if int(keywordsEntries[1]) == 1:
        list1.append(keywordsEntries[0])
    elif int(keywordsEntries[1]) == 5:
        list5.append(keywordsEntries[0])
    elif int(keywordsEntries[1]) == 7:
        list7.append(keywordsEntries[0])
    else:
        list10.append(keywordsEntries[0])

line = TWEETFILE.readline()
#Reads each line in the tweet file until it finds a blank line (end of file)
while line != "":
    #Splits line at each space and strips brackets and commas from latitude and longitude
    tweetEntries = line.split(" ")
    tweetEntries[0] = tweetEntries[0].strip("[")
    tweetEntries[0] = tweetEntries[0].strip(",")
    tweetEntries[1] = tweetEntries[1].strip("]")
    lat = (float(tweetEntries[0]))
    lon = (float(tweetEntries[1]))
#Checks to see if the tweet is from the right range of latitude
    if 24.660845 <= lat <= 49.189787:
        #Checks to see if the tweet is from the Eastern timezone
        if -87.518395 < lon <= -67.444574:
            word1 = 0
            tempEastSent = 0
            #Causes only the tweet to be read from the line
            for i in range(5, len(tweetEntries)):
                #Gets rid of specified puncuation and symbols and puts the word in lowercase so it can match with the keywords
                tweetEntries[i] = ''.join([c for c in tweetEntries[i] if c not in ('!','#','?',"'",':',')','(',';','$','^',',','.')])
                tweetEntries[i] = tweetEntries[i].lower()
                #Checks if each word is in the specified keyword list, if so the word count is increased and the specified sentiment points are added
                if tweetEntries[i] in list1:
                    tempEastSent += 1
                    word1 += 1
                elif tweetEntries[i] in list5:
                    tempEastSent += 5
                    word1 += 1
                elif tweetEntries[i] in list7:
                    tempEastSent += 7
                    word1 += 1
                elif tweetEntries[i] in list10:
                    tempEastSent += 10
                    word1 += 1
            #Calculates sentiment value for each tweet and adds it to the total sentiment calculation for the specified timezone
            easternSent += tempEastSent/(word1 if word1 > 0 else 1)
            #If the tweet scores any sentiment points, it is added to the number of tweets from the specified timezone
            if tempEastSent > 0:
                numOfEasternTweets += 1
        #Checks to see if tweet is in the Central timezone
        elif -101.998892 <= lon <= -87.518395:
            word2 = 0
            tempCentSent = 0

            for i in range(5, len(tweetEntries)):

                tweetEntries[i] = ''.join([c for c in tweetEntries[i] if c not in ('!','#','?',"'",':',')','(',';','$','^',',','.')])
                tweetEntries[i] = tweetEntries[i].lower()
                if tweetEntries[i] in list1:
                    tempCentSent += 1
                    word2 += 1
                elif tweetEntries[i] in list5:
                    tempCentSent += 5
                    word2 += 1
                elif tweetEntries[i] in list7:
                    tempCentSent += 7
                    word2 += 1
                elif tweetEntries[i] in list10:
                    tempCentSent += 10
                    word2 += 1

            centralSent += tempCentSent/(word2 if word2 > 0 else 1)
            if tempCentSent > 0:
                numOfCentralTweets += 1
        #Checks to see if tweet is in the Mountain time zone
        elif -115.236428 <= lon <= 101.998892:
            word3 = 0
            tempMountSent = 0
            for i in range(5, len(tweetEntries)):

                tweetEntries[i] = ''.join([c for c in tweetEntries[i] if c not in ('!','#','?',"'",':',')','(',';','$','^',',','.')])
                tweetEntries[i] = tweetEntries[i].lower()
                if tweetEntries[i] in list1:
                    tempMountSent += 1
                    word3 += 1
                elif tweetEntries[i] in list5:
                    tempMountSent += 5
                    word3 += 1
                elif tweetEntries[i] in list7:
                    tempMountSent += 7
                    word3 += 1
                elif tweetEntries[i] in list10:
                    tempMountSent += 10
                    word3 += 1

            mountainSent += tempMountSent / (word3 if word3 > 0 else 1)
            if tempMountSent > 0:
                numOfMountainTweets += 1
        #Checks to see if tweet is in the Pacific timezone
        elif -125.24226 <= lon <= -115.236428:
            tempPacifSent = 0
            word4 = 0
            for i in range(5, len(tweetEntries)):

                tweetEntries[i] = ''.join([c for c in tweetEntries[i] if c not in ('!','#','?',"'",':',')','(',';','$','^',',','.')])
                tweetEntries[i] = tweetEntries[i].lower()
                if tweetEntries[i] in list1:
                    tempPacifSent += 1
                    word4 += 1
                elif tweetEntries[i] in list5:
                    tempPacifSent += 5
                    word4 += 1
                elif tweetEntries[i] in list7:
                    tempPacifSent += 7
                    word4 += 1
                elif tweetEntries[i] in list10:
                    tempPacifSent += 10
                    word4 += 1

            pacificSent += tempPacifSent / (word4 if word4 > 0 else 1)
            if tempPacifSent > 0:
                numOfPacificTweets += 1

    line = TWEETFILE.readline()
#Calculates final sentiment scores for each seperate timezone
pacificScore = pacificSent / numOfPacificTweets
mountainScore = mountainSent / numOfMountainTweets
centralScore = centralSent / numOfCentralTweets
easternScore = easternSent / numOfEasternTweets

#Prints calculation effect
print("Searching through tweets and calculating happiness scores")
import sys
sys.stdout.write(".")
sys.stdout.flush()
time.sleep(0.8)

sys.stdout.write(".")
sys.stdout.flush()
time.sleep(0.8)

sys.stdout.write(".")
sys.stdout.flush()
time.sleep(0.8)

#Prints happiness score for each timezone as well as the number of tweets with sentiment in each timezone
print("")
print("The average happiness score in the Pacific timezone is: {}".format(pacificScore))
print("The number of tweets found in that timezone is: {}".format(numOfPacificTweets))
print("The average sentiment score in the Mountain timezone is: {}".format(mountainScore))
print("The number of tweets found in that timezone is: {}".format(numOfMountainTweets))
print("The average sentiment score in the Central timezone is: {}".format(centralScore))
print("The number of tweets found in that timezone is: {}".format(numOfCentralTweets))
print("The average sentiment score in the Eastern timezone is: {}".format(easternScore))
print("The number of tweets found in that timezone is: {}".format(numOfEasternTweets))


#Creates function that produces a histogram based on the calculated sentiment values for each time zone
def graphicsDisplay(east, cent, mount, pacif):
    import happy_histogram as hp
    hp.drawSimpleHistogram(east, cent, mount, pacif)
#Calls function to run
graphicsDisplay(easternScore, centralScore, mountainScore, pacificScore)










