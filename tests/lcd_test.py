
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)

lcd.cursor_pos = (0,0)
lcd.write_string('Hello world')
lcd.cursor_pos = (0,0)
lcd.write_string('Hello worlds')



