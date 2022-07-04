import random
import math
import csv
import datetime

map_size = 100  # the width and height of the map
starting_pop = 100  # the starting population of the three species
sim_cycles = 10  # how many generations the simulation runs before ending
food_amount = 600  # the amount of food generated at the start of each generation
sim_times = 1  # how many times the simulation runs

class Lifeform():

    def __init__(self, mutability, speed, combat, foraging, energy, xcoord, ycoord, got_food):
        self._mutability = mutability
        self._speed = speed
        self._combat = combat
        self._foraging = foraging
        self._energy = energy
        self._xcoord = xcoord
        self._ycoord = ycoord
        self._got_food = got_food

    def getmutability(self):
        return self._mutability

    def setmutability(self, value):
        self._mutability = value

    def getspeed(self):
        return self._speed

    def setspeed(self, value):
        self._speed = value

    def getcombat(self):
        return self._combat

    def setcombat(self, value):
        self._combat = value

    def getforaging(self):
        return self._foraging

    def setforaging(self, value):
        self._foraging = value

    def getenergy(self):
        return self._energy

    def setenergy(self, value):
        self._energy = value

    def getx(self):
        return self._xcoord

    def setx(self, value):
        self._xcoord = value

    def gety(self):
        return self._ycoord

    def sety(self, value):
        self._ycoord = value

    def got_food(self):
        return self._got_food

    def setgot_food(self, value):
        self._got_food = value

    def swapgot_food(self):
        if self.got_food():
            self.setgot_food(False)
        else:
            self.setgot_food(True)

    def __str__(self):
        return ("Mutability: " + str(self.getmutability()) +
                "\nSpeed: " + str(self.getspeed()) +
                "\nCombat: " + str(self.getcombat()) + "\nForaging: " + str(self.getforaging()))


class Species():

    def __init__(self, name, list_of_lifeforms, population, mutability=0, speed=0, combat=0, foraging=0):
        self._name = name
        self._population = population
        self._mutability = mutability
        self._speed = speed
        self._combat = combat
        self._foraging = foraging
        self._list_of_lifeforms = list_of_lifeforms

    def getlistoflifeforms(self):
        return self._list_of_lifeforms

    def setlistoflifeforms(self, new_list):
        self._list_of_lifeforms = new_list

    def getname(self):
        return self._name

    def setname(self, value):
        self._name = value

    def getpopulation(self):
        return self._population

    def setpopulation(self):
        self._population = len(self.getlistoflifeforms())

    def getmutability(self):
        return self._mutability

    def setmutability(self):
        self._mutability = 0
        if len(self.getlistoflifeforms()) != 0:
            for i in self.getlistoflifeforms():
                self._mutability += i.getmutability()
            self._mutability /= len(self.getlistoflifeforms())

    def getspeed(self):
        return self._speed

    def setspeed(self):
        self._speed = 0
        if len(self.getlistoflifeforms()) != 0:
            for i in self.getlistoflifeforms():
                self._speed += i.getspeed()
            self._speed /= len(self.getlistoflifeforms())

    def getcombat(self):
        return self._combat

    def setcombat(self):
        self._combat = 0
        if len(self.getlistoflifeforms()) != 0:
            for i in self.getlistoflifeforms():
                self._combat += i.getcombat()
            self._combat /= len(self.getlistoflifeforms())

    def getforaging(self):
        return self._foraging

    def setforaging(self):
        self._foraging = 0
        if len(self.getlistoflifeforms()) != 0:
            for i in self.getlistoflifeforms():
                self._foraging += i.getforaging()
            self._foraging /= len(self.getlistoflifeforms())

    def setall(self):
        self.setpopulation()
        self.setmutability()
        self.setspeed()
        self.setcombat()
        self.setforaging()

    def printlistoflife(self):
        for i in self.getlistoflifeforms():
            print(i)
            print()

    def __str__(self):
        return ("Species: " + str(self.getname()) + "\nPopulation: " + str(self.getpopulation()) +
                "\nAvg. Mutability: " + str(self.getmutability()) + "\nAvg. Speed: " + str(self.getspeed()) +
                "\nAvg. Combat: " + str(self.getcombat()) + "\nAvg. Foraging: " + str(self.getforaging()))


