import numpy as np
import skfuzzy as skf
from skfuzzy import control as ctrl

#Função que recebe o método de defuzzificação e os valores de entrada das variáveis antecedentes
def fuzzy(defuzzification_methods, input_price, input_preparation_time, input_service_score):
    #Cria o conjunto universo das variáveis antecedentes e da consequente
    price = ctrl.Antecedent(np.arange(10, 301, 1), 'price')
    preparation_time = ctrl.Antecedent(np.arange(10, 120, 1), 'preparation time')
    service = ctrl.Antecedent(np.arange(0,11,1), 'service score')
    rating = ctrl.Consequent(np.arange(0,101,1), 'rating score', defuzzification_methods)

    #Maneira automatica de definir a função de pertinência da variável (Triangular)
    price.automf(number=3, names=['cheap', 'medium', 'expensive'])

    #Maneira manual de definir a função de pertinência das variáveis.
    #Para a variável preparation_time foi definido a função de pertinência trapezoidal em (skf.trampf)
    #Também é definido os termos da variável ('fast', 'medium', 'slow') ('Rápido', 'Médio', 'Lento')
    preparation_time['fast'] = skf.trapmf(preparation_time.universe, [9, 25, 35, 50])
    preparation_time['medium'] = skf.trapmf(preparation_time.universe, [35, 55, 75, 95])
    preparation_time['slow'] = skf.trapmf(preparation_time.universe, [80, 95, 105, 121])

    #O mesmo é feito para as variáveis service e rating
    service['poor'] = skf.trimf(service.universe, [-1, 2, 5])
    service['fair'] = skf.trimf(service.universe, [3, 5, 7])
    service['good'] = skf.trimf(service.universe, [5, 8, 11])

    rating['very poor'] = skf.trapmf(rating.universe, [-1, 12, 18, 30])
    rating['poor'] = skf.trapmf(rating.universe, [20, 32, 38, 50])
    rating['fair'] = skf.trapmf(rating.universe, [40, 52, 58, 70])
    rating['good'] = skf.trapmf(rating.universe, [60, 72, 78, 90])
    rating['excellent'] = skf.trapmf(rating.universe, [80, 92, 98, 101])

    #Define as regras fuzzy que criam o relacionamento entre as variáveis antecedentes e a consequente
    rules = [
        ctrl.Rule(price['cheap'] & preparation_time['fast'] & service['good'], rating['excellent']),
        ctrl.Rule(price['cheap'] & preparation_time['fast'] & service['fair'], rating['excellent']),
        ctrl.Rule(price['medium'] & preparation_time['fast'] & service['good'], rating['excellent']),
        ctrl.Rule(price['cheap'] & preparation_time['medium'] & service['good'], rating['excellent']),
        ctrl.Rule(price['cheap'] & preparation_time['fast'] & service['poor'], rating['good']),
        ctrl.Rule(price['cheap'] & preparation_time['slow'] & service['good'], rating['good']),
        ctrl.Rule(price['expensive'] & preparation_time['fast'] & service['good'], rating['good']),
        ctrl.Rule(price['cheap'] & preparation_time['medium'] & service['fair'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['fast'] & service['fair'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['medium'] & service['good'], rating['fair']),
        ctrl.Rule(price['expensive'] & preparation_time['medium'] & service['fair'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['slow'] & service['fair'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['medium'] & service['poor'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['medium'] & service['poor'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['medium'] & service['fair'], rating['fair']),
        ctrl.Rule(price['expensive'] & preparation_time['medium'] & service['good'], rating['fair']),
        ctrl.Rule(price['medium'] & preparation_time['fast'] & service['poor'], rating['fair']),
        ctrl.Rule(price['cheap'] & preparation_time['slow'] & service['fair'], rating['fair']),
        ctrl.Rule(price['expensive'] & preparation_time['slow'] & service['good'], rating['poor']),
        ctrl.Rule(price['expensive'] & preparation_time['fast'] & service['poor'], rating['poor']),
        ctrl.Rule(price['cheap'] & preparation_time['slow'] & service['poor'], rating['poor']),
        ctrl.Rule(price['expensive'] & preparation_time['slow'] & service['fair'], rating['poor']),
        ctrl.Rule(price['expensive'] & preparation_time['medium'] & service['poor'], rating['poor']),
        ctrl.Rule(price['medium'] & preparation_time['slow'] & service['poor'], rating['poor']),
        ctrl.Rule(price['expensive'] & preparation_time['slow'] & service['poor'], rating['very poor'])
    ]

    #Cria um sistema de controle com as regras definidas. Em seguida, cria uma simulação desse sistema e atribui os valores de entrada recebidos por parâmetro pela aplicação main
    sys_ctrl = ctrl.ControlSystem(rules)

    recommendation = ctrl.ControlSystemSimulation(sys_ctrl)

    recommendation.input['price'] = input_price
    recommendation.input['preparation time'] = input_preparation_time
    recommendation.input['service score'] = input_service_score

    #Calcula a saída fuzzy
    recommendation.compute()
    rating_score = recommendation.output['rating score']

    #Retorna uma tupla com o valor de saída fuzzy e os valores para criação dos gráficos na aplicação main
    return rating_score,price,preparation_time,service,recommendation