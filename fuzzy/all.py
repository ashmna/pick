import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions


courier_speed = ctrl.Antecedent(np.arange(0, 120, 1), 'courier_speed')
restaurant_cooking_speed = ctrl.Antecedent(np.arange(0, 60, 1), 'restaurant_cooking_speed')
courier_restaurant_distance = ctrl.Antecedent(np.arange(0, 100, 1), 'courier_restaurant_distance')
customer_restaurant_distance = ctrl.Antecedent(np.arange(0, 100, 1), 'customer_restaurant_distance')

choose_probability = ctrl.Antecedent(np.arange(0, 100, 1), 'choose_probability')


courier_speed['all'] = fuzz.trimf(courier_speed.universe, [0, 0, 120])
restaurant_cooking_speed['all'] = fuzz.trimf(restaurant_cooking_speed.universe, [0, 0, 60])
courier_restaurant_distance['all'] = fuzz.trimf(courier_restaurant_distance.universe, [0, 0, 100])
customer_restaurant_distance['all'] = fuzz.trimf(customer_restaurant_distance.universe, [0, 0, 100])

choose_probability['all'] = fuzz.trimf(choose_probability.universe, [0, 0, 100])

# courier_speed.view()

# courier_speed.automf(3)
# restaurant_cooking_speed.automf(3)
# courier_restaurant_distance.automf(3)
# customer_restaurant_distance.automf(3)

# choose_probability.automf(3)

# rule1 = ctrl.Rule(
#     courier_speed['all'] & restaurant_cooking_speed['all'],
#     choose_probability['all']
# )
# rule2 = ctrl.Rule(
#     courier_speed['all'] & courier_restaurant_distance['all'] & customer_restaurant_distance['all'],
#     choose_probability['all']
# )
rule3 = ctrl.Rule(
    courier_speed['all'] & courier_restaurant_distance['all'] & customer_restaurant_distance['all'],
    choose_probability['all']
)

# rule1.view()
# rule2.view()
# rule3.view()

probability_ctrl = ctrl.ControlSystem([rule3])
probability = ctrl.ControlSystemSimulation(probability_ctrl)

probability.input['courier_speed'] = 30.
# probability.input['restaurant_cooking_speed'] = 30.
probability.input['courier_restaurant_distance'] = 20.
probability.input['customer_restaurant_distance'] = 20.
# probability.input['choose_probability'] = 0.

probability.compute()

print probability.output['choose_probability']
choose_probability.view(sim=probability)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
# tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
# tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
# tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])
r = 5
