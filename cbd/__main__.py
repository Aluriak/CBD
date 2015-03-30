# -*- coding: utf-8 -*-
#########################
#       MAIN            #
#########################


#########################
# IMPORTS               #
#########################
from cbd.database import Database, DATABASE_NAME
import matplotlib.pyplot as plt
import networkx as nx
import pylab
import glob
import csv
import os



#########################
# PRE-DECLARATIONS      #
#########################
# STUDY PARAMETERS
PROTEIN_NAME = 'hepcidin'
# OUTPUT FILES
OUTPUT_FILE_REPERTORY            = 'data/outputs/'
CSV_HEPCIDIN_INTERACTION_BY_YEAR = OUTPUT_FILE_REPERTORY + 'interactionWith'+PROTEIN_NAME.title()+'ByYear.csv'
HEPCIDIN_INTERACTORS             = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'Interactors.txt'
CSV_HEPCIDIN_DISEASE_ASSOCIATION = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'DiseaseAssociation.csv'
CSV_HEPCIDIN_DISEASE_ASSOC_COUNT = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'DiseaseAssociationCount.csv'
CSV_HEPCIDIN_BACKGROUND_EVENTS   = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'BackgroundEvents.csv'
CSV_HEPCIDIN_BCKGRD_QUANTIF      = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'BackgroundQuantification.csv'
GRAPH_INTERACTION_BACKGROUND     = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'GraphInteractionsBackground{}.png'
GRAPH_INTERACTION_NON_BACKGROUND = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'GraphInteractionsNonBackground{}.png'
GIF_BACKGROUND_INTERACTION       = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'BackgroundInteractions.gif'
GIF_NON_BACKGROUND_INTERACTION   = OUTPUT_FILE_REPERTORY + PROTEIN_NAME + 'NonBackgroundInteractions.gif'
# MODULAR CONSTANTS
DB_AVAILABLE = lambda: os.path.exists(DATABASE_NAME)
DELETE_ALL_FILES_BEFORE          = True
DELETE_ALL_FILES_BEFORE          = False



