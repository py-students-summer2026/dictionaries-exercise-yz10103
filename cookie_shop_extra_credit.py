"""
Functions necessary for running a virtual cookie shop.
See README.md for instructions.
Do not run this file directly.  Rather, run main.py instead.
"""
import csv

def convert_yes_no_to_bool(answer):
    """
    Converts a yes/no string from the data file into a Boolean value.
    """
    answer = answer.strip().lower()

    if answer == "yes" or answer == "y":
        return True
    else:
        return False


def get_yes_or_no(prompt):
    """
    Asks the user a yes/no question and validates the response.
    """
    answer = input(prompt)
    answer = answer.strip().lower()

    while answer != "yes" and answer != "y" and answer != "no" and answer != "n":
        answer = input("Please enter yes, y, no, or n: ")
        answer = answer.strip().lower()

    return answer

def bake_cookies(filepath):
    """
    Opens up the CSV data file from the path specified as an argument.
    - Each line in the file, except the first, is assumed to contain comma-separated information about one cookie.
    - Creates a dictionary with the data from each line.
    - Adds each dictionary to a list of all cookies that is returned.

    :param filepath: The path to the data file.
    :returns: A list of all cookie data, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    cookies = []

    f = open(filepath, "r")
    reader = csv.reader(f)
    first_line = True

    for data in reader:
        if first_line == True:
            first_line = False
        else:
            cookie = {
                "id": int(data[0]),
                "title": data[1],
                "description": data[2],
                "price": float(data[3].replace("$", "").strip()),
                "sugar_free": convert_yes_no_to_bool(data[4]),
                "gluten_free": convert_yes_no_to_bool(data[5]),
                "contains_nuts": convert_yes_no_to_bool(data[6])
            }

            cookies.append(cookie)

    f.close()

    return cookies

def welcome():
    """
    Prints a welcome message to the customer in the format:

      Welcome to the Python Cookie Shop!
      We feed each according to their need.

    """
    # write your code for this function below this line
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.")
    print()
    print("We'd hate to trigger an allergic reaction in your body. So please answer the following questions:")
    print()

    nuts_answer = get_yes_or_no("Are you allergic to nuts? ")
    gluten_answer = get_yes_or_no("Are you allergic to gluten? ")
    sugar_answer = get_yes_or_no("Do you suffer from diabetes? ")

    customer_needs = {
        "avoid_nuts": convert_yes_no_to_bool(nuts_answer),
        "avoid_gluten": convert_yes_no_to_bool(gluten_answer),
        "avoid_sugar": convert_yes_no_to_bool(sugar_answer)
    }

    return customer_needs

def get_cookies_for_customer(cookies, customer_needs):
    """
    Returns only the cookies that match the customer's dietary needs.
    """
    matching_cookies = []

    for cookie in cookies:
        is_good_cookie = True

        if customer_needs["avoid_nuts"] == True and cookie["contains_nuts"] == True:
            is_good_cookie = False

        if customer_needs["avoid_gluten"] == True and cookie["gluten_free"] == False:
            is_good_cookie = False

        if customer_needs["avoid_sugar"] == True and cookie["sugar_free"] == False:
            is_good_cookie = False

        if is_good_cookie == True:
            matching_cookies.append(cookie)

    return matching_cookies


def display_cookies(cookies):
    """
    Prints a list of all cookies in the shop to the user.
    - Sample output - we show only two cookies here, but imagine the output continues for all cookiese:
        Here are the cookies we have in the shop for you:

          #1 - Basboosa Semolina Cake
          This is a This is a traditional Middle Eastern dessert made with semolina and yogurt then soaked in a rose water syrup.
          Price: $3.99

          #2 - Vanilla Chai Cookie
          Crisp with a smooth inside. Rich vanilla pairs perfectly with its Chai partner a combination of cinnamon ands ginger and cloves. Can you think of a better way to have your coffee AND your Vanilla Chai in the morning?
          Price: $5.50

    - If doing the extra credit version, ask the user for their dietary restrictions first, and only print those cookies that are suitable for the customer.

    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below this line
    print()

    if len(cookies) == 0:
        print("Sorry, we do not have any cookies that match your dietary needs.")
        print()

    else:
        print("Great! Here are the cookies that we think you might like:")
        print()

        for cookie in cookies:
            print("#" + str(cookie["id"]) + " - " + cookie["title"])
            print(cookie["description"])
            print("Price: $" + f"{cookie['price']:.2f}")
            print()

    

