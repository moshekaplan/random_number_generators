# Some sample code that demonstrates how a Linear Congruential Generator can be
# trivially 'broken', to allow determining all future 'random' numbers.

# Thanks to http://jazzy.id.au/default/2010/09/20/cracking_random_number_generators_part_1.html
# for the guidance

class LCG:
    """Models the Linear Congruential Generator, as is used by Java
    See http://docs.oracle.com/javase/7/docs/api/java/util/Random.html#next(int)"""
    modulus = 2**48
    multiplier = 0x5DEECE66D
    increment = 11
    
    def __init__(self, seed):
        self.seed = seed
        
    def nextInt(self):
        # Moves to the next integer and returns the uppermost 32 bits
        self.seed = (LCG.multiplier * self.seed + LCG.increment) % LCG.modulus
        return self.seed >> 16

def determine_seed(first, second):
    # Takes two numbers from a LCG and determines what the seed is
    # Strategy: 'first' is the upper 32 bits of the seed. So we can brute force
    # the lower 16 bits and run it through the calculation until one matches.
    for i in xrange(2**16):
        guessed_seed = (first << 16) + i
        result = (LCG.multiplier * guessed_seed + LCG.increment) % LCG.modulus
        # Only the upper 16 bits are returned
        if result >> 16 == second:
            return result

# Now to see if it works:

# Test data generated within Java
test_data = [3296195175, 3255739001, 709468474, 3182556348, 990460223, 253667409, 1142724798, 3673392684, 3378821630, 4142241469, 3569511523, 3039852516, 1016965201, 1135659418, 1844024034, 1317380980, 730558197, 206350386, 536460063, 2966798829, 671557757, 845228205, 746716298, 979230316, 2978046035, 2672727751, 2427398599, 1199955446, 3963903996, 260280771]

# Attempt to figure out the seed from the first two random numbers       
seed = determine_seed(test_data[0], test_data[1])
# Now create a custom LCG object with the determined seed
lcg = LCG(seed)
# And check to see if we were able to generate the same sequence!
for rand in test_data[2::]:
    if lcg.nextInt() != rand:
        print "Failed"
        break
else:
    print "Passed"
