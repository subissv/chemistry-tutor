from chempy import *
import chempy
from chempy.chemistry import Reaction
from chempy.chemistry import balance_stoichiometry
from chempy import Substance
from drafter import *
from dataclasses import dataclass 
from bakery import assert_equal

set_website_title("Chemistry Tutor")
set_site_information(
    author = "Subiksha Srinivasan Vidya",
    description = "Help solve simple chemistry problems",
    sources = "Thanks to the Drafter docs",
    planning = [],
    links = []
)

hide_debug_information()
set_website_framed(False)


#Second Dataclass
@dataclass
class Calculation:
    """
    Store the inputs and calculated results of a stoichiometry problem
"""
    reactants: str
    products: str
    reactant_mass: float
    actual_yield: float
    theoretical_yield: float
    percent_yield: float


#State Dataclass
@dataclass
class State:
    """
    Store the current website information, user inputs, and calculation histroy 
    """
    reactants: str
    products: str
    reactant_mass: float
    actual_product_mass: float
    result: str
    calculations: list[Calculation] = None

    def __post_init__(self):
        """
        Create an empty calculation history if one is not provided
        """

        if self.calculations is None:
            self.calculations = []

#supported chemical formulas
supported_formulas = {
    "H2O": Substance.from_formula("H2O"),
    "CO2": Substance.from_formula("CO2"),
    "C5H12": Substance.from_formula("C5H12"),
    "O2": Substance.from_formula("O2"),
    "NaCl": Substance.from_formula("NaCl"),
    "HCl": Substance.from_formula("HCl"),
    "NaOH": Substance.from_formula("NaOH"),
    "CH4": Substance.from_formula("CH4"),
    "C2H6": Substance.from_formula("C2H6"),
    "C3H8": Substance.from_formula("C3H8"),
    "C4H10": Substance.from_formula("C4H10"),
    "C6H14": Substance.from_formula("C6H14"),
    "C7H16": Substance.from_formula("C7H16"),
    "C8H18": Substance.from_formula("C8H18"),
    "C9H20": Substance.from_formula("C9H20"),
    "C10H22": Substance.from_formula("C10H22"),
    "H2" : Substance.from_formula("H2")
}

#function to process chemical substances
def parse_substances(equation: str):
    """
    Separate chemical formulas and their coefficients from and equation
    """

    substances = equation.split('+')
    parsed_substances = []


    for substance in substances:
        parts = substance.strip().split()

        if len(parts) == 1:
            coefficient = 1
            formula = parts[0]

        elif len(parts) == 2:
            if parts[0].isdigit():
                coefficient = int(parts[0])
                formula = parts[1]

            else:
                return None

        else:
            return None

        if coefficient <= 0:
            return None

        if formula not in supported_formulas:
            return None

        parsed_substances.append((formula, coefficient))

    return parsed_substances

def calculate_theoretical_yield(reactant_formula, product_formula, reactant_coefficient, product_coefficient, reactant_mass):
    """
    Calculate theoertical yield using the mole ratio
    """
    reactant_molar_mass = supported_formulas[reactant_formula].mass
    product_molar_mass = supported_formulas[product_formula].mass

    reactant_moles = reactant_mass / reactant_molar_mass

    product_moles = reactant_moles * (
        product_coefficient / reactant_coefficient
    )

    theoretical_yield = product_moles * product_molar_mass

    return theoretical_yield


# Function to calculate percent yield
def calculate_percent_yield(actual_yield, theoretical_yield):
    """
    Calculate the percent yield of a chemical reaction.
    """

    if theoretical_yield <= 0:
        return None

    percent_yield = (actual_yield / theoretical_yield) * 100

    return percent_yield


# UNIT TESTS

def test_parse_substances():
    """Test whether chemical formulas and coefficients are extracted correctly."""

    assert_equal(parse_substances("H2"), [("H2", 1)])

    assert_equal(parse_substances("2 H2 + 1 O2"),
                 [("H2", 2), ("O2", 1)])

    assert_equal(parse_substances("2 H2O"),
                 [("H2O", 2)])

    assert_equal(parse_substances("3 CH4 + 2 O2"),
                 [("CH4", 3), ("O2", 2)])

    assert_equal(parse_substances("2 XYZ"), None)


def test_calculate_theoretical_yield():
    """Test whether theoretical yield is calculated correctly."""

    result = calculate_theoretical_yield(
        "H2", "H2O", 2, 2, 4.032
    )

    assert_equal(round(result, 2), 36.03)

    result = calculate_theoretical_yield(
        "H2", "H2O", 2, 2, 10
    )

    assert_equal(round(result, 2), 89.36)