def get_cookie_from_dict(id, cookies):
    """
    Finds the cookie that matches the given id from the full list of cookies.

    :param id: the id of the cookie to look for
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: the matching cookie, as a dictionary
    """
    # write your code for this function below this line
    for cookie in cookies:
        if cookie["id"] == id:
            return cookie


def solicit_quantity(id, cookies):
    """
    Asks the user how many of the given cookie they would like to order.
    - Validates the response.
    - Uses the get_cookie_from_dict function to get the full information about the cookie whose id is passed as an argument, including its title and price.
    - Displays the subtotal for the given quantity of this cookie, formatted to two decimal places.
    - Follows the format (with sample responses from the user):

        My favorite! How many Animal Cupcakes would you like? 5
        Your subtotal for 5 Animal Cupcake is $4.95.

    :param id: the id of the cookie to ask about
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: The quantity the user entered, as an integer.
    """
    # write your code for this function below this line
    cookie = get_cookie_from_dict(id, cookies)

    quantity = input("My favorite! How many " + cookie["title"] + " would you like? ")

    while not quantity.isnumeric():
        quantity = input("Please enter the quantity as an integer: ")

    quantity = int(quantity)

    subtotal = quantity * cookie["price"]

    print("Your subtotal for " + str(quantity) + " " + cookie["title"] + " is $" + f"{subtotal:.2f}.")

    return quantity


def solicit_order(cookies):
    """
    Takes the complete order from the customer.
    - Asks over-and-over again for the user to enter the id of a cookie they want to order until they enter 'finished', 'done', 'quit', or 'exit'.
    - Validates the id the user enters.
    - For every id the user enters, determines the quantity they want by calling the solicit_quantity function.
    - Places the id and quantity of each cookie the user wants into a dictionary with the format
        {'id': 5, 'quantity': 10}
    - Returns a list of all sub-orders, in the format:
        [
          {'id': 5, 'quantity': 10},
          {'id': 1, 'quantity': 3}
        ]

    :returns: A list of the ids and quantities of each cookies the user wants to order.
    """
    # write your code for this function below this line
    order = []

    keep_ordering = True


    while keep_ordering:
        if len(order) == 0:
            cookie_id = input("Please enter the number of any cookie you would like to purchase: ")
        else:
            cookie_id = input('Please enter the number of any other cookie you would like to purchase (type "finished" if finished with your order): ')
        
        cookie_id = cookie_id.strip().lower()

        if cookie_id == "finished" or cookie_id == "done" or cookie_id == "quit" or cookie_id == "exit":
            keep_ordering = False

        elif cookie_id.isnumeric():
            cookie_id = int(cookie_id)

            cookie = get_cookie_from_dict(cookie_id, cookies)

            if cookie == None:
                print("Sorry, that is not a cookie we have in the shop.")
            else:
                quantity = solicit_quantity(cookie_id, cookies)

                sub_order = {
                    "id": cookie_id,
                    "quantity": quantity
                }

                order.append(sub_order)

        else:
            print("Please enter a cookie number as an integer.")

    return order


def display_order_total(order, cookies):
    """
    Prints a summary of the user's complete order.
    - Includes a breakdown of the title and quantity of each cookie the user ordereed.
    - Includes the total cost of the complete order, formatted to two decimal places.
    - Follows the format:

        Thank you for your order. You have ordered:

        -8 Animal Cupcake
        -1 Basboosa Semolina Cake

        Your total is $11.91.
        Please pay with Bitcoin before picking-up.

        Thank you!
        -The Python Cookie Shop Robot.

    """
    # write your code for this function below this line
    total = 0

    print()
    print("Thank you for your order. You have ordered:")
    print()

    for item in order:
        cookie_id = item["id"]
        quantity = item["quantity"]

        cookie = get_cookie_from_dict(cookie_id, cookies)

        print("-" + str(quantity) + " " + cookie["title"])

        subtotal = quantity * cookie["price"]
        total = total + subtotal

    print()
    print("Your total is $" + f"{total:.2f}.")
    print("Please pay with Bitcoin before picking-up.")
    print()
    print("Thank you!")
    print("-The Python Cookie Shop Robot.")


def run_shop(cookies):
    """
    Executes the cookie shop program, following requirements in the README.md file.
    - This function definition is given to you.
    - Do not modify it!

    :param cookies: A list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    customer_needs = welcome()
    matching_cookies = get_cookies_for_customer(cookies, customer_needs)
    display_cookies(matching_cookies)

    if len(matching_cookies) > 0:
        order = solicit_order(matching_cookies)
        display_order_total(order, matching_cookies)
