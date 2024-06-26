def numToWords(number:int) -> str:
    parsed_to_string = str(number)
    STRING_LENGTH = len(parsed_to_string)
    MAX_LENGTH = 15
    IS_ZERO = 0
    NUMBER_HIERARCHY = ("", "thousand", "million", "billion", "trillion")
    REMAINING_CHARACTERS = STRING_LENGTH - (STRING_LENGTH // 3) * 3
    list_of_number = []

    def _nameTheNumbers(numbers:str):
        global ONES, TEEN_VALUES, TENTHS
        parsed_to_int = int(numbers, 10)
        LENGTH_OF_NUMBERS = len(numbers)

        def _tenthsToWords(twoDigits:str):
            if len(twoDigits) > 2:
                twoDigits = twoDigits.replace(str(IS_ZERO), "")
            first_digit = twoDigits[0]
            second_digit = twoDigits[1]
            BASE_ONES = ONES[int(second_digit, 10) -1]
            BASE_TENTHS = TENTHS[int(first_digit, 10)-1]

            if first_digit == "1":
                return BASE_ONES
            if second_digit == "0":
                return BASE_TENTHS
            return "%s %s" % (BASE_TENTHS, BASE_ONES)
        
        if LENGTH_OF_NUMBERS == 1:
            return "%s" % ONES[parsed_to_int-1]
        elif LENGTH_OF_NUMBERS == 2 or (LENGTH_OF_NUMBERS == 3 and numbers[0] == "0"):
            return _tenthsToWords(numbers)
        BASE_HUNDRED = "%s hundred" % ONES[int(numbers[0], 10) -1]

        return "%s %s" % (BASE_HUNDRED, _tenthsToWords(numbers[1:3]))
        
    # Add check for negative value
    if STRING_LENGTH > MAX_LENGTH:
        return "We don't accept number higher than hundred Trillions"
    
    if parsed_to_string.replace(str(IS_ZERO), "") == "":
        return "zero"

    x = STRING_LENGTH
    while x>IS_ZERO:
        INDEX = x-1
        REVERSE_COUNTER = (INDEX - STRING_LENGTH) *-1
        if (REVERSE_COUNTER % 3 == 0):
            list_of_number.append(parsed_to_string[INDEX:INDEX+3])
        x-=1
    if (REMAINING_CHARACTERS != IS_ZERO):
        list_of_number.append(parsed_to_string[0:REMAINING_CHARACTERS])

    if len(list_of_number) < 2:
        return "Enter a valid number"

    # Naming happens here
    result = ""
    for index in range(len(list_of_number)):
        numbers = list_of_number[index]
        hierarchy_to_add = ("%s %s" % (_nameTheNumbers(numbers), NUMBER_HIERARCHY[index])).strip()
        result = "%s %s" % (hierarchy_to_add, result)
    return result

if __name__ == "__main__":
    ONES = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    TEEN_VALUES = ("eleven", "twelve", "thirteen", "fourteen", "fiftheen", "sixteen", "seventeen", "eighteen", "nineteen")
    TENTHS = ("ten", "twenty", "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety")
    NEGATIVE_SIGN = "-"
    userInput = input("Enter a number: ")
    try:
        result = numToWords(int(userInput, 10))
        print(result)
    except ValueError:
        print("Number inputted must be >= 0" if userInput[0] == NEGATIVE_SIGN else "Not a valid number")