import random as rand


def generate_population(specimen_template, n):
    """ Population generator
    Generates population accoriding to given template

    :param specimen_template - [(real, (low, high)),...]
    :param n - size of population
    """

    population = [None] * n
    for i in range(n):
        population[i] = generate_specimen(specimen_template)
    return population


def generate_specimen(specimen_template):
    """ Specimen generator
    Generates specimen accoriding to given template

    :param specimen_template - [(real, (low, high)),...]
    """

    specimen = []
    for att in specimen_template:
        att_type = att = att[0]
        low = att[1][0]
        high = att[1][1]

        if att_type == 'real':
            specimen.append(rand.random() * (high - low) + low)
        elif att_type == 'integer':
            specimen.append(rand.randint(low, high))
        else:
            specimen.append(None)
    return specimen


def validate_constrains(specimen, specimen_template):
    """ Constrains validator
    Validates if any attribute of specimen violate given constrains
    if yes then generate new value for it
    Note! - indexes of attributes of specimen and template must be same

    :param specimen - specimen to validate
    :param specimen_template - template with constrains
    """
    for att_index in range(len(specimen_template)):
        low_const = specimen_template[att_index][1][0]
        high_const = specimen_template[att_index][1][1]
        # If attribute cross constrains then generate new value for it
        if specimen[att_index] > high_const or specimen[att_index] < low_const:
            att_type = specimen_template[att_index][0]
            # Generate new value for attribute
            if att_type == 'real':
                specimen[att_index] = rand.random() * (high_const - low_const) + low_const
            elif att_type == 'integer':
                specimen[att_index] = rand.randint(low_const, high_const)
            else:
                specimen[att_index] = None


def soft_penalization():
    pass


def hard_penalization():
    pass