class Food():

    def __init__(self, xcoord, ycoord, energy):
        self._xcoord = xcoord
        self._ycoord = ycoord
        self._energy = energy

    def getx(self):
        return self._xcoord

    def setx(self, value):
        self._xcoord = value

    def gety(self):
        return self._ycoord

    def sety(self, value):
        self._ycoord = value

    def getenergy(self):
        return self._energy

    def __str__(self):
        return ("(" + str(self.getx()) + "," + str(self.gety()) + "): " + str(self.getenergy()))


def gatherdata(list_of_species, list_of_food, current_tick, sim_times):  # Writes data to a csv file
    print("GATHER DATA")
    print()
    with open("c:\TempPath\data_file.csv", mode="a") as data_file:
        data_writer = csv.writer(data_file, delimiter=",")
        for i in list_of_species:
            i.setall()
            data_writer.writerow(
                [sim_times, current_tick, i.getname(), i.getpopulation(), i.getmutability(), i.getspeed(),
                 i.getcombat(), i.getforaging()])


def foodgen(list_of_food, gen_rate):
    print("FOOD GENERATION")
    for i in range(gen_rate):
        x = random.randint(1, map_size)
        y = random.randint(1, map_size)
        energy = int(round(random.gauss(10, 1), 0))
        list_of_food.append(Food(x, y, energy))


