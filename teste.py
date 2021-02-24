from search_shifts import Shift

inst_shift = Shift()

posicoes = inst_shift.shift_and("ABACATE", "sssMEU ABACATE Ssss ABACAte sss ABACATE sss")
print(posicoes)
posicoes = inst_shift.shift_or("sssMEU", "sssMEU ABACATE Ssss sssMEUABACAte sss ABsssMEUsssMEUsssMEUACATE sss")
print(posicoes)
posicoes = inst_shift.min_shift_and("Ssss", "sssMEU ABSsssACATE Ssss ABACAte ssSssss ABACATE sss")
print(posicoes)