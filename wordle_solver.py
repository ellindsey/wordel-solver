import random

solution_file = open('answers.txt')

solutions = solution_file.read().split()
solutions.sort()

solution_file.close()

guesses_file = open('guesses.txt')

guesses = guesses_file.read().split()
guesses.sort()

guesses_file.close()

for w in solutions:
    if not w in guesses:
        guesses.append(w)
        
guesses_allowed = 6

hard_mode = True

verbose = False

secret_word = None #for actually playing
#secret_word = random.choice(solutions) #for testing
#secret_word = 'hatch' #also for testing

print "This solver specifically made to solve the Wordle build at:"
print "https://www.powerlanguage.co.uk/wordle/"

letters_known_somewhere = []
letters_known_nowhere = []

locked_letters = [None,None,None,None,None]

letters_can_be = ['abcdefghijklmnopqrstuvwxyz',
                  'abcdefghijklmnopqrstuvwxyz',
                  'abcdefghijklmnopqrstuvwxyz',
                  'abcdefghijklmnopqrstuvwxyz',
                  'abcdefghijklmnopqrstuvwxyz']

done = False

guess_count = 0

while guess_count < guesses_allowed and not done:

    if len(solutions) < 3 or guess_count == (guesses_allowed-1):
        if verbose:
            if len(solutions) + guess_count <= guesses_allowed:
                print
                print "Skipping filter stages, solution is assured."
            else:
                print
                print "Guessing at random at this point."
                
        elif guess_count > 0:
            print
            if len(solutions) > 1:
                print len(solutions),"solutions remaining, guessing at random..."
            else:
                print len(solutions),"solution remaining, this should be the answer."

        guess = random.choice(solutions)
    else:
        if guess_count > 0:
            print
            print len(solutions),"solutions remaining, attempting to narrow it down..."

        letter_freq = dict()

        letters_we_care_about = list()

        #filter permitted guesses in hard mode
        
        if hard_mode:
            allowed_guesses = list()

            if verbose:
                mask = ''
                
                for c in locked_letters:
                    if c == None:
                        mask = mask + '-'
                    else:
                        mask = mask + c

                additional_letters = filter(lambda c:c not in mask,letters_known_somewhere)

                if mask != '-----':
                    print
                    if len(additional_letters) > 1:
                        print 'Guesses must match',mask,'and contain the letters',','.join(additional_letters)
                    elif len(additional_letters) > 0:
                        print 'Guesses must match',mask,'and contain the letter',','.join(additional_letters)
                    else:
                        print 'Guesses must match',mask
                else:
                    if len(additional_letters) > 1:
                        print
                        print 'Guesses must contain the letters',','.join(additional_letters)
                    elif len(additional_letters) > 0:
                        print
                        print 'Guesses must contain the letter',','.join(additional_letters)

            for w in guesses:
                if all(map(lambda p:p[0]==None or p[0]==p[1],zip(locked_letters,list(w)))):
                    if all(map(lambda c:c in w,letters_known_somewhere)):
                        allowed_guesses.append(w)

        else:
            allowed_guesses = guesses
                
        #determine which letters are important in our solution space

        for c in 'abcdefghijklmnopqrstuvwxyz':
            if not c in (letters_known_somewhere):
                for w in solutions:
                    if c in w and not c in letters_we_care_about:
                        letters_we_care_about.append(c)
                            
        if verbose:
            print
            print "Letters we care about:"

        for c in letters_we_care_about:
            letter_freq[c] = 0

            for w in solutions:
                if c in w:
                    letter_freq[c] += 1

            if letter_freq[c] > (len(solutions)/2):
                letter_freq[c] = len(solutions) - letter_freq[c]
            if verbose:
                print '    ',c,letter_freq[c]

        #sort guesses by those containing important letters

        best_scoring_guesses = dict()

        for w in allowed_guesses:
        #for w in solutions:
            best_scoring_guesses[w] = 0
            for c in letter_freq.keys():
                if c in w:
                    best_scoring_guesses[w] += letter_freq[c]

        best_scoring_guesses_sorted = list()

        for w in allowed_guesses:
            best_scoring_guesses_sorted.append([best_scoring_guesses[w],w])

        best_scoring_guesses_sorted.sort()
        best_scoring_guesses_sorted.reverse()

        best_score = best_scoring_guesses_sorted[0][0]

        possible_guesses = list()

        for guess in best_scoring_guesses_sorted:
            if guess[0] == best_score:
                possible_guesses.append(guess[1])

        if verbose:
            print
            print 'Possible guesses:',' '.join(possible_guesses)

        if len(possible_guesses) > 1:

            #choose guesses with letters in positions with multiple options

            best_scoring_guesses_sorted = list()

            for guess in possible_guesses:
                score = 0
                for i in range(5):
                    if guess[i] in letters_can_be[i] and len(letters_can_be[i]) > 1:
                        score = score + 1
                best_scoring_guesses_sorted.append([score,guess])

            best_scoring_guesses_sorted.sort()
            best_scoring_guesses_sorted.reverse()

            best_score = best_scoring_guesses_sorted[0][0]

            possible_guesses = list()

            for guess in best_scoring_guesses_sorted:
                if guess[0] == best_score:
                    possible_guesses.append(guess[1])

            if verbose:
                print
                print 'Filtered possible guesses:',' '.join(possible_guesses)

        if len(possible_guesses) > 1:

            #pick guesses that might tell us exact letter positions

            best_scoring_guesses_sorted = list()

            for guess in possible_guesses:
                score = 0
                for i in range(5):
                    if len(letters_can_be[i]) > 1:
                        for w in solutions:
                            if guess[i] == w[i]:
                                score = score + 1
                best_scoring_guesses_sorted.append([score,guess])

            best_scoring_guesses_sorted.sort()
            best_scoring_guesses_sorted.reverse()

            best_score = best_scoring_guesses_sorted[0][0]

            possible_guesses = list()

            for guess in best_scoring_guesses_sorted:
                if guess[0] == best_score:
                    possible_guesses.append(guess[1])

            if verbose:
                print
                print 'Further filtered possible guesses:',' '.join(possible_guesses)

        if len(possible_guesses) > 1:

            #minimize duplicated letters in guesses
                
            best_scoring_guesses_sorted = list()

            for guess in possible_guesses:
                score = 0
                for i in range(5):
                    if guess.count(guess[i]) > 1:
                        score = score + 1
                best_scoring_guesses_sorted.append([score,guess])

            best_scoring_guesses_sorted.sort()

            best_score = best_scoring_guesses_sorted[0][0]

            possible_guesses = list()

            for guess in best_scoring_guesses_sorted:
                if guess[0] == best_score:
                    possible_guesses.append(guess[1])

            if verbose:
                print
                print 'Even further filtered possible guesses:',' '.join(possible_guesses)
                    
        if len(possible_guesses) > 1:
                
            #if any of the guesses are possible solutions, pick those first
                
            filtered_possible_guesses = list()

            for guess in possible_guesses:
                if guess in solutions:
                    filtered_possible_guesses.append(guess)

            if len(filtered_possible_guesses) > 0:
                possible_guesses = filtered_possible_guesses

                if verbose:
                    print
                    print 'Possible guesses that might be solutions:',' '.join(possible_guesses)
                    
        guess = random.choice(possible_guesses)

    guess_count += 1

    print
        
    print '    Guess #'+str(guess_count)+':', guess.upper()

    if secret_word == None: #playing for real, wait for the user to enter guess and get response

        valid_input = False

        while not valid_input:

            result = raw_input ('Result (RYG): ')

            if len(result) == 5 and result.upper().count('R') + result.upper().count('Y') + result.upper().count('G') == 5:
                valid_input = True

    else:   #testing against known word
        result = ['R'] * 5
        matchWord = list(secret_word)

        for i in range(5):
            if guess[i] == matchWord[i]:
                result[i] = 'G'
                matchWord[i] = None
        
        for i in range(5):
            if result[i] != 'G' and guess[i] in matchWord:
                result[i] = 'Y'

        result = ''.join(result)

        print 'Result (RYG):',result
                
    result = result.upper()
    if result == 'GGGGG':
            
        if verbose:
            print
            print "Solution is",guess
            print guess_count,"guesses used"
        done = True
    elif guess_count < guesses_allowed:

        #use response to filter what letters can be in what positions
            
        for i in range(5):
            if result[i] == 'G':
                letters_can_be[i] = guess[i]
                locked_letters[i] = guess[i]
                if not guess[i] in letters_known_somewhere:
                    letters_known_somewhere.append(guess[i])

        for i in range(5):
            if result[i] == 'Y':
                letters_can_be[i] = letters_can_be[i].replace(guess[i],'')
                if not guess[i] in letters_known_somewhere:
                    letters_known_somewhere.append(guess[i])
                    
        for i in range(5):
            if result[i] == 'R':
                for j in range(5):
                    if len(letters_can_be[j]) > 1:
                        letters_can_be[j] = letters_can_be[j].replace(guess[i],'')

        if verbose:
            print
            for i in range(5):
                if result[i] == 'G':
                    print guess[i],'correct in this location'
                elif result[i] == 'Y':
                    print guess[i],'correct but in wrong location'
                else:
                    print guess[i],'incorrect'
                                
        done_sorting = False

        while not done_sorting:
            done_sorting = True
                            
            if verbose:
                print

                print 'Sorting...'

            remaining_solutions = list()

            for w in solutions:
                can_match = True

                for i in range(5):
                    if not w[i] in letters_can_be[i]:
                        can_match = False
                            
                if can_match:
                    for c in letters_known_somewhere:
                        if not c in w:
                            can_match = False
                                
                if can_match:
                    remaining_solutions.append(w)

            solutions = remaining_solutions

            letters_known_nowhere = 'abcdefghijklmnopqrstuvwxyz'

            for i in range(5):
                letters_can_be[i] = ''
                for w in solutions:
                    if not w[i] in letters_can_be[i]:
                        letters_can_be[i] = letters_can_be[i] + w[i]
                    letters_known_nowhere = letters_known_nowhere.replace(w[i],'')

            done_eliminating = False

            while not done_eliminating:
                done_eliminating = True
                for c in letters_known_somewhere:
                    if sum(map(lambda w:c in w,letters_can_be)) == 1:
                        for i in range(5):
                            if c in letters_can_be[i]:
                                if len(letters_can_be[i]) > 1:
                                    if verbose:
                                        print
                                        print 'Letter',i+1,'must be',c,'by process of elimination'
                                    done_eliminating = False
                                    letters_can_be[i] = c
                                    done_sorting = False
                                
        if verbose and len(solutions) > 1:
            print

            for i in range(5):
                print 'Letter',i+1,'must be',letters_can_be[i]
                    
            print

            if len(letters_known_somewhere) > 0:
                print "The following letters must be included:",','.join(letters_known_somewhere)

            if len(letters_known_nowhere) > 0:
                print "The following letters must not be included:",','.join(letters_known_nowhere)

        if len(solutions) == 0:
            print
            print "No solutions remain. Something went wrong."
            done = True
        elif verbose:
            if len(solutions) == 1:
                print
                print len(solutions),'solution remains:',solutions[0]
            elif len(solutions) < 100:
                print
                print len(solutions),'solutions remain:',' '.join(solutions)
            else:
                print
                print len(solutions),'solutions remain:',' '.join(solutions[:100]),'...'