def movement(lifeform, list_of_food):
    closest_distance = 101
    closest_food_x = 0
    closest_food_y = 0
    for food in list_of_food:
        food_distance = math.sqrt(
            math.pow(lifeform.getx() - food.getx(), 2) + math.pow(lifeform.gety() - food.gety(), 2))
        if food_distance < closest_distance:
            closest_distance, closest_food_x, closest_food_y = food_distance, food.getx(), food.gety()
    if closest_distance <= lifeform.getforaging():
        # DEBUGGING
        # print("closest_distance < 101")
        # ---------
        if closest_distance < lifeform.getspeed():
            # DEBUGGING
            # print("closest_distance < lifeform.getspeed()")
            # ---------
            lifeform.setx(closest_food_x)
            lifeform.sety(closest_food_y)
            lifeform.setenergy(int(round(
                lifeform.getenergy() - (food_distance / lifeform.getspeed() * math.pow(lifeform.getspeed(), 1.2)) / 10,
                0)))
        else:
            # DEBUGGING
            # print("closest_distance >= lifeform.getspeed()")
            # ---------
            if closest_food_x != lifeform.getx():
                angle = math.atan(abs((closest_food_y - lifeform.gety()) / (closest_food_x - lifeform.getx())))
            if closest_food_x > lifeform.getx() and closest_food_y > lifeform.gety():
                # DEBUGGING
                # print("closest_food_x > lifeform.getx() and closest_food_y > lifeform.gety()")
                # ---------
                lifeform.setx(int(round(lifeform.getx() + lifeform.getspeed() * math.cos(angle), 0)))
                lifeform.sety(int(round(lifeform.gety() + lifeform.getspeed() * math.sin(angle), 0)))
            elif closest_food_x > lifeform.getx() and closest_food_y < lifeform.gety():
                # DEBUGGING
                # print("closest_food_x > lifeform.getx() and closest_food_y < lifeform.gety()")
                # ---------
                lifeform.setx(int(round(lifeform.getx() + lifeform.getspeed() * math.cos(angle), 0)))
                lifeform.sety(int(round(lifeform.gety() - lifeform.getspeed() * math.sin(angle), 0)))
            elif closest_food_x < lifeform.getx() and closest_food_y > lifeform.gety():
                # DEBUGGING
                # print("closest_food_x < lifeform.getx() and closest_food_y > lifeform.gety()")
                # ---------
                lifeform.setx(int(round(lifeform.getx() - lifeform.getspeed() * math.cos(angle), 0)))
                lifeform.sety(int(round(lifeform.gety() + lifeform.getspeed() * math.sin(angle), 0)))
            elif closest_food_x < lifeform.getx() and closest_food_y < lifeform.gety():
                # DEBUGGING
                # print("closest_food_x < lifeform.getx() and closest_food_y < lifeform.gety()")
                # ---------
                lifeform.setx(int(round(lifeform.getx() - lifeform.getspeed() * math.cos(angle), 0)))
                lifeform.sety(int(round(lifeform.gety() - lifeform.getspeed() * math.sin(angle), 0)))
            elif closest_food_y > lifeform.gety():
                # DEBUGGING
                # print("closest_food_y > lifeform.gety()")
                # ---------
                lifeform.sety(lifeform.gety() + lifeform.getspeed())
            elif closest_food_x > lifeform.getx():
                # DEBUGGING
                # print("closest_food_x > lifeform.getx()")
                # ---------
                lifeform.setx(lifeform.getx() + lifeform.getspeed())
            elif closest_food_y < lifeform.gety():
                # DEBUGGING
                # print("closest_food_y < lifeform.gety()")
                # ---------
                lifeform.sety(lifeform.gety() - lifeform.getspeed())
            else:
                # DEBUGGING
                # print("closest_food_x < lifeform.getx()")
                # ---------
                lifeform.setx(lifeform.getx() - lifeform.getspeed())
            lifeform.setenergy(int(round(lifeform.getenergy() - math.pow(lifeform.getspeed(), 1.2) / 10, 0)))
    else:
        # DEBUGGING
        # print("closest_distance >= 101")
        # ---------
        angle = math.radians(random.randint(1, 90))
        direction = random.randint(0, 3)
        if direction == 0:
            # DEBUGGING
            # print("direction == 0")
            # ---------
            newx = int(round(lifeform.getx() + lifeform.getspeed() * math.cos(angle), 0))
            newy = int(round(lifeform.gety() + lifeform.getspeed() * math.sin(angle), 0))
            if newx > map_size or newy > map_size:
                # DEBUGGING
                # print("newx > map_size or newy > map_size")
                # ---------
                lifeform.setx(random.randint(1, map_size))
                lifeform.sety(random.randint(1, map_size))
            else:
                # DEBUGGING
                # print("not newx > map_size and newy > map_size")
                # ---------
                lifeform.setx(newx)
                lifeform.sety(newy)
        elif direction == 1:
            # DEBUGGING
            # print("direction == 1")
            # ---------
            newx = int(round(lifeform.getx() + lifeform.getspeed() * math.cos(angle), 0))
            newy = int(round(lifeform.gety() - lifeform.getspeed() * math.sin(angle), 0))
            if newx > map_size or newy < 1:
                # DEBUGGING
                # print("newx > map_size or newy < 1")
                # ---------
                lifeform.setx(random.randint(1, map_size))
                lifeform.sety(random.randint(1, map_size))
            else:
                # DEBUGGING
                # print("not newx > map_size and newy < 1")
                # ---------
                lifeform.setx(newx)
                lifeform.sety(newy)
        elif direction == 2:
            # DEBUGGING
            # print("direction == 2")
            # ---------
            newx = int(round(lifeform.getx() - lifeform.getspeed() * math.cos(angle), 0))
            newy = int(round(lifeform.gety() - lifeform.getspeed() * math.sin(angle), 0))
            if newx < 1 or newy < 1:
                # DEBUGGING
                # print("newx < 1 or newy < 1")
                # ---------
                lifeform.setx(random.randint(1, map_size))
                lifeform.sety(random.randint(1, map_size))
            else:
                lifeform.setx(newx)
                lifeform.sety(newy)
        else:
            newx = int(round(lifeform.getx() - lifeform.getspeed() * math.cos(angle), 0))
            newy = int(round(lifeform.gety() + lifeform.getspeed() * math.sin(angle), 0))
            if newx < 1 or newy > map_size:
                lifeform.setx(random.randint(1, map_size))
                lifeform.sety(random.randint(1, map_size))
            else:
                lifeform.setx(newx)
                lifeform.sety(newy)
        lifeform.setenergy(int(round(lifeform.getenergy() - math.pow(lifeform.getspeed(), 1.2) / 10, 0)))