def test_calculate_percent_yield():
    """Test whether percent yield is calculated correctly."""

    assert_equal(calculate_percent_yield(8, 10), 80.0)

    assert_equal(calculate_percent_yield(5, 10), 50.0)

    assert_equal(calculate_percent_yield(0, 10), 0.0)

    assert_equal(calculate_percent_yield(5, 0), None)



@route
def index(state: State) -> Page:
    """
    Display the home page and navigation options for the Chemistry Tutor

    Arg: 
        state (State)

    Return: 
        Page
    """
    return Page(state, [

        Header("Chemistry Tutor"),
        "Learn how to solve chemistry problems step by step!",

        Button("Practice Stoichiometry", "stoichiometry"),

        Button("Intro to Titration", "titration"),

        Button("Practice Titration", "titration_sim"),

        Button("Balance Acid-Base Reactions", "balance_acid_base"),

        Button("Explore Titration Curves", "titration_curve")
    ]

    )

#titration introduction page
@route
def titration(state: State) -> Page:
    """
    Display the titration introduce page
    """
    return Page(state,[

        Header("Intro to Acid-Base Titration"),
        Button("Return Home", "index")
    ])



#titration simulation page
@route
def titration_sim(state: State) -> Page:
    """
    Display the acid-base titration and simulation
    """

    return Page(state,[

        Header("Acid-Base Titration Simulation"),
        Button("Return Home", "index")
    ])


@route
def titration_curve(state: State) -> Page:
    """
    Display the titration curve from the titration simulation
    """

    return Page(state,[
        Header("Titration Curves"),
        Button("Return Home", "index")

    ])

@route
def balance_acid_base(state: State) -> Page:

    """
    Displays a calculator to help balance acid-base reactions
    """

    return Page(state,[
        Header("Balancing Acid-Base Reactions"),
        Button("Return Home", "index")

    ])


#Stoichiometry Page
@route
def stoichiometry(state: State) -> Page:
    """
    Displays the stoichiometry calculator 
    """

    previous_calculations = ""

    for calculation in state.calculations:
        previous_calculations += (
            "Reactions:" + calculation.reactants + 
            "->" + calculation.products +
            "| Theoretical yield:" +
            str(round(calculation.theoretical_yield, 2)) + "g\n"

        )

    return Page(state, [ 
        Header("Stoichiometry Calculator"),
        "Calculate the theoretical yield and percent yield of a chemical reaction.",

        Header("Step 1: Enter Your Reactants"),

        "Enter your reactants separated by + signs.",
        "Example: 2 C5H12 + 1 O2",

        TextBox("reactants", state.reactants),

        Header("Step 2: Enter Your Products"),

        "Enter your products separated by + signs.",
        "Example: 1 CO2 + 1 H2O",

        TextBox("products", state.products),

        Header("Step 3: Enter the Totla mass of Your Reactants"),

        "Enter the mass of your reactants in grams:",

        TextBox("reactant_mass", state.reactant_mass),

        Header("Step 4: Enter the Actual Yield of Your Products"),

        "How many grams of product did you actually produce?",

        TextBox("actual_product_mass", state.actual_product_mass),

        "Note: This calculator assumes the reactants are present in the exact proportions shown in the balanced equation.",

        Button("Calculate", "calculate_stoichiometry"),

        Header("Previous Calculations"),
        previous_calculations,

        Button("Return Home", "index")




    ] )


