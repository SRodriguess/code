# Three variations of shift search algorithms using bit paralellism

class Shift:

    # -- MIN SHIFT AND ---
    def min_shift_and(self, p, t):
        m = len(p)
        B = {}                              # char -> bitmask table
        p = p.upper(); t = t.upper()
        match_positions = []
        for i in range(m):
            B[p[i]] = (B.get(p[i], 0) | (1 << i))

        hit = 1 << (m - 1)
        a = 0                               # accumulator
        for i in range(len(t)):
            a = ((a << 1) | 1) & B.get(t[i], 0)
            if a & hit:
                # print("found at %d" % (i - m + 1))
                match_positions.append((i - m + 1))
        
        return match_positions


    # -- SHIFT OR ---
    def neg(self, x):
        return 0b11111111111111111111111111111111 - x
    
    def shift_or(self, pattern, sequence):
        """Same as shift_and, but invert masks and use OR to
        avoid an | in the inner loop."""
        m = len(pattern)
        n = len(sequence)
        pattern = pattern.upper(); sequence = sequence.upper()
        neg0 = self.neg(0)
        match_positions = []

        # build table
        B = {}                              # char -> bitmask table
        for i in range(m):
            B[pattern[i]] = (B.get(pattern[i], 0) | (1 << i))

        B = {k: self.neg(B[k]) for k in B}

        # complement all bit masks in B, complement bit mask
        a = neg0

        hit = (1 << (m - 1))

        for i in range(len(sequence)):
            a = (((a << 1) & neg0) | B.get(sequence[i], neg0))
            if a & hit == 0:
                # print("found at %d" % (i - m + 1))
                match_positions.append((i - m + 1))

        return match_positions


    # -- SHIFT AND ---
    def shift_and(self, pattern, sequence):
        m = len(pattern)
        n = len(sequence)
        pattern = pattern.upper(); sequence = sequence.upper()
        match_positions = []
    
        B = {}                              # char -> bitmask table
        for i in range(m):
            B[pattern[i]] = (B.get(pattern[i], 0) | (1 << i))
        
        # search
        D = 0
        for i in range(n):
            D = ((D << 1) | 1) & (B.get(sequence[i], 0))
            if D & (1 << (m - 1)):
                # print("Found at %d" % (i - m + 1))
                match_positions.append((i - m + 1))
        
        return match_positions


# tests
if __name__ == '__main__':

    inst_shift = Shift()

    posicoes = inst_shift.shift_and("ABACATE", "sssMEU ABACATE Ssss ABACAte sss ABACATE sss")
    print(posicoes)
    posicoes = inst_shift.shift_or("sssMEU", "sssMEU ABACATE Ssss sssMEUABACAte sss ABsssMEUsssMEUsssMEUACATE sss")
    print(posicoes)
    posicoes = inst_shift.min_shift_and("Ssss", "sssMEU ABSsssACATE Ssss ABACAte ssSssss ABACATE sss")
    print(posicoes)