def deathcheck(list_of_species):
    print("DEATH CHECK")
    for i in list_of_species:
        listoflifeforms = [x for x in i.getlistoflifeforms() if not x.getenergy() < 1]
        i.setlistoflifeforms(listoflifeforms)


def enemycollision(list_of_species):
    print("ENEMY COLLISION")
    for i in list_of_species:
        for j in i.getlistoflifeforms():
            for k in list_of_species:
                if i != k:
                    for m in i.getlistoflifeforms():
                        if j.getx() == m.getx() and j.gety() == m.gety():
                            j.setenergy(int(round(j.getenergy() - 100 / j.getcombat(), 0)))
                            m.setenergy(int(round(m.getenergy() - j.getcombat() / 5, 0)))


def foodcollision(list_of_species, list_of_food):
    print("FOOD COLLISION")
    for food in list_of_food:
        lifeform_count = 0
        for j in list_of_species:
            for k in j.getlistoflifeforms():
                if food.getx() == k.getx() and food.gety() == k.gety():
                    lifeform_count += 1
        if lifeform_count > 0:
            for j in list_of_species:
                for k in j.getlistoflifeforms():
                    if food.getx() == k.getx() and food.gety() == k.gety():
                        k.setenergy(k.getenergy() + food.getenergy() / lifeform_count)
                        if k.getenergy() > 100:
                            k.setenergy(100)
                        k.setgot_food(True)
            food.setx(-1)
    list_of_food = [x for x in list_of_food if not x.getx() == -1]
    return list_of_food


def movecycles(list_of_species, list_of_food):
    print("MOVE CYCLE INITIATION")
    generation_complete = False
    [[lifeform.setgot_food(False) for lifeform in i.getlistoflifeforms()] for i in list_of_species]
    while not generation_complete:
        print("MOVEMENT")
        for i in list_of_species:
            [movement(j, list_of_food) for j in i.getlistoflifeforms() if not j.got_food()]
        deathcheck(list_of_species)
        enemycollision(list_of_species)
        deathcheck(list_of_species)
        list_of_food = foodcollision(list_of_species, list_of_food)
        test_complete = True
        for i in list_of_species:
            for j in i.getlistoflifeforms():
                if not j.got_food():
                    test_complete = False
                    generation_complete = False
                else:
                    if test_complete:
                        generation_complete = True
    return list_of_food


def breeding(list_of_species):
    print("BREEDING")
    for i in list_of_species:
        child_list = []
        random.shuffle(i.getlistoflifeforms())
        for j in range(int(len(i.getlistoflifeforms()) / 2)):
            parent_1 = i.getlistoflifeforms()[(j + 1) * 2 - 2]
            parent_2 = i.getlistoflifeforms()[(j + 1) * 2 - 1]
            child = Lifeform(0, 0, 0, 0, 100, random.randint(1, map_size), random.randint(1, map_size), False)
            mutation_rate = (parent_1.getmutability() + parent_2.getmutability()) / 20
            if random.randint(1, 2) == 1:
                while child.getmutability() < 1 or child.getmutability() > 100:
                    child.setmutability(int(round(random.gauss(parent_1.getmutability(), mutation_rate), 0)))
            else:
                while child.getmutability() < 1 or child.getmutability() > 100:
                    child.setmutability(int(round(random.gauss(parent_2.getmutability(), mutation_rate), 0)))
            if random.randint(1, 2) == 1:
                while child.getspeed() < 1 or child.getspeed() > 100:
                    child.setspeed(int(round(random.gauss(parent_1.getspeed(), mutation_rate), 0)))
            else:
                while child.getspeed() < 1 or child.getspeed() > 100:
                    child.setspeed(int(round(random.gauss(parent_2.getspeed(), mutation_rate), 0)))
            if random.randint(1, 2) == 1:
                while child.getcombat() < 1 or child.getcombat() > 100:
                    child.setcombat(int(round(random.gauss(parent_1.getcombat(), mutation_rate), 0)))
            else:
                while child.getcombat() < 1 or child.getcombat() > 100:
                    child.setcombat(int(round(random.gauss(parent_2.getcombat(), mutation_rate), 0)))
            if random.randint(1, 2) == 1:
                while child.getforaging() < 1 or child.getforaging() > 100:
                    child.setforaging(int(round(random.gauss(parent_1.getforaging(), mutation_rate), 0)))
            else:
                while child.getforaging() < 1 or child.getforaging() > 100:
                    child.setforaging(int(round(random.gauss(parent_2.getforaging(), mutation_rate), 0)))
            if child.getcombat() + child.getforaging() > 100:
                excess = (child.getcombat() + child.getforaging() - 100) / 2
                if (child.getcombat() + child.getforaging()) % 2 == 0:
                    child.setcombat(int(child.getcombat() - excess))
                    child.setforaging(int(child.getforaging() - excess))
                else:
                    if child.getcombat() > child.getforaging():
                        child.setcombat(int(round(child.getcombat() - excess - 1, 0)))
                        child.setforaging(int(round(child.getforaging() - excess, 0)))
                    else:
                        child.setcombat(int(round(child.getcombat() - excess, 0)))
                        child.setforaging(int(round(child.getforaging() - excess - 1, 0)))
            elif child.getcombat() + child.getforaging() < 100:
                missing = (100 - child.getcombat() - child.getforaging()) / 2
                if (child.getcombat() + child.getforaging()) % 2 == 0:
                    child.setcombat(int(child.getcombat() + missing))
                    child.setforaging(int(child.getforaging() + missing))
                else:
                    if child.getcombat() > child.getforaging():
                        child.setcombat(int(child.getcombat() + missing + 1))
                        child.setforaging(int(child.getforaging() + missing))
                    else:
                        child.setcombat(int(child.getcombat() + missing))
                        child.setforaging(int(child.getforaging() + missing + 1))
            child_list.append(child)
        for j in child_list:
            i.getlistoflifeforms().append(j)


