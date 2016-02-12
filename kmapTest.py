
numberDict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}

numbers = {}

'''
LED7 = "ABC+ABD+ABEF+ABEG+ABEH".split("+")
LED6 = "AB+ACD".split("+")
LED5 = "AB+AC+ADE+ADFGH".split("+")
LED4 = "A+BCDEFG".split("+")
LED3 = "A+BCD+BCE+BCFG+BCFH".split("+")
LED2 = "A+BC+BD+BEF".split("+")
LED1 = "A+B+CDGH+ECD+FCD".split("+")
LED0 = "A+B+C+DEF+DEG".split("+")
'''

LED7 = "AB+ACD+ACEFGH".split("+")
LED6 = "AB+AC+ADE+ADFG".split("+")
LED5 = "A+BCDEFG+BCDEFH".split("+")
LED4 = "A+BCD+BCE+BCF".split("+")
LED3 = "A+BD+BC+BEF+BEGH".split("+")
LED2 = "A+B+CDE+CDF+BEGH".split("+")
LED1 = "A+B+C+DEH+DEF+DEG".split("+")
LED0 = "A+B+C+D+E+F+G+H".split("+")

LEDs = [LED7,LED6,LED5,LED4,LED3,LED2,LED1,LED0]

for i in range(256):
    #All 256 testing numbers
    testString = "%08d"%int(bin(i)[2:])
    LEDOn = [0]*8
    for j in range(8):
        #All LEDs
        #e.g. j = LED7
        successLED = False
        for k in LEDs[j]:
            #All combinations
            #e.g. k = "ABC"
            successComb = True
            for m in k:
                #All characters in one combination
                #e.g. m = "A"
                if testString[numberDict[m]] == "0":
                    successComb = False
                    break
            if successComb == True:
                successLED = True
                break
        if successLED == True:
            LEDOn[j] = 1
    numbers[testString] = LEDOn

for i in range(256):
    testString = "%08d"%int(bin(i)[2:])
    print "%03d %s"%(i, testString),
    print numbers[testString]
