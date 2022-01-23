import random

solution_file = open('primes.txt')

solutions = solution_file.read().split()
solutions.sort()

solution_file.close()

guesses = list()

for w in solutions:
    if not w in guesses:
        guesses.append(w)
        
guesses_allowed = 6

hard_mode = True

verbose = False

secret_prime = None #for actually playing
#secret_prime = random.choice(solutions) #for testing
#secret_prime = 'hatch' #also for testing

print "This solver specifically made to solve the Primel build at:"
print "https://t.co/fmog2jz7U8"

digits_known_somewhere = []
digits_known_nowhere = []

locked_digits = [None,None,None,None,None]

digits_can_be = ['0123456789',
                  '0123456789',
                  '0123456789',
                  '0123456789',
                  '0123456789']

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

        digit_freq = dict()

        digits_we_care_about = list()

        #filter permitted guesses in hard mode
        
        if hard_mode:
            allowed_guesses = list()

            if verbose:
                mask = ''
                
                for c in locked_digits:
                    if c == None:
                        mask = mask + '-'
                    else:
                        mask = mask + c

                additional_digits = filter(lambda c:c not in mask,digits_known_somewhere)

                if mask != '-----':
                    print
                    if len(additional_digits) > 1:
                        print 'Guesses must match',mask,'and contain the digits',','.join(additional_digits)
                    elif len(additional_digits) > 0:
                        print 'Guesses must match',mask,'and contain the digit',','.join(additional_digits)
                    else:
                        print 'Guesses must match',mask
                else:
                    if len(additional_digits) > 1:
                        print
                        print 'Guesses must contain the digits',','.join(additional_digits)
                    elif len(additional_digits) > 0:
                        print
                        print 'Guesses must contain the digit',','.join(additional_digits)

            for w in guesses:
                if all(map(lambda p:p[0]==None or p[0]==p[1],zip(locked_digits,list(w)))):
                    if all(map(lambda c:c in w,digits_known_somewhere)):
                        allowed_guesses.append(w)

        else:
            allowed_guesses = guesses
                
        #determine which digits are important in our solution space

        for c in '0123456789':
            if not c in (digits_known_somewhere):
                for w in solutions:
                    if c in w and not c in digits_we_care_about:
                        digits_we_care_about.append(c)
                            
        if verbose:
            print
            print "Digits we care about:"

        for c in digits_we_care_about:
            digit_freq[c] = 0

            for w in solutions:
                if c in w:
                    digit_freq[c] += 1

            if digit_freq[c] > (len(solutions)/2):
                digit_freq[c] = len(solutions) - digit_freq[c]
            if verbose:
                print '    ',c,digit_freq[c]

        #sort guesses by those containing important digits

        best_scoring_guesses = dict()

        for w in allowed_guesses:
        #for w in solutions:
            best_scoring_guesses[w] = 0
            for c in digit_freq.keys():
                if c in w:
                    best_scoring_guesses[w] += digit_freq[c]

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

            #choose guesses with digits in positions with multiple options

            best_scoring_guesses_sorted = list()

            for guess in possible_guesses:
                score = 0
                for i in range(5):
                    if guess[i] in digits_can_be[i] and len(digits_can_be[i]) > 1:
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

            #pick guesses that might tell us exact digit positions

            best_scoring_guesses_sorted = list()

            for guess in possible_guesses:
                score = 0
                for i in range(5):
                    if len(digits_can_be[i]) > 1:
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

            #minimize duplicated digits in guesses
                
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
                    
        guess = random.choice(possible_guesses)

    guess_count += 1

    print
        
    print '    Guess #'+str(guess_count)+':', guess.upper()

    if secret_prime == None: #playing for real, wait for the user to enter guess and get response

        valid_input = False

        while not valid_input:

            result = raw_input ('Result (RYG): ')

            if len(result) == 5 and result.upper().count('R') + result.upper().count('Y') + result.upper().count('G') == 5:
                valid_input = True

    else:   #testing against known word
        result = ['R'] * 5
        matchWord = list(secret_prime)

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

        #use response to filter what digits can be in what positions
            
        for i in range(5):
            if result[i] == 'G':
                digits_can_be[i] = guess[i]
                locked_digits[i] = guess[i]
                if not guess[i] in digits_known_somewhere:
                    digits_known_somewhere.append(guess[i])

        for i in range(5):
            if result[i] == 'Y':
                digits_can_be[i] = digits_can_be[i].replace(guess[i],'')
                if not guess[i] in digits_known_somewhere:
                    digits_known_somewhere.append(guess[i])
                    
        for i in range(5):
            if result[i] == 'R':
                for j in range(5):
                    if len(digits_can_be[j]) > 1:
                        digits_can_be[j] = digits_can_be[j].replace(guess[i],'')

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
                    if not w[i] in digits_can_be[i]:
                        can_match = False
                            
                if can_match:
                    for c in digits_known_somewhere:
                        if not c in w:
                            can_match = False
                                
                if can_match:
                    remaining_solutions.append(w)

            solutions = remaining_solutions

            digits_known_nowhere = '0123456789'

            for i in range(5):
                digits_can_be[i] = ''
                for w in solutions:
                    if not w[i] in digits_can_be[i]:
                        digits_can_be[i] = digits_can_be[i] + w[i]
                    digits_known_nowhere = digits_known_nowhere.replace(w[i],'')

            done_eliminating = False

            while not done_eliminating:
                done_eliminating = True
                for c in digits_known_somewhere:
                    if sum(map(lambda w:c in w,digits_can_be)) == 1:
                        for i in range(5):
                            if c in digits_can_be[i]:
                                if len(digits_can_be[i]) > 1:
                                    if verbose:
                                        print
                                        print 'Digit',i+1,'must be',c,'by process of elimination'
                                    done_eliminating = False
                                    digits_can_be[i] = c
                                    done_sorting = False
                                
        if verbose and len(solutions) > 1:
            print

            for i in range(5):
                print 'Digit',i+1,'must be',digits_can_be[i]
                    
            print

            if len(digits_known_somewhere) > 0:
                print "The following digits must be included:",','.join(digits_known_somewhere)

            if len(digits_known_nowhere) > 0:
                print "The following digits must not be included:",','.join(digits_known_nowhere)

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