#########################
# MAIN                  #
#########################
if __name__ == '__main__':
    if DELETE_ALL_FILES_BEFORE: 
        for filename in glob.glob(OUTPUT_FILE_REPERTORY + '*'):
            os.remove(filename)
        os.remove(DATABASE_NAME)
        print('ALL FILES ARE DELETED !')


    print('DATABASE MANAGEMENT…')
    db = Database('data/events_data/events_20*.txt', 'data/create_database.sql', db_available=DB_AVAILABLE())
    #db = Database('data/events_data/events_20*.txt', 'data/create_database.sql', db_available=False)
    print('DONE !')


    print('FIRST NEED…')
    print('\tINTERACTIONS COUNTING… (see file ' + CSV_HEPCIDIN_INTERACTION_BY_YEAR + ')')
    # first need: interactions with hepcidin
    if not os.path.exists(CSV_HEPCIDIN_INTERACTION_BY_YEAR):
        with open(CSV_HEPCIDIN_INTERACTION_BY_YEAR, 'w') as fd:
            writer = csv.DictWriter(fd, fieldnames=['year', 'eventCount'])
            writer.writeheader()
            for year, nb_interaction in db.by_year_interaction(PROTEIN_NAME):
                writer.writerow({'year': year, 'eventCount': nb_interaction})
    # first need: interactions with hepcidin (show all interactors)
    print('\tINTERACTORS LISTING… (see file ' + HEPCIDIN_INTERACTORS + ')')
    if not os.path.exists(HEPCIDIN_INTERACTORS):
        with open(HEPCIDIN_INTERACTORS, 'w') as fd:
            fd.write('\n'.join(db.interaction_with(PROTEIN_NAME)))


    print('SECOND NEED…')
    print('\tDISEASES LISTING… (see files ' + CSV_HEPCIDIN_DISEASE_ASSOCIATION 
          + 'and ' + CSV_HEPCIDIN_DISEASE_ASSOC_COUNT + ')')
    if(not os.path.exists(CSV_HEPCIDIN_DISEASE_ASSOCIATION) or 
       not os.path.exists(CSV_HEPCIDIN_DISEASE_ASSOC_COUNT)):
        with open(CSV_HEPCIDIN_DISEASE_ASSOCIATION, 'w') as fd_names, open(CSV_HEPCIDIN_DISEASE_ASSOC_COUNT, 'w') as fd_count :
            writer_names = csv.DictWriter(fd_names, fieldnames=['disease', 'discovYear'])
            writer_count = csv.DictWriter(fd_count, fieldnames=['year', 'diseases'])
            writer_names.writeheader()
            writer_count.writeheader()
            for year in db.years:
                diseases = (str(_) for _ in db.associations_in_year(PROTEIN_NAME, year, 
                                                                    associated_with='I', # deseases only 
                                                                    name_only=True, unique=True))
                disease_number = 0
                for disease in diseases:
                    writer_names.writerow({'disease':disease, 'discovYear':year})
                    disease_number += 1
                writer_count.writerow({'year':year, 'diseases':disease_number})


    print('THIRD NEED…')
    print('\tINTERACTORS COUNTING… (see file ' + CSV_HEPCIDIN_BACKGROUND_EVENTS + ')')
    background_events = None
    if not os.path.exists(CSV_HEPCIDIN_BACKGROUND_EVENTS):
        with open(CSV_HEPCIDIN_BACKGROUND_EVENTS, 'w') as fd:
            writer = csv.DictWriter(fd, fieldnames=['protein', 'yearsCount'])
            writer.writeheader()
            background_events = db.count_association_over_year(PROTEIN_NAME, minimal_count=2)
            for protein_name, appearances in background_events.items():
                writer.writerow({'protein':protein_name, 'yearsCount':appearances})


    print('FOURTH NEED…')
    print('\tBACKGROUND COUNTING… (see file ' + CSV_HEPCIDIN_BCKGRD_QUANTIF + ')')
    background_associations = None
    if not os.path.exists(CSV_HEPCIDIN_BCKGRD_QUANTIF):
        with open(CSV_HEPCIDIN_BCKGRD_QUANTIF, 'w') as fd:
            writer = csv.DictWriter(fd, fieldnames=['association', 'count'])
            writer.writeheader()
            # background associations
            background_associations = db.background_associations(
                PROTEIN_NAME, associated_with='P'
            )
            writer.writerow({'association':'background', 'count':len(background_associations)})
            # all associations
            know_associations = set() 
            for year in db.years:
                associations = db.associations_in_year(
                    PROTEIN_NAME, year, associated_with='P', name_only=True, unique=True
                )
                for association in associations:
                    know_associations.add(association)
            writer.writerow({'association':'unique', 'count':len(know_associations)})


    print('FIFTH NEED…')

    # Create a new graph
    if DELETE_ALL_FILES_BEFORE:
        root_node = PROTEIN_NAME
        graph_back = nx.Graph() # only background events
        graph_nobk = nx.Graph() # without background events
        graph_back.add_node(root_node) 
        graph_nobk.add_node(root_node) 
        # just add not already pushed proteins
        added_proteins = set()
        # used for print color of the edge to hepcidin 
        counts_back = [] # order conservation
        counts_nobk = [] # assure that color of edge correspond to a count proportion
        print('\tCOMPUTE BACKGROUND ASSOCIATIONS…')
        if background_associations is None:
            background_associations = db.background_associations(PROTEIN_NAME, associated_with='P')

        print('\tDRAW GRAPHS… (see png files)')
        for year, counters in db.count_association_by_year(PROTEIN_NAME).items():
            for protein, count in counters.items():
                if protein not in added_proteins: 
                    # fill the right graph
                    if protein in background_associations:
                        graph_back.add_node (protein)
                        graph_back.add_edge (protein, root_node)
                        counts_back.append(count)
                    else:
                        graph_nobk.add_node (protein)
                        graph_nobk.add_edge (protein, root_node)
                        counts_nobk.append(count)
                    added_proteins.add(protein)
            # print graph for background events
            plt.figure(figsize=(13,13))
            plt.axis('off')
            plt.title(PROTEIN_NAME + " have a background with "
                      + str(len(graph_back.nodes())-1) 
                      + " proteins studied in " + str(year)
                     )
            nx.draw(graph_back, node_color='#A4EBC2', 
                    edge_color=counts_back, width=4,
                    edge_cmap=plt.cm.Blues, 
                    with_labels=True
                   )
            plt.savefig(GRAPH_INTERACTION_BACKGROUND.format((str(year))))
            pylab.close()
            # print graph for non background events
            plt.figure(figsize=(13,13))
            plt.axis('off')
            plt.title(PROTEIN_NAME + " is associated to "
                      + str(len(graph_nobk.nodes())-1) 
                      + " proteins outside background events until " 
                      + str(year)
                     )
            nx.draw(graph_nobk, node_color='#A4EB02', 
                    edge_color=counts_nobk, width=4,
                    edge_cmap=plt.cm.Blues, 
                    with_labels=True
                   )
            plt.savefig(GRAPH_INTERACTION_NON_BACKGROUND.format((str(year))))
            pylab.close()


    print('FINISHED !')

