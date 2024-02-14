from fuzzy import Fuzzy
import matplotlib.pyplot as plt


#Menu para escolher o método de defuzzificação
while True:
    inputDefuzzificationMethods = int(input("Escolha o Método de Defuzzificação:\n[1] Centroide\n[2] Bissetriz\n[3] Média dos máximos\n[4] Mínimo dos máximos\n[5] Máximos dos máximos\n"))
    if 0 < inputDefuzzificationMethods <= 5:
        break
    else:
        print("Você deve escolher um número entre 1 e 5!")

match inputDefuzzificationMethods:
    case 1:
        defuzzificationMethods = "centroid"
    case 2:
        defuzzificationMethods = "bisector"
    case 3:
        defuzzificationMethods = "mom"
    case 4:
        defuzzificationMethods = "som"
    case 5:
        defuzzificationMethods = "lom"


#Menu para coletar os valores de entrada das variáveis antecedentes (Preço, Tempo de Preparo e Nota de Atendimento)
inputRestaurantName = input("Qual o nome do restaurante?\n")
inputPrice = float(input("Qual a média de preços do restaurante?\n"))
inputPreparationTime = int(input("Qual é o tempo médio de preparo dos pratos?\n"))
inputServiceScore = float(input("Qual a nota do atendimento?\n"))


#Chama da função fuzzy da biblioteca que fuzzy que criamos e passa por parâmetro o método de defuzzificação e os valores das variáveis antecedentes
ratingScore = Fuzzy(defuzzificationMethods, inputPrice, inputPreparationTime, inputServiceScore)


#Imprime a nota de recomendação obtida
print("A nota de recomendação do " + inputRestaurantName + ", em uma escala de 0 a 100, é : " + str(round(ratingScore[0])))


#Imprime o gráfico mostrando o grau de pertinência das variáveis Preço, Tempo de Preparo e Nota de Atendimento
ratingScore[1].view(sim=ratingScore[4])
ratingScore[2].view(sim=ratingScore[4])
ratingScore[3].view(sim=ratingScore[4])

plt.show()