def runsim(current_tick, max_ticks, list_of_species, list_of_food, sim_times):
    print("GENERATION " + str(current_tick) + " STARTED")
    foodgen(list_of_food, food_amount)
    list_of_food = movecycles(list_of_species, list_of_food)
    breeding(list_of_species)
    gatherdata(list_of_species, list_of_food, current_tick, sim_times)
    if current_tick != max_ticks:
        runsim(current_tick + 1, max_ticks, list_of_species, list_of_food, sim_times)


def createspecies():
    print("SPECIES CREATED")
    rabbit_list = []
    rabbit = Species("Rabbit", rabbit_list, starting_pop, 50, 50, 50, 50)
    for i in range(starting_pop):
        rabbit_list.append(Lifeform(rabbit.getmutability(), rabbit.getspeed(),
                                    rabbit.getcombat(), rabbit.getforaging(), 100, 0, 0, False))

    turtle_list = []
    turtle = Species("Turtle", turtle_list, starting_pop, 50, 50, 50, 50)
    for i in range(starting_pop):
        turtle_list.append(Lifeform(turtle.getmutability(), turtle.getspeed(),
                                    turtle.getcombat(), turtle.getforaging(), 100, 0, 0, False))

    human_list = []
    human = Species("Human", human_list, starting_pop, 50, 50, 50, 50)
    for i in range(starting_pop):
        human_list.append(Lifeform(human.getmutability(), human.getspeed(),
                                   human.getcombat(), human.getforaging(), 100, 0, 0, False))

    list_of_species = [rabbit, turtle, human]
    return list_of_species


def spawnlifeforms(list_of_species):
    print("LIFE SPAWNED")
    for i in list_of_species:
        for j in i.getlistoflifeforms():
            x = random.randint(1, map_size)
            y = random.randint(1, map_size)
            j.setx(x)
            j.sety(y)


def startup(sim_times):
    print("START")
    list_of_species = createspecies()
    list_of_food = []
    spawnlifeforms(list_of_species)
    gatherdata(list_of_species, list_of_food, 0, sim_times)
    runsim(1, sim_cycles, list_of_species, list_of_food, sim_times)


# Initiates Program
# Prints simulation number, then runs the simulation

startTime = datetime.datetime.now()
for i in range(sim_times):
    print(i + 1)
    startup(i + 1)

endTime = datetime.datetime.now()
print(endTime - startTime)
