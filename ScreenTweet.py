import sys
import tweepy
import nltk
import RPi.GPIO as GPIO
import time
from RPLCD import CharLCD

lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=24, pins_data=[22,18,16,12])

def write_to_lcd(lcd, framebuffer, num_cols):
	lcd.home()
	for row in framebuffer:
		lcd.write_string(row.ljust(num_cols)[:num_cols])
		lcd.write_string('\r\n')

def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.2):
	padding = ' ' * num_cols 
	s = padding + string + padding  
	for i in range(len(s) - num_cols + 1):  
		framebuffer[row] = s[i:i+num_cols]  
		write_to_lcd(lcd, framebuffer, num_cols)  
		time.sleep(delay) 

def main():
    consumer_key = sys.argv[1]
    consumer_secret = sys.argv[2]
    access_token = sys.argv[3]
    access_token_secret = sys.argv[4]
    subject = sys.argv[5]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.search(subject, locale="en", count=100)

    while True:
        for tweet in public_tweets:
            if "RT" not in str(tweet):
	      framebuffer = [
	          '#Trumptweets', 
                  '',
	      ]
	      print str(tweet.text.encode("utf-8"))
              long_string = str(tweet.text.encode("utf-8"))
	      
	      loop_string(long_string, lcd, framebuffer, 1, 16)

 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd.write_string("Goodbye!")
    GPIO.cleanup()
