position = 0             # current position of the word
i = 1                    # current position of the pattern
match_state = True       # if the word matches the pattern


def search_pattern_in_word(pattern, word):
    #print(f"\n\t{word} -  the word checked against the pattern")
    global match_state
    match_state = True
    pattern = pattern.replace("*", "{0," + str(len(word)) + "}")
    pattern = pattern.replace("+", "{1," + str(len(word)) + "}")
    global position
    global i
    position = 0       # current position of the word
    i = 1             # current position of the pattern

    while i < len(pattern):
        character = pattern[i]
        occurrence = ""

        if character.isalnum():
            if position  >= len(word):
                match_state = False
                return
            elif position < len(word):
                if character != word[position]:
                    match_state = False
                    return
                elif character == word[position]:
                    #print(f"{position} position matches")
                    i += 1
                    position += 1

        elif character == ".":      # .{2}     #.{2, _} types are not implemented
            if pattern[i + 1] == "{":
                i += 2
                func_case(pattern, word, "any")
            else:
                if position + 1 >= len(word):
                    match_state = False
                    return
                else:
                    #print(f"{position} position matches {word[position]} - any")     # ..
                    i = i + 1
                    position = position + 1

        elif pattern[i: i + 5] == "[A-Z]":
            i += 6
            func_case(pattern, word, "upper")
        elif pattern[i: i + 5] == "[a-z]":
            i += 6
            func_case(pattern, word, "lower")
        elif pattern[i: i + 5] == "[0-9]":
            i += 6
            func_case(pattern, word, "digit")
        elif pattern[i: i + 8] == "[A-Za-z]":
            i += 9
            func_case(pattern, word, "alpha")
        elif pattern[i: i + 11] == "[A-Za-z0-9]":
            i += 12
            func_case(pattern, word, "alnum")
        elif character == "$":
            if position != len(word):
                match_state = False
                return
            else:
                return


def func_case(pattern, word, check):
    global match_state
    global position
    global i
    occurrence = ""  # 3,5  there should be 3 caps, and in addition there can be another two caps too
    while pattern[i] != "}":
        occurrence += pattern[i]
        i += 1
    i += 1
    start = int(occurrence.split(",")[0])
    stop = int(occurrence.split(",")[-1])

    if check == "upper":
        for pos in range(0, start):
            if position >= len(word):
                match_state = False
                return
            else:
                if word[position].isupper():
                    #print(f"{position} position matches {word[position]} - upper")
                    position += 1
                else:
                    match_state = False
                    return
        for pos in range(0, stop - start):
            if position < len(word):
                if word[position].isupper():
                    #print(f"{position} position matches too  {word[position]} - uppercase")
                    position += 1

    elif check == "any":
        if position + start >= len(word):
            match_state = False
            return
        else:
            #print(f"     {start} number of positions matches {word[position]} - any")
            position = position + start

    elif check == "lower":
        for pos in range(0, start):
            if position >= len(word):
                match_state = False
                return
            else:
                if word[position].islower():
                    #print(f"{position} position matches {word[position]} - lower")
                    position += 1
                else:
                    match_state = False
                    return
        for pos in range(0, stop - start):
            if position < len(word):
                if word[position].islower():
                    #print(f"{position} position matches too  {word[position]} - lowercase")
                    position += 1

    elif check == "digit":
        for pos in range(0, start):
            if position >= len(word):
                match_state = False
                return
            else:
                if word[position].isdigit():
                    #print(f"{position} position matches {word[position]} - digit")
                    position += 1
                else:
                    match_state = False
                    return
        for pos in range(0, stop - start):
            if position < len(word):
                if word[position].isdigit():
                    #print(f"{position} position matches too {word[position]} - digit")
                    position += 1

    elif check == "alpha":
        for pos in range(0, start):
            if position >= len(word):
                match_state = False
                return
            else:
                if word[position].isalpha():
                    #print(f"{position} position matches {word[position]} - alpha")
                    position += 1
                else:
                    match_state = False
                    return
        for pos in range(0, stop - start):
            if position < len(word):
                if word[position].isalpha():
                    #print(f"{position} position matches too {word[position]} - alpha")
                    position += 1

    elif check == "alnum":
        for pos in range(0, start):
            if position >= len(word):
                match_state = False
                return
            else:
                if word[position].isalnum():
                    #print(f"{position} position matches {word[position]} - alnum")
                    position += 1
                else:
                    match_state = False
                    return
        for pos in range(0, stop - start):
            if position < len(word):
                if word[position].isalnum():
                    #print(f"{position} position matches too {word[position]} - alnum")
                    position += 1


def search_pattern_in_paragraph(pattern, paragraph):
    if pattern[0] != '^':
        pattern = "^.*" + pattern
    if pattern[-1] != '$':
        pattern = pattern + ".*$"

    pattern = pattern.replace("?", "{0,1}")

    word_set = paragraph.split(" ")
    for word in word_set:
        search_pattern_in_word(pattern, word)
        if match_state:
            print(f"\n>>>pattern matches with the word - {word}\n")
        #else:
            #print(f"\n>>>pattern doesn't match with the word - {word}\n")


######################################################################################################################

###########################################           TEST CASES            ##########################################


#search_pattern_in_paragraph("^hello.{2}[A-Z]{3}[0-9]{2}[A-Z]{3,5}[0-9]?$", "helloppHEL55ABCD helloppHEL55ABCDd8 hello")
#search_pattern_in_paragraph("^[A-Za-z]{3}[0-9]?$", "Hel7 hel HEL7")
#search_pattern_in_paragraph("^hello.{2}[A-Z]{3}[0-9]{2}[A-Z]{3,5}[0-9]?$", "hello hello!!PPP78ABCD")
#search_pattern_in_paragraph("^hello$", "oh hello world what a nice day")
#search_pattern_in_paragraph("^[A-Z]{5, 7}$", "HELLO world this is a TEST to CHECK if PaTTERN MATCHES giVEN wordS")
#search_pattern_in_paragraph("^abc[A-Z]{5, 7}$", "abcLETTER test")
#search_pattern_in_paragraph("^..ppy$", "happy little nappy scrappy")

'''
f = open("test_01.txt", "r")
text_01 = f.read()
print(text_01)
search_pattern_in_paragraph("^r..embered$", text_01)
'''

'''
f = open("test_01.txt", "r")
text_01 = f.read()
print(text_01)
search_pattern_in_paragraph("^home$", text_01)  # this is not in the given text
'''

'''
f = open("test_01.txt", "r")
text_01 = f.read()
print(text_01)
search_pattern_in_paragraph("^[A-Za-z]{1}ings$", text_01)
'''

'''
f = open("test_01.txt", "r")
text_01 = f.read()
print(text_01)
search_pattern_in_paragraph("^..ll[a-z]{1,2}$", text_01)
'''

'''
f = open("test_02.txt", "r")
text_02 = f.read()
print(text_02)
search_pattern_in_paragraph("^[A-Z]{4,5}$", text_02)
'''

'''
f = open("test_02.txt", "r")
text_02 = f.read()
print(text_02)
search_pattern_in_paragraph("^[A-Z]{5,7}[0-9]{2,4}M00$", text_02)
'''

