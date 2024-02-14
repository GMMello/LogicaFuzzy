from fuzzy import fuzzy
import matplotlib.pyplot as plt


#Menu para escolher o método de defuzzificação
while True:
    input_defuzzification_methods = int(input("Escolha o Método de Defuzzificação:\n[1] Centroide\n[2] Bissetriz\n[3] Média dos máximos\n[4] Mínimo dos máximos\n[5] Máximos dos máximos\n"))
    if 0 < input_defuzzification_methods <= 5:
        break
    else:
        print("Você deve escolher um número entre 1 e 5!")

match input_defuzzification_methods:
    case 1:
        defuzzification_methods = "centroid"
    case 2:
        defuzzification_methods = "bisector"
    case 3:
        defuzzification_methods = "mom"
    case 4:
        defuzzification_methods = "som"
    case 5:
        defuzzification_methods = "lom"


#Menu para coletar os valores de entrada das variáveis antecedentes (Preço, Tempo de Preparo e Nota de Atendimento)
input_restaurant_name = input("Qual o nome do restaurante?\n")
input_price = float(input("Qual a média de preços do restaurante?\n"))
input_preparation_time = int(input("Qual é o tempo médio de preparo dos pratos?\n"))
input_service_score = float(input("Qual a nota do atendimento?\n"))


#Chama da função fuzzy da biblioteca que fuzzy que criamos e passa por parâmetro o método de defuzzificação e os valores das variáveis antecedentes
rating_score = Fuzzy(defuzzification_methods, input_price, input_preparation_time, input_service_score)


#Imprime a nota de recomendação obtida
print("A nota de recomendação do " + input_restaurant_name + ", em uma escala de 0 a 100, é : " + str(round(rating_score[0])))


#Imprime o gráfico mostrando o grau de pertinência das variáveis Preço, Tempo de Preparo e Nota de Atendimento
rating_score[1].view(sim=rating_score[4])
rating_score[2].view(sim=rating_score[4])
rating_score[3].view(sim=rating_score[4])

plt.show()