#calculate stoichiometry
@route
def calculate_stoichiometry(state: State, reactants: str, products: str, reactant_mass: float, actual_product_mass: float) -> Page:

    """ 
    Helps calculate the theoertical yield of the given reactants

    Args:
        state: State
        reactants (str): the chemical formulas for the reactants, including the coefficents and + signs
        products (str): the chemical formulas for the products, including the coefficients and + signs
        reactant_mass(float): the starting reactant mass in grams
        actual_product_mass(float): how much product is created

    Return:
        Page: displays the results of the inputs


    """
    

    #check numerical inputs

    if reactant_mass <= 0:
        return Page(state, [ 
            Header("Invalid Input"),
            "Reactant mass must be greater than zero.",
            Button("Try Again", "stoichiometry"),

        ])

    if actual_product_mass < 0:
        return Page(state, [ 
            Header("Invalid Input"),
            "Actual product mass cannot be negative.",
            Button("Try Again", "stoichiometry"),

        ])

    #Check Reactant & product formulas

    reactant_info = parse_substances(reactants)
    product_info = parse_substances(products)

    if reactant_info == None:
        return Page(state, [ 
            Header("Invalid Reactant"),
            "Please enter a supported chemical formula and positive coefficient.",
            Button("Try Again", "stoichiometry"),

        ])

    if product_info == None:
        return Page(state, [ 
            Header("Invalid Product"),
            "Please enter a supported chemical formula and positive coefficient.",
            Button("Try Again", "stoichiometry"),

        ])

    reactant_formula = reactant_info[0][0]
    reactant_coefficient = reactant_info[0][1]
    
    product_formula = product_info[0][0]
    product_coefficient = product_info[0][1]
    
    #get molar masses using chempy
    reactant_molar_mass = supported_formulas[reactant_formula].mass
    product_molar_mass = supported_formulas[product_formula].mass
    
    #convert grams of reactant to moles
    reactant_moles = reactant_mass / reactant_molar_mass

    product_moles = reactant_moles * (product_coefficient / reactant_coefficient)

    #calculate theoretical yield in grams
    theoretical_yield = product_moles * product_molar_mass

    #check theoretical yield to avoid division by zero

    if theoretical_yield <= 0:
        return Page(state, [ 
            Header("Invalid Calculation"),
            "Theoretical yield must be greater than zero.",
            Button("Try Again", "stoichiometery"),

        ])

    #calculate percent yield
    percent_yield = (actual_product_mass / theoretical_yield) * 100

    #create detailed reactant calculations
    reactant_details = []

    for formula, coefficient in reactant_info:
        molar_mass = supported_formulas[formula].mass
        substance_moles = (reactant_moles/reactant_coefficient) * coefficient

        reactant_details.append(
            "Molar mass of " + formula + ": " + str(round(molar_mass, 2)) + " g/mol",
        )

        reactant_details.append(
            "Moles of " + formula + " = " + str(round(substance_moles, 4)) + " mol"
        )

    #create detailed product calculations
    product_details = []

    for formula, coefficient in product_info:
        molar_mass = supported_formulas[formula].mass
        substance_moles = (reactant_moles / reactant_coefficient) * coefficient
        substance_mass = substance_moles * molar_mass

        product_details.append(
            "Molar mass of " + formula + ": " + str(round(molar_mass,2)) + " g/mol")

        product_details.append(
            "Moles of " + formula + ": " + str(round(substance_moles,4)) + " mol")
        
        product_details.append(
            "Mass of " + formula + ": " + str(round(substance_mass,2)) + "g")

    #save inputs in state
    state.reactants = reactants
    state.products = products
    state.reactant_mass = reactant_mass
    state.actual_product_mass = actual_product_mass

    #create calculation instanc

    calculation = Calculation(
        reactants,
        products,
        reactant_mass,
        actual_product_mass,
        theoretical_yield,
        percent_yield

    )

    #add calculation to list
    state.calculations.append(calculation)

        #then the results are displayed
    return Page(state, [

        Header("Stoichiometry Calculator"),
        
        Header("Your Chemical Reaction"),
        
        reactants + " -> " + products,
        
        Header("Step 1: Calculate the molar mass of the "), 
        
        "Molar mass of " + reactant_formula + ": " + 
        str(round(reactant_molar_mass, 2)) + " g/mol",
        
        str(reactant_mass) + " g/ " +
        str(round(reactant_molar_mass, 2)) + " g/mol = " +
        str(round(reactant_moles, 4)) + " mole",
        
        Header("Step 2: Apply the Mole Ratio"),
        
        "Mole ratio = " +
        str(reactant_coefficient) + ":" +
        str(product_coefficient), 
        
        "Moles of " + product_formula + " = " +
        str(round(product_moles,4)) + " mol",
        
        Header("Step 3: Enter the Mass of Your First Reactant"),
        
        "Molar mass of " + product_formula + ": " +
        str(round(product_molar_mass, 2)) + " g/mol",
        
        "Theoertical yeild = " + 
        str(round(theoretical_yield, 2)) + " g",
        
        Header("Step 4: Calculate Percent Yield"),
        
        "Actual yield = " +
        str(actual_product_mass) + " g",
        
        "Percent yield = " + 
        str(round(percent_yield,2)) + " %",
        
        Header("Additional Reactant Information"),
        ]+ reactant_details + [
        Header("Additional Product Information")
        ] + product_details + [
        
        Button("Try Another Problem", "stoichiometry"),
        Button("Return Home", "index")
                        
        
        ])


#run unit tests
test_parse_substances()
test_calculate_theoretical_yield()
test_calculate_theoretical_yield()

    #Start website
start_server(State(
        "2 H2 + 1 O2",
        "2 H2O",
        10.0,
        3.0,
        "",
        []
))
