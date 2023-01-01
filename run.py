from datetime import datetime
from scripts.get_resources import (GamePlayVisuals, LocationVisuals, WeaponVisuals, InventoryVisuals,
                                   MonsterVisual, OrbVisuals)

from scripts.transactions import (CreateInsertUpdateDeleteRecord, RetrieveTransaction)

# using colors on string
# REF: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
W = '\033[0m'  # white
B = '\033[34m'  # blue
ENDC = '\033[0m'  # Ends the color
BOLD = '\033[1m'  # bold letters
UNDERLINE = '\033[4m'  # underline string


class Fallen:

    def __int__(self):
        pass

    def contnue_or_quit(self):
        print("==" * 50)
        ans = input(O+BOLD+"""
            ========================================
            Want to continue from where you stopped?
            ========================================
            Enter yes: to continue: 
            ========================================
            Enter no: to quit: 
            """+ENDC).lower()

        if ans == 'no':
            quit()

    def show_weapons_and_inventories(self, location_description, coins):
        # cut from here
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)
        print(O + BOLD + "Purchase weapons and inventories which you can afford" + ENDC)
        print("==" * 50)
        print(O + BOLD + UNDERLINE + f"Your available balance is: £{coins}.00" + ENDC)
        print("==" * 50)

        # get weapons and weapon visuals
        weapons = RetrieveTransaction().get_weapons()
        weapon_visuals = WeaponVisuals().list_of_weapon_visuials()

        # get inventories and inventory visuals
        inventories = RetrieveTransaction().get_inventories()
        inventory_visuals = InventoryVisuals().list_of_inventories()

        print(O + BOLD + "Here are the weapons and their prices" + ENDC)

        for weapon, visual in zip(weapons, weapon_visuals):
            print(f"""
                   =======================================
                   {B}S/N: {R}{weapon[0]}{ENDC}
                   {B}Weapons: {R}{weapon[1]}{ENDC}
                   {B}Prices: {R}£{weapon[2]}.00{ENDC}
                   ========================================
                   {visual}
                   """)

        print("==" * 50)
        print(O + BOLD + "Here are the inventories and their prices" + ENDC)

        for inventory, inventory_visual in zip(inventories, inventory_visuals):
            print(f"""
            ====================================
            {B}S/N: {R}{inventory[0]}{ENDC}
            {B}Inventories: {R}{inventory[1]}{ENDC}
            {B}Description: {R}{inventory[2]}{ENDC}
            {B}Prices: {R}£{inventory[3]}.00{ENDC}
            ====================================
            {inventory_visual}
            """)

    def create_account(self):
        # this method is a view that allows character creation
        print("==" * 50)
        print(O + BOLD + """Before you proceed and conquer the realms. 
        Kindly create your character using a username and password""" + ENDC)
        print("==" * 50)

        # request username
        username = input(B + BOLD + "Kindly input your username: " + ENDC)

        # check if the user already exists
        check_user = RetrieveTransaction().check_user(username=username)

        # if user already exists
        if check_user:
            print("Sorry but this user already exists.")
            print("==" * 50)
            ans = input(f"""
            ==============================================================
            {O}{BOLD}Have an account already (yes/no)?{ENDC} 
            ============================================================== 
            {B}{BOLD} No. Create my account:{ENDC} 
            ==============================================================
            {B}{BOLD} Yes. Go to login:{ENDC} 
            ==============================================================
            """).lower()

            if ans == "no":
                self.create_account()
            elif ans == "yes":
                self.login()
            else:
                print(R + BOLD + "Invalid input" + ENDC)
                self.create_account()

        # collect user's password
        password = input(B + BOLD + "Kindly input your password: " + ENDC)
        # make sure username is more 3 characters
        if len(username) < 3:
            print(R + BOLD + "Username should be more than 3 characters. Kindly select an appropriate username" + ENDC)
            self.create_account()

        # make sure password is not lesser than 5 characters and more than 16 characters
        if 5 > len(password) > 16:
            print(O + BOLD + """ Password should be more than 5 characters and less than 16 characters.
            Kindly select an appropriate password.""" + ENDC)
            self.create_account()

        print("==" * 50)

        print(O + BOLD + """In Roth there are two unique races that characters can choose from.
            Your character can either be an Orixinais or a Viaxeiros""" + ENDC)

        print("==" * 50)

        print(O + BOLD + "Choose Your race" + ENDC)

        # user should select a race
        race = input(
            f"""
            ============================================ 
            {B}{BOLD}Enter 1: Orixinais:{ENDC} 
            ============================================
            {B}{BOLD}Enter 2: Viaxeiros:{ENDC} 
            """
        ).lower()

        print("==========================================")

        if str(race) != '1' and str(race) != '2':
            print(R + BOLD + "Invalid selection. Please select either 1 or 2" + ENDC)
            self.create_account()

        # create user account
        user_id = CreateInsertUpdateDeleteRecord().create_user(username=username, password=password, race_id=int(race))

        # if user was successfully created
        if user_id:
            get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
            print(f"""
            ================================================================
            {G}{BOLD}Congratulations{ENDC} {O}{BOLD}{get_user[1]}!{ENDC}
            ================================================================
            {O}{BOLD}Your character has been created!{ENDC}
            ================================================================
            {O}{BOLD}Time to get started on your Journey.{ENDC}
            ================================================================
            """)

            # send users into the appropriate world
            if get_user[8] == 1:
                # if user's race is Orixinais save user's first location to terra
                CreateInsertUpdateDeleteRecord().save_user_location(user_id, 1)
                self.terra_market_place_level(user_id, get_user[1])
            elif get_user[8] == 2:
                # if user's race is Viaxeiros save user's first location to inferno
                CreateInsertUpdateDeleteRecord().save_user_location(user_id, 6)
                self.inferno_shop_level(user_id, get_user[1])

    def login(self):
        print(G + "==" * 30 + ENDC)
        print(O + BOLD + "Welcome in player! lets get you logged in so you can keep playing!" + ENDC)
        print(G + "==" * 50 + ENDC)

        # collect username from user
        username = input(B + BOLD + "Kindly input your username: " + ENDC)

        # collect password from
        password = input(B + BOLD + "Kindly input your password: " + ENDC)

        # check if user exists and log them in
        user = RetrieveTransaction().login_user(username=username, password=password)

        if user:
            # get user's current location in the game world and log them in
            # [(user_id, location_id), (user_id, location_id), (user_id, location)]
            get_user_location = RetrieveTransaction().get_user_locations(user_id=user[0])
            if get_user_location[-1][1] == 1:
                self.terra_market_place_level(user[0], user[1])
            elif get_user_location[-1][1] == 2:
                self.gorr_fortress_level(user)
            elif get_user_location[-1][1] == 3:
                self.snake_island_level(user)
            elif get_user_location[-1][1] == 4:
                self.terra_nova_level(user)
            elif get_user_location[-1][1] == 5:
                self.dark_dungeon_level(user)
            elif get_user_location[-1][1] == 6:
                self.inferno_shop_level(user[0], user[1])
            elif get_user_location[-1][1] == 7:
                self.cross_roads_level(user)
            elif get_user_location[-1][1] == 8:
                self.damned_valley_level(user)
            elif get_user_location[-1][1] == 9:
                self.torture_lair(user)
            elif get_user_location[-1][1] == 10:
                self.demon_cave_level(user)
            elif get_user_location[-1][1] == 11:
                self.golden_gates_level(user)
        else:
            # if user doesn't exist prompt them to try again or create an account
            ans = input(f"""
            =======================================
            {R}{BOLD}Sorry Could not find this user{ENDC}
            ==============================================================
            {O}{BOLD}Do you own an account (yes/no)?{ENDC}
            ==============================================================
            {B}{BOLD}No. Create my account:{ENDC}
            ==============================================================
            {B}{BOLD}Yes. Go to login:
            """).lower()

            if ans == "no":
                self.create_account()
            elif ans == "yes":
                self.login()
            else:
                print(R + BOLD + "Invalid input" + ENDC)
                self.create_account()

    def terra_market_place_level(self, user_id, username):
        # ask users if they would like to take a break
        # self.contnue_or_quit()

        # get the user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)

        # get the current coin attribute
        coins = get_user[6]

        # get current location
        get_location = RetrieveTransaction().get_location_by_id(1)

        # get the location name
        location_name = get_location[1]

        # get the location description
        location_description = get_location[2]

        # get the realm object
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # get the realm description
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {username}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)

        # show the visuals of the realm
        print(LocationVisuals().terra_city_market())

        # show the inventories and weapons gamers can select from
        self.show_weapons_and_inventories(location_description, coins)

        # get the user's current weapons
        user_weapons = RetrieveTransaction().get_user_weapons(user_id)

        # if the user has bought a weapon before, ask user if they'd be interested to buy another one
        if user_weapons and len(user_weapons) > 0:
            prmt = input(R + BOLD + "Would you like to purchase another weapon (yes/No)? " + ENDC).lower()

            # if yes, show the user the balance on his account and ask user to select a weapon using the S/N
            if prmt == 'yes':
                print("==" * 50)
                print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
                print("==" * 50)
                print("""use the serial number (S/N) to purchase the weapon you want e.g 1.
                      Remember to purchase one you can afford with your current balance""")
                print("==" * 50)

                s_n = input(B + BOLD + "input the serial number here: " + ENDC).lower()

                get_weapon = RetrieveTransaction().get_weapon_by_id(int(s_n))  # (id, name, price)

                print("=============================================================================================")
                print(R + BOLD + f"You choose: {get_weapon[1]}")
                print("=============================================================================================")

                # if the users balance is less than the cost of the weapon abort or start over
                if coins < get_weapon[2]:
                    print(R + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
                    print()
                    ans = input(B + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
                    if ans == 'yes':
                        self.terra_market_place_level(get_user[0], get_user[1])
                    elif ans == 'no':
                        quit()
                else:
                    # if the coins is more than the balance then proceed to purchase
                    balance = coins - get_weapon[2]
                    update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
                    purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_weapon(get_user[0], int(s_n))
                    if purchase_weapon and update_price:
                        print(B + BOLD + "You have successfully chosen that weapon!!" + ENDC)
                        print(O + BOLD + "Congrats!!! Warrior. Lets Keep the good work going!!" + ENDC)

            # if the user selected no, then take user to his last known location in the realm
            elif prmt == 'no':
                get_user_location = RetrieveTransaction().get_user_locations(user_id=get_user[0])
                get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)

                # if user is coming from the inferno world whose last id is 10
                # if the user doesn't want to purchase any weapon then send the user to the next realm
                CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 2)
                if get_user_location[-1][1] == 2:
                    self.gorr_fortress_level(get_user)
                elif get_user_location[-1][1] == 3:
                    self.snake_island_level(get_user)
                elif get_user_location[-1][1] == 4:
                    self.terra_nova_level(get_user)
                elif get_user_location[-1][1] == 5:
                    self.dark_dungeon_level(get_user)
                elif get_user_location[-1][1] == 6:
                    self.inferno_shop_level(get_user[0], get_user[1])
                elif get_user_location[-1][1] == 7:
                    self.cross_roads_level(get_user)
                elif get_user_location[-1][1] == 8:
                    self.damned_valley_level(get_user)
                elif get_user_location[-1][1] == 9:
                    self.torture_lair(get_user)
                elif get_user_location[-1][1] == 10:
                    self.demon_cave_level(get_user)
                elif get_user_location[-1][1] == 11:
                    self.golden_gates_level(get_user)
            else:
                print(R+BOLD+"Invalid response"+ENDC)
                self.terra_market_place_level(get_user[0], get_user[1])

        # check for user inventory too
        # For inventory purchase
        # get new user object and coins
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
        coins = get_user[6]

        # retrieve all user's inventory
        user_inventories = RetrieveTransaction().get_user_inventories(user_id)

        # if user has selected an inventory before, ask user if they'd like to buy another one.
        if user_inventories and len(user_inventories) > 0:
            prompt_ = input(R + BOLD + "Would you like to purchase another inventory (yes/No)? " + ENDC).lower()

            # if yes, show the user the balance on his account and ask user to select a weapon using the S/N
            if prompt_ == 'yes':
                print("==" * 50)
                print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
                print("==" * 50)
                print("""use the serial number (S/N) to purchase the inventory you want e.g 1.
                Remember to purchase one you can afford with your current balance""")
                print("==" * 50)

                i_n = input(B + BOLD + "input the serial number here: " + ENDC).lower()

                # get the inventory by id
                get_inventory = RetrieveTransaction().get_inventory_by_id(int(i_n))  # (id, name, description, price)

                print("=============================================================================================")
                print(R + BOLD + UNDERLINE + f"You choose: {get_inventory[1]}")
                print("=============================================================================================")

                # if the users balance is less than the cost of the weapon abort or start over
                if coins < get_inventory[3]:
                    print(O + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
                    print()
                    ans = input(O + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
                    if ans == 'yes':
                        self.terra_market_place_level(get_user[0], get_user[1])
                    elif ans == 'no':
                        quit()
                else:
                    # if the coins is more than the balance then proceed to purchase
                    balance = coins - get_inventory[3]
                    update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
                    purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_inventory(get_user[0], int(i_n))
                    if purchase_weapon and update_price:
                        print(B + BOLD + "You have successfully chosen that inventory!!" + ENDC)
                        print(O + BOLD + "Congrats!!! Warrior. LeTS Keep the good work going!!" + ENDC)

            # if the user selected no, then take user to his last known location in the realm
            elif prompt_ == 'no':
                get_user_location = RetrieveTransaction().get_user_locations(user_id=get_user[0])
                get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)

                # if user is coming from the inferno world whose last id is 10
                # if the user doesn't want to purchase any weapon then send the user to the next realm
                CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 2)
                if get_user_location[-1][1] == 2:
                    self.gorr_fortress_level(get_user)
                elif get_user_location[-1][1] == 3:
                    self.snake_island_level(get_user)
                elif get_user_location[-1][1] == 4:
                    self.terra_nova_level(get_user)
                elif get_user_location[-1][1] == 5:
                    self.dark_dungeon_level(get_user)
                elif get_user_location[-1][1] == 6:
                    self.inferno_shop_level(get_user[0], get_user[1])
                elif get_user_location[-1][1] == 7:
                    self.cross_roads_level(get_user)
                elif get_user_location[-1][1] == 8:
                    self.damned_valley_level(get_user)
                elif get_user_location[-1][1] == 9:
                    self.torture_lair(get_user)
                elif get_user_location[-1][1] == 10:
                    self.demon_cave_level(get_user)
                elif get_user_location[-1][1] == 11:
                    self.golden_gates_level(get_user)
            else:
                print(R+BOLD+"Invalid response"+ENDC)
                self.terra_market_place_level(get_user[0], get_user[1])

            # congratulations you have finished mission one
            # your location will be upgraded
            print(O + BOLD + "Congrats!!! Warrior. Lets Keep the good work going!!" + ENDC)
            get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 2)
            self.gorr_fortress_level(get_user)

        # now for new gamers that are yet to select any weapon of inventory
        # This part is for newcomers
        print(B + BOLD + "Kindly purchase an affordable weapon for your journey" + ENDC)
        print("==" * 50)
        print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
        print("""use the serial number (S/N) to purchase the weapon you want e.g 1.
              Remember to purchase one you can afford with your current balance""")
        print("==" * 50)

        s_n_ = input(O + BOLD + "input the weapon number here: " + ENDC).lower()

        # get the weapon by the id
        get_weapon = RetrieveTransaction().get_weapon_by_id(int(s_n_))  # (id, name, price)

        print("=============================================================================================")
        print(R + BOLD + UNDERLINE + f"You choose this weapon: {get_weapon[1]}" + ENDC)
        print("=============================================================================================")

        # if the user's coins is less than the weapon
        if coins < get_weapon[2]:
            print(B + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
            print()
            ans = input(B + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
            if ans == 'yes':
                self.terra_market_place_level(get_user[0], get_user[1])
            elif ans == 'no':
                quit()
        else:
            # of the coins is greater than the price of the weapon
            balance = coins - get_weapon[2]
            update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
            purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_weapon(get_user[0], int(s_n_))
            if purchase_weapon and update_price:
                print(B + BOLD + "You have successfully chosen that weapon!!" + ENDC)

        # new user's will also purchase an inventory
        # For inventory purchase
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
        coins = get_user[6]

        print(B + BOLD + "Kindly purchase an affordable inventory for your journey" + ENDC)
        print("==" * 50)
        print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
        print("""use the serial number (S/N) to purchase the weapon you want e.g 1.
                      Remember to purchase one you can afford with your current balance""")
        print("==" * 50)

        i_n_ = input(O + BOLD + "input the inventory S/N here: " + ENDC).lower()

        # get that inventory by id
        get_inventory = RetrieveTransaction().get_inventory_by_id(int(i_n_))  # (id, name, description, price)

        print("=============================================================================================")
        print(R + BOLD + UNDERLINE + f"You choose this inventory: {get_inventory[1]}" + ENDC)
        print("=============================================================================================")

        # make sure the coins are not less than the inventory price
        # if they are than reset or quit
        if coins < get_inventory[3]:
            print(B + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
            print()
            ans = input(B + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
            if ans == 'yes':
                self.terra_market_place_level(get_user[0], get_user[1])
            elif ans == 'no':
                quit()
        else:
            # if the coins is more than the price then proceed to buying te inventory
            balance = coins - get_inventory[3]
            update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
            purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_inventory(get_user[0], int(i_n_))
            if purchase_weapon and update_price:
                print(B + BOLD + "You have successfully chosen that inventory!!" + ENDC)

        # congratulations you have finished mission one
        # your location will be upgraded
        print(O + BOLD + "Congrats!!! Warrior. Lets Keep the good work going!!" + ENDC)
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
        CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 2)
        self.gorr_fortress_level(get_user)

    # does not contain an orb
    def gorr_fortress_level(self, user):
        # do you want to quit or continue
        self.contnue_or_quit()

        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(2)

        # get the name of the current location
        location_name = get_location[1]

        # get the description of the current location
        location_description = get_location[2]

        # get the realm object
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the name of the realm
        realm_name = realm[1]

        # get the description of the realm
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)

        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(LocationVisuals().gorr_fortress())
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # retrieve your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are faced with the mighty gorr" + ENDC)

        # show the monster
        print(MonsterVisual().gorr())

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the monster" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        # print out all the user's weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapon: {R}{weapon[1]}{ENDC}
               ========================================
               """)
        # ask user to select a weapon
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get your preferred weapon by id
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if your selection is invalid
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.gorr_fortress_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow"+ENDC)

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # after killing the monster
        # upgrade the user's strength level
        strength = 10
        print("variable strength")
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)
        # add 10 to the user's current coin
        coin_gained = get_user[6] + 10
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)

        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])
        print(f"This is your new balance: {get_user[6]}")

        if 50 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        # update the current location of the game
        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 3)
            self.snake_island_level(get_user)

    # has an orb
    def snake_island_level(self, user):
        # ask user if they want to continue or not
        self.contnue_or_quit()

        # get user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(3)

        # location name
        location_name = get_location[1]

        # location description
        location_description = get_location[2]

        # get the realm
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # realm description
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(LocationVisuals().snake_island())
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # get your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are in contact with the large snakes" + ENDC)

        print(MonsterVisual().snakes())

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the monster" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        #  lists all users weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)

        # select the weapon using the S/N (also known as the id)
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get the weapon by passing the id into the method
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if the user entry is in valid reset the world
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.snake_island_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        strength = 10
        # update the user's strength level
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)
        # add to the user's current coin
        coin_gained = get_user[6] + 10
        # inititiate the update price method
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)

        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        print("==" * 50)
        print(O + BOLD + "You look around and you found an orb" + ENDC)
        print("==" * 50)

        # current location id
        location_id = 3

        # retrieve the orb
        orb = RetrieveTransaction().get_orb_by_location(location_id)

        # orb name
        orb_name = orb[0][1]

        # orb description
        orb_description = orb[0][2]

        # show the orb visuals
        print(O + BOLD + f"""The orb is a {B}{orb_name}""" + ENDC)
        print(O + BOLD + OrbVisuals().poder() + ENDC)
        print()
        print(f"{orb_description}")
        print("You stretch out your hands and grab it")

        # save the user's orb
        save_user_orb = CreateInsertUpdateDeleteRecord().save_user_orb(get_user[0], orb[0][0])

        # if save had an issue then print an error
        if not save_user_orb:
            print(R+BOLD+"Sorry something went wrong with the program"+ENDC)

        print(G + BOLD + "You have an orb now. Congrats" + ENDC)

        # get new user id
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # try to update the rank by making sure rank condition is met

        if 40 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        get_user_orbs = RetrieveTransaction().get_user_orb(get_user[0])

        # line of code is for locations with orbs
        if get_user_orbs and len(get_user_orbs) >= 3:
            print(O + BOLD + "This is your ascension to The Paraíso relam!" + ENDC)
            CreateInsertUpdateDeleteRecord().game_won(get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 11)
            self.golden_gates_level(get_user)

        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 4)
            self.terra_nova_level(get_user)

    # does not have orb
    def terra_nova_level(self, user):

        # do you want to quit or continue
        self.contnue_or_quit()

        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(4)

        # get the name of the current location
        location_name = get_location[1]

        # get the description of the current location
        location_description = get_location[2]

        # get the realm object
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the name of the realm
        realm_name = realm[1]

        # get the description of the realm
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)

        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(LocationVisuals().terra_nova())
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # retrieve your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are faced with by the Harpy creature" + ENDC)

        # show the monster
        print(MonsterVisual().harpy_demon())

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the monster" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        # print out all the user's weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)
        # ask user to select a weapon
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get your preferred weapon by id
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if your selection is invalid
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.terra_nova_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # after killing the monster
        # upgrade the users
        strength = 10
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)

        # add 10 to the user's current coin
        coin_gained = get_user[6] + 10
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)
        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])
        print(f"This is your new balance: {get_user[6]}")

        # update the rank if strength level condition is met

        if 40 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        # update the current location of the game
        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 5)
            self.dark_dungeon_level(get_user)

    # has an orb
    def dark_dungeon_level(self, user):
        # ask user if they want to continue or not
        self.contnue_or_quit()

        # get user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(5)

        # location name
        location_name = get_location[1]

        # location description
        location_description = get_location[2]

        # get the realm
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # realm description
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(LocationVisuals().dark_dungeon())
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # get your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are in contact with the evil sorcerers " + ENDC)

        print(MonsterVisual().sorcerers())

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the monster" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        #  lists all users weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)

        # select the weapon using the S/N (also known as the id)
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get the weapon by passing the id into the method
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if the user entry is in valid reset the world
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.dark_dungeon_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # update the user's strength level
        strength = 10
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)
        # add to the user's current coin
        coin_gained = get_user[6] + 10
        # initiate the update price method
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)

        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        print("==" * 50)
        print(O + BOLD + "You look around and you found an orb" + ENDC)
        print("==" * 50)

        # current location id
        location_id = 5

        # retrieve the orb
        orb = RetrieveTransaction().get_orb_by_location(location_id)

        # orb name
        orb_name = orb[0][1]

        # orb description
        orb_description = orb[0][2]

        # show the orb visuals
        print(O + BOLD + f"""The orb is a {B}{orb_name}""" + ENDC)
        print(B + BOLD + OrbVisuals().conecementor() + ENDC)
        print()
        print(f"{orb_description}")
        print("You stretch out your hands and grab it")

        # save the user's orb
        save_user_orb = CreateInsertUpdateDeleteRecord().save_user_orb(get_user[0], orb[0][0])

        # if save had an issue then print an error
        if not save_user_orb:
            print(R+BOLD+"Sorry something went wrong with the program"+ENDC)

        print(G + BOLD + "You have an orb now. Congrats" + ENDC)

        # get new user id
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # try to update the rank by making sure rank condition is met

        if 40 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        get_user_orbs = RetrieveTransaction().get_user_orb(get_user[0])

        # line of code is for locations with orbs
        if get_user_orbs and len(get_user_orbs) >= 3:
            print(O + BOLD + "This is your ascension to The Paraíso relam!" + ENDC)
            CreateInsertUpdateDeleteRecord().game_won(get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 11)
            self.golden_gates_level(get_user)

        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 6)
            self.inferno_shop_level(get_user[0], get_user[1])

    def inferno_shop_level(self, user_id, username):

        # ask users if they would like to take a break
        # self.contnue_or_quit()

        # get the user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)

        # get the current coin attribute
        coins = get_user[6]

        # get current location
        get_location = RetrieveTransaction().get_location_by_id(6)

        # get the location name
        location_name = get_location[1]

        # get the location description
        location_description = get_location[2]

        # get the realm object
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # get the realm description
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {username}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)

        # show the visuals of the realm
        print(R+BOLD+LocationVisuals().inferno_shop()+ENDC)

        # show the inventories and weapons gamers can select from
        self.show_weapons_and_inventories(location_description, coins)

        # get the user's current weapons
        user_weapons = RetrieveTransaction().get_user_weapons(user_id)

        # if the user has bought a weapon before, ask user if they'd be interested to buy another one
        if user_weapons and len(user_weapons) > 0:
            prmt = input(R + BOLD + "Would you like to purchase another weapon (yes/no)? " + ENDC).lower()

            # if yes, show the user the balance on his account and ask user to select a weapon using the S/N
            if prmt == 'yes':
                print("==" * 50)
                print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
                print("==" * 50)
                print("""use the serial number (S/N) to purchase the weapon you want e.g 1.
                      Remember to purchase one you can afford with your current balance""")
                print("==" * 50)

                s_n = input(B + BOLD + "input the serial number here: " + ENDC).lower()

                get_weapon = RetrieveTransaction().get_weapon_by_id(int(s_n))  # (id, name, price)

                print("=============================================================================================")
                print(R + BOLD + f"You choose this weapon: {get_weapon[1]}"+ENDC)
                print("=============================================================================================")

                # if the users balance is less than the cost of the weapon abort or start over
                if coins < get_weapon[2]:
                    print(R + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
                    print()
                    ans = input(B + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
                    if ans == 'yes':
                        self.inferno_shop_level(get_user[0], get_user[1])
                    elif ans == 'no':
                        quit()
                else:
                    # if the coins is more than the balance then proceed to purchase
                    balance = coins - get_weapon[2]
                    update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
                    purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_weapon(get_user[0], int(s_n))
                    if purchase_weapon and update_price:
                        print(B + BOLD + "You have successfully chosen that weapon!!" + ENDC)
                        print(O + BOLD + "Congrats!!! Warrior. Lets Keep the good work going!!" + ENDC)

            # if the user selected no, then take user to his last known location in the realm
            elif prmt == 'no':
                get_user_location = RetrieveTransaction().get_user_locations(user_id=get_user[0])
                get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)

                CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 7)
                if get_user_location[-1][1] == 1:
                    self.terra_market_place_level(get_user[0], get_user[1])
                elif get_user_location[-1][1] == 2:
                    self.gorr_fortress_level(get_user)
                elif get_user_location[-1][1] == 3:
                    self.snake_island_level(get_user)
                elif get_user_location[-1][1] == 4:
                    self.terra_nova_level(get_user)
                elif get_user_location[-1][1] == 5:
                    self.dark_dungeon_level(get_user)
                elif get_user_location[-1][1] == 7:
                    self.cross_roads_level(get_user)
                elif get_user_location[-1][1] == 8:
                    self.damned_valley_level(get_user)
                elif get_user_location[-1][1] == 9:
                    self.torture_lair(get_user)
                elif get_user_location[-1][1] == 10:
                    self.demon_cave_level(get_user)
                elif get_user_location[-1][1] == 11:
                    self.golden_gates_level(get_user)
            else:
                print(R + BOLD + "Invalid response" + ENDC)
                self.inferno_shop_level(get_user[0], get_user[1])

        # check for user inventory too
        # For inventory purchase
        # get new user object and coins
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
        coins = get_user[6]

        # retrieve all user's inventory
        user_inventories = RetrieveTransaction().get_user_inventories(user_id)

        # if user has selected an inventory before, ask user if they'd like to buy another one.
        if user_inventories and len(user_inventories) > 0:
            prompt_ = input(R + BOLD + "Would you like to purchase another inventory (yes/No)? " + ENDC).lower()

            # if yes, show the user the balance on his account and ask user to select a weapon using the S/N
            if prompt_ == 'yes':
                print("==" * 50)
                print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
                print("==" * 50)
                print("""use the serial number (S/N) to purchase the inventory you want e.g 1.
                Remember to purchase one you can afford with your current balance""")
                print("==" * 50)

                i_n = input(B + BOLD + "input the serial number here: " + ENDC).lower()

                # get the inventory by id
                get_inventory = RetrieveTransaction().get_inventory_by_id(int(i_n))  # (id, name, description, price)

                print("=============================================================================================")
                print(R + BOLD + f"You chose: {get_inventory[1]}"+ENDC)
                print("=============================================================================================")

                # if the users balance is less than the cost of the weapon abort or start over
                if coins < get_inventory[3]:
                    print(O + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
                    print()
                    ans = input(O + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
                    if ans == 'yes':
                        self.inferno_shop_level(get_user[0], get_user[1])
                    elif ans == 'no':
                        quit()
                else:
                    # if the coins is more than the balance then proceed to purchase
                    balance = coins - get_inventory[3]
                    update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
                    purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_inventory(get_user[0], int(i_n))
                    if purchase_weapon and update_price:
                        print(B + BOLD + "You have successfully chosen that inventory!!" + ENDC)
                        print(O + BOLD + "Congrats!!! Warrior. LeTS Keep the good work going!!" + ENDC)

            # if the user selected no, then take user to his last known location in the realm
            elif prompt_ == 'no':
                get_user_location = RetrieveTransaction().get_user_locations(user_id=get_user[0])
                get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)

                CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 7)
                if get_user_location[-1][1] == 1:
                    self.terra_market_place_level(get_user[0], get_user[1])
                elif get_user_location[-1][1] == 2:
                    self.gorr_fortress_level(get_user)
                elif get_user_location[-1][1] == 3:
                    self.snake_island_level(get_user)
                elif get_user_location[-1][1] == 4:
                    self.terra_nova_level(get_user)
                elif get_user_location[-1][1] == 5:
                    self.dark_dungeon_level(get_user)
                elif get_user_location[-1][1] == 7:
                    self.cross_roads_level(get_user)
                elif get_user_location[-1][1] == 8:
                    self.damned_valley_level(get_user)
                elif get_user_location[-1][1] == 9:
                    self.torture_lair(get_user)
                elif get_user_location[-1][1] == 10:
                    self.demon_cave_level(get_user)
                elif get_user_location[-1][1] == 11:
                    self.golden_gates_level(get_user)
            else:
                print(R + BOLD + "Invalid response" + ENDC)
                self.inferno_shop_level(get_user[0], get_user[1])

            # congratulations you have finished mission one
            # your location will be upgraded
            print(O + BOLD + "Congrats!!! Warrior. Lets Keep the good work going!!" + ENDC)
            get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 7)
            self.cross_roads_level(get_user)

        # now for new gamers that are yet to select any weapon of inventory
        # This part is for newcomers
        print(B + BOLD + "Kindly purchase an affordable weapon for your journey" + ENDC)
        print("==" * 50)
        print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
        print("""use the serial number (S/N) to purchase the weapon you want e.g 1.
              Remember to purchase one you can afford with your current balance""")
        print("==" * 50)

        s_n_ = input(O + BOLD + "input the weapon number here: " + ENDC).lower()

        # get the weapon by the id
        get_weapon = RetrieveTransaction().get_weapon_by_id(int(s_n_))  # (id, name, price)

        print("=============================================================================================")
        print(R + BOLD + UNDERLINE + f"You choose: {get_weapon[1]}" + ENDC)
        print("=============================================================================================")

        # if the user's coins is less than the weapon
        if coins < get_weapon[2]:
            print(B + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
            print()
            ans = input(B + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
            if ans == 'yes':
                self.inferno_shop_level(get_user[0], get_user[1])
            elif ans == 'no':
                quit()
        else:
            # of the coins is greater than the price of the weapon
            balance = coins - get_weapon[2]
            update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
            purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_weapon(get_user[0], int(s_n_))
            if purchase_weapon and update_price:
                print(B + BOLD + "You have successfully chosen that weapon!!" + ENDC)

        # new user's will also purchase an inventory
        # For inventory purchase
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
        coins = get_user[6]

        print(B + BOLD + "Kindly purchase an affordable inventory for your journey" + ENDC)
        print("==" * 50)
        print(R + BOLD + f"Here is your balance £{coins}.00" + ENDC)
        print("""use the serial number (S/N) to purchase the inventory you want e.g 1.
                      Remember to purchase one you can afford with your current balance""")
        print("==" * 50)

        i_n_ = input(O + BOLD + "input the inventory S/N here: " + ENDC).lower()

        # get that inventory by id
        get_inventory = RetrieveTransaction().get_inventory_by_id(int(i_n_))  # (id, name, description, price)

        print("=============================================================================================")
        print(R + BOLD + UNDERLINE + f"You choose: {get_inventory[1]}" + ENDC)
        print("=============================================================================================")

        # make sure the coins are not less than the inventory price
        # if they are than reset or quit
        if coins < get_inventory[3]:
            print(B + BOLD + "Sorry you do not have a sufficient balance" + ENDC)
            print()
            ans = input(B + BOLD + "Do you want to try again or quit (yes/no)? " + ENDC).lower()
            if ans == 'yes':
                self.terra_market_place_level(get_user[0], get_user[1])
            elif ans == 'no':
                quit()
        else:
            # if the coins is more than the price then proceed to buying te inventory
            balance = coins - get_inventory[3]
            update_price = CreateInsertUpdateDeleteRecord().update_price(get_user[0], balance)
            purchase_weapon = CreateInsertUpdateDeleteRecord().save_user_inventory(get_user[0], int(i_n_))
            if purchase_weapon and update_price:
                print(B + BOLD + "You have successfully chosen that inventory!!" + ENDC)

        # congratulations you have finished mission one
        # your location will be upgraded
        print(O + BOLD + "Congrats!!! Warrior. Lets Keep the good work going!!" + ENDC)
        get_user = RetrieveTransaction().get_user_by_id(user_id=user_id)
        CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 7)
        self.cross_roads_level(get_user)

    # does not have an orb
    def cross_roads_level(self, user):

        # do you want to quit or continue
        self.contnue_or_quit()

        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(7)

        # get the name of the current location
        location_name = get_location[1]

        # get the description of the current location
        location_description = get_location[2]

        # get the realm object
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the name of the realm
        realm_name = realm[1]

        # get the description of the realm
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)

        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(R+BOLD+LocationVisuals().cross_location()+ENDC)
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # retrieve your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are faced with by a alrog monster" + ENDC)

        # show the monster
        print(R+BOLD+MonsterVisual().alrog_demon()+ENDC)

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the alrog monster" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        # print out all the user's weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)
        # ask user to select a weapon
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get your preferred weapon by id
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if your selection is invalid
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.terra_nova_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # after killing the monster
        # upgrade the users
        strength = 10
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)

        # add 10 to the user's current coin
        coin_gained = get_user[6] + 10
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)
        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])
        print(f"This is your new balance: {get_user[6]}")

        # update the rank if strength level condition is met
        if 40 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        # update the current location of the game
        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 8)
            self.damned_valley_level(get_user)

    # can get an orb here
    def damned_valley_level(self, user):
        # ask user if they want to continue or not
        self.contnue_or_quit()

        # get user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(8)

        # location name
        location_name = get_location[1]

        # location description
        location_description = get_location[2]

        # get the realm
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # realm description
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(R+BOLD+LocationVisuals().damned_valley()+ENDC)
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # get your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are in contact with the Bazog demon " + ENDC)

        print(R+BOLD+MonsterVisual().bazog_demon()+ENDC)

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the bazog monster" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        #  lists all users weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)

        # select the weapon using the S/N (also known as the id)
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get the weapon by passing the id into the method
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if the user entry is in valid reset the world
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.dark_dungeon_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # update the user's strength level
        strength = 10
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)
        # add to the user's current coin
        coin_gained = get_user[6] + 10
        # initiate the update price method
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)

        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        print("==" * 50)
        print(O + BOLD + "You look around and you found an orb" + ENDC)
        print("==" * 50)

        # current location id
        location_id = 8

        # retrieve the orb
        orb = RetrieveTransaction().get_orb_by_location(location_id)

        # orb name
        orb_name = orb[0][1]

        # orb description
        orb_description = orb[0][2]

        # show the orb visuals
        print(O + BOLD + f"""The orb is a {B}{orb_name}""" + ENDC)
        print(R + BOLD + OrbVisuals().vida() + ENDC)
        print()
        print(f"{orb_description}")
        print("You stretch out your hands and grab it")

        # save the user's orb
        save_user_orb = CreateInsertUpdateDeleteRecord().save_user_orb(get_user[0], orb[0][0])

        # if save had an issue then print an error
        if not save_user_orb:
            print(R+BOLD+"Sorry something went wrong with the program"+ENDC)

        print(G + BOLD + "You have an orb now. Congrats" + ENDC)

        # get new user id
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # try to update the rank by making sure rank condition is met

        if 50 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        get_user_orbs = RetrieveTransaction().get_user_orb(get_user[0])

        # line of code is for locations with orbs
        if get_user_orbs and len(get_user_orbs) >= 3:
            print(O + BOLD + "This is your ascension to The Paraíso relam!" + ENDC)
            CreateInsertUpdateDeleteRecord().game_won(get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 11)
            self.golden_gates_level(get_user)

        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 9)
            self.torture_lair(get_user)

    # no orb here
    def torture_lair(self, user):

        # do you want to quit or continue
        self.contnue_or_quit()

        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(9)

        # get the name of the current location
        location_name = get_location[1]

        # get the description of the current location
        location_description = get_location[2]

        # get the realm object
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the name of the realm
        realm_name = realm[1]

        # get the description of the realm
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)

        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(R+BOLD+LocationVisuals().torture_liar()+ENDC)
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # retrieve your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are faced with by The torturers" + ENDC)

        # show the monster
        print(R+BOLD+MonsterVisual().alrog_demon()+ENDC)

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the The torturers" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        # print out all the user's weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)
        # ask user to select a weapon
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get your preferred weapon by id
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if your selection is invalid
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.terra_nova_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # after killing the monster
        # upgrade the users
        strength = 10
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)

        # add 10 to the user's current coin
        coin_gained = get_user[6] + 10
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)
        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        # get new user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])
        print(f"This is your new balance: {get_user[6]}")

        # update the rank if strength level condition is met

        if 40 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        # update the current location of the game
        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 10)
            self.snake_island_level(get_user)

    # has an orb
    def demon_cave_level(self, user):
        # ask user if they want to continue or not
        self.contnue_or_quit()

        # get user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(10)

        # location name
        location_name = get_location[1]

        # location description
        location_description = get_location[2]

        # get the realm
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # realm description
        realm_description = realm[2]

        print(f"""
        ===========================================================================
        {R}{BOLD} Hi, {user[1]}! {ENDC}
        ===========================================================================
        {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
        ===========================================================================
        {O}{BOLD} {realm_description}.{ENDC}
        ===========================================================================
        """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(R+BOLD+LocationVisuals().demon_cave()+ENDC)
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        # get your weapon
        weapons = RetrieveTransaction().get_user_weapons(get_user[0])

        print(O + BOLD + "Here you are in contact with the fire dragon " + ENDC)

        print(R+BOLD+MonsterVisual().fire_dragon()+ENDC)

        print("==" * 50)

        print(O + BOLD + "Use your weapon to slay the fire dragon" + ENDC)

        print(O + BOLD + "Here is a list of your weapons" + ENDC)

        #  lists all users weapons
        for weapon in weapons:
            print(f"""
               =======================================
               {B}S/N: {R}{weapon[0]}{ENDC}
               {B}Weapons: {R}{weapon[1]}{ENDC}
               ========================================
               """)

        # select the weapon using the S/N (also known as the id)
        weapon_id = input(B + BOLD + "Choose the serial number of the weapon? " + ENDC)

        # get the weapon by passing the id into the method
        get_the_weapon = RetrieveTransaction().get_weapon_by_id(int(weapon_id))

        # if the user entry is in valid reset the world
        if not get_the_weapon:
            print(R + B + f"Invalid entry" + ENDC)
            self.dark_dungeon_level(get_user)

        print(B + BOLD + f"You have selected {get_the_weapon[1]}. And you use it to deliver a fetal blow")

        print("==" * 50)

        print(O + BOLD + f"The monster is dead!!!" + ENDC)
        print("==" * 50)

        # update the user's strength level
        strength = 10
        update_strength_level = CreateInsertUpdateDeleteRecord().update_strength_level(get_user[0], strength=strength)
        # add to the user's current coin
        coin_gained = get_user[6] + 10
        # initiate the update price method
        upgrade_coin = CreateInsertUpdateDeleteRecord().update_price(get_user[0], coin_gained)

        print(O + BOLD + "Because of your heroic act you have also gained some coins" + ENDC)
        print("==" * 50)
        print(O + BOLD + "You look around and you found n orb" + ENDC)
        print("==" * 50)

        # current location id
        location_id = 10

        # retrieve the orb
        orb = RetrieveTransaction().get_orb_by_location(location_id)

        # orb name
        orb_name = orb[0][1]

        # orb description
        orb_description = orb[0][2]

        # show the orb visuals
        print(O + BOLD + f"""The orb is a {B}{orb_name}""" + ENDC)
        print(B + BOLD + OrbVisuals().conecementor() + ENDC)
        print()
        print(f"{orb_description}")
        print("You stretch out your hands and grab it")

        # save the user's orb
        save_user_orb = CreateInsertUpdateDeleteRecord().save_user_orb(get_user[0], orb[0][0])

        # if save had an issue then print an error
        if not save_user_orb:
            print(R+BOLD+"Sorry something went wrong with the program"+ENDC)

        print(G + BOLD + "You have an orb now. Congrats" + ENDC)

        # get new user id
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # try to update the rank by making sure rank condition is met

        if 40 <= get_user[3] < 100:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="medio")
        elif get_user[3] >= 90:
            CreateInsertUpdateDeleteRecord().update_rank(get_user[0], rank="alto")

        get_user_orbs = RetrieveTransaction().get_user_orb(get_user[0])

        # line of code is for locations with orbs
        if get_user_orbs and len(get_user_orbs) >= 3:
            print(O + BOLD + "This is your ascension to The Paraíso relam!" + ENDC)
            CreateInsertUpdateDeleteRecord().game_won(get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 11)
            self.golden_gates_level(get_user)

        if update_strength_level and upgrade_coin:
            print("Well done Warrior. Move to the next phase. Search for the orbs")
            get_user = RetrieveTransaction().get_user_by_id(user_id=get_user[0])
            CreateInsertUpdateDeleteRecord().save_user_location(get_user[0], 1)
            self.terra_market_place_level(get_user[0], get_user[1])

    # the golden paradise gate of Paraíso
    def golden_gates_level(self, user):
        # get user object
        get_user = RetrieveTransaction().get_user_by_id(user_id=user[0])

        # get the current location by id
        get_location = RetrieveTransaction().get_location_by_id(11)

        # location name
        location_name = get_location[1]

        # location description
        location_description = get_location[2]

        # get the realm
        realm = RetrieveTransaction().get_realm_by_id(realm_id=get_location[3])

        # get the realm name
        realm_name = realm[1]

        # realm description
        realm_description = realm[2]

        print(f"""
                ===========================================================================
                {R}{BOLD} Hi, {user[1]}! {ENDC}
                ===========================================================================
                {O}{BOLD} Welcome to The {realm_name} realm {ENDC}
                ===========================================================================
                {O}{BOLD} {realm_description}.{ENDC}
                ===========================================================================
                """)
        print(O + BOLD + f"Your current location is the: {R}{location_name}" + ENDC)
        print(O+BOLD+LocationVisuals().paraiso()+ENDC)
        print("==" * 50)
        print(B + BOLD + f"location description: {location_description}" + ENDC)
        print("==" * 50)

        print(O+BOLD+f"CONGRTULATIONS! {get_user[1]} YOU HAVE ASCENDED BY INTO PARAISO THE GOLDEN CITY OF THE GODS"+ENDC)

        self.contnue_or_quit()


def main():
    # create an object of the game class
    fallen = Fallen()
    print("==" * 50)
    print(G + BOLD + f'==' * 10, f'Connected on {datetime.now().strftime("%A, %B %d, %Y, %H:%M %p")}', '==' * 15, ENDC)
    print("==" * 50)
    print(UNDERLINE + BOLD + R + "Welcome to Fallen Game World!" + ENDC)
    print("==" * 50)
    print(B + BOLD + "Game Overview" + ENDC)
    print("==" * 50)
    print(BOLD + O + GamePlayVisuals().game_play() + ENDC)
    print("==" * 50)
    prompt = input(
        f"""
            ======================================================= 
            {B}{BOLD}To create an account, enter 1: {ENDC}
            =======================================================
            {B}{BOLD}To login and continue playing, enter 2: {ENDC} 
            =======================================================
            {R}{BOLD}To quit, enter q: {ENDC} 
            """
    ).lower()

    while True:
        if prompt == '1':
            fallen.create_account()
            break
        elif prompt == '2':
            fallen.login()
            break
        elif prompt == 'q':
            print("Thank you, Goodbye!!!")
            quit()
            break
        else:
            prompt = input(
                f"""
                    {R}Invalid input{ENDC}
                    ============================================
                    Please try again
                    ============================================ 
                    {B}{BOLD}To create an account, enter 1: {ENDC} 
                    =======================================================
                    {B}{BOLD}To login and continue playing, enter 2: {ENDC} 
                    =======================================================
                    {R}{BOLD}To quit, enter q: {ENDC} 
                    """
            ).lower()


if __name__ == '__main__':
    main